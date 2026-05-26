#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/kernel.h>
#include <linux/compiler.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/pci.h>
#include <linux/dma-mapping.h>
#include <linux/delay.h>
#include <linux/errno.h>
#include <linux/types.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <asm/io.h>
#include <asm/irq.h>
#include <asm/uaccess.h>
#include <linux/miscdevice.h>
#include <linux/netlink.h>
#include <net/netlink.h>
#include <net/net_namespace.h>

#include "oplk_datatype.h"

#define FPGA_MINOR                      151
#define FPGA_DEV_FILE_NAME              "xilinx"

#if 0
#define FPGA_DRV_VER                "1.0.0002"
#endif
#define FPGA_DRV_VER                "1.00.0001"


#define MAGIC_NUM 'f'

#define FPGA_GET_DRV_VER            _IO(MAGIC_NUM,1)
#define FPGA_GET_DRV_VER_STR_LEN    _IO(MAGIC_NUM,2)


#define FPGA_MAX_CMD                (2)

#define DRV_NAME                    "xilinx-fpga-pci"

#define MY_PCI_VENDOR_ID            (0x10EE) //(0x1304)
#define MY_PCI_DEVICE_ID            (0x7011) //(0x8B)

#define FPGA_ADD_LEN                (0x400000)  //0x100000 20220401
#define REG_STATUS                  (0x74)
static void __iomem *gBaseVirt;
static spinlock_t m_stSpinLock;


unsigned int    gStatFlags = 0;
int             gIrq;
struct pci_dev *gDev = NULL;
/* Protocol family, consistent in both kernel prog and user prog. */
#define MYPROTO NETLINK_USERSOCK
/* Multicast group, consistent in both kernel prog and user prog. */
#define MYGRP 21
static struct sock *nl_sk = NULL;

static struct pci_device_id xilinx_fpga_pci_tbl[] = {  
       {MY_PCI_VENDOR_ID, MY_PCI_DEVICE_ID, PCI_ANY_ID, PCI_ANY_ID, 0, 0, 0 },
       {0,}
};

MODULE_DEVICE_TABLE (pci, xilinx_fpga_pci_tbl);


#define XILINX_FPGA_READ(addr)          readl(gBaseVirt + (addr))
#define XILINX_FPGA_WRITE(val, addr)    writel((val), (gBaseVirt + (addr)))
static void send_to_user(void)
{
    struct sk_buff *skb;
    struct nlmsghdr *nlh;
    int res;
    unsigned int uiValue = 0;
    unsigned int uiOffset = REG_STATUS;
    char *msg = (char *)&uiValue;
    int msg_size = sizeof(uiValue)+1;

    uiValue = XILINX_FPGA_READ(uiOffset);   
    printk("uiValue0x%0x, uiOffset:0x%0x\n",uiValue,uiOffset);

    skb = nlmsg_new(NLMSG_ALIGN(msg_size+1), GFP_KERNEL);
    if (!skb) {
        pr_err("Allocation failure.\n");
        return;
    }

    nlh = nlmsg_put(skb, 0, 1, NLMSG_DONE, msg_size+1, 0);
    memcpy(nlmsg_data(nlh), (char *)msg, sizeof(uiValue));

    printk("Sending skb.\n");
    res = nlmsg_multicast(nl_sk, skb, 0, MYGRP, GFP_KERNEL);
    if (res < 0)
        printk("nlmsg_multicast() error: %d\n", res);
    else
        printk("Success.\n");
}

static irqreturn_t xilinx_fpga_irqhandle(int irq, void *dev_id)
{
    printk("%s xilinx_fpga_irqhandle  send_to_user..\n", FPGA_DEV_FILE_NAME);
    send_to_user();

    return IRQ_RETVAL(IRQ_HANDLED);
}

static int xilinx_fpga_open(struct inode *inode, struct file *file)
{

    return 0;
}

static int xilinx_fpga_release(struct inode *inode, struct file *file)
{

    return 0;
}

static ssize_t xilinx_fpga_write(struct file *file, const char __user *buffer,
        size_t count, loff_t *ppos)
{
    unsigned int  ulPos = *ppos;
    unsigned int i = 0;
    unsigned int  ulCount = 0;
    unsigned int uiFpgaAddrOffset  = 0;
    unsigned int  ulCountFromFpgaStart = 0;
    unsigned int  ulCountFromFpga = 0;
    unsigned int *puiBuffer = NULL;
    unsigned char ucBuf = 0;
    unsigned int uiAry = 0;
    unsigned int uiWide = 0;

    spin_lock(&m_stSpinLock);

    uiWide = 4;
    /* if(ulPos >= 0x20000)
    {
        printk("#### kernel : ulPos :0x%x\n",ulPos);
        uiWide = 2;
    } */

    if (ulPos > FPGA_ADD_LEN)
    {
        printk("#### kernel : _fpga_write offset overflow.\n");
        goto ERR_LABEL;
    }

    if ((ulPos + count) > FPGA_ADD_LEN)
    {
        ulCount = FPGA_ADD_LEN - ulPos;
    }
    else
    {
        ulCount = count;
    }


    /* if you lseek(0x0001_0001), write(0x55), FPGA driver will first
     * read 32 bits (00 00 00 66) from address 0x0001_0000, produce a new word
     * of 00 55 00 66, and write it back to address 0x0001_0000
     */

    ulCountFromFpgaStart = ulPos - (ulPos % uiWide);
    ulCountFromFpga = (ulPos%uiWide + ulCount + uiWide-1)/uiWide;

    puiBuffer = (unsigned int *)kmalloc(ulCount + 8, 0);
    if (NULL == puiBuffer)
    {
        printk("#### kernel : kmalloc err.\n");
        goto ERR_LABEL;
    }

    /* read 32 bits from FPGA                                                   */
    for(i=0; i<ulCountFromFpga; i++)
    {
        puiBuffer[i] = XILINX_FPGA_READ(ulCountFromFpgaStart+(i*uiWide));
    }

    /* replace puiBuffer byte one by one  */
    for (i = 0; i < ulCount; i++)
    {
        if (copy_from_user(&ucBuf, buffer+i, 1))
        {
            printk("#### kernel : _fpga_write copy_from_user err.\n");
            goto ERR_LABEL;
        }

        uiAry = (ulPos%uiWide + i)/uiWide;

        uiFpgaAddrOffset = (ulPos + i) % uiWide;

        if (0 == uiFpgaAddrOffset)
        {
            /* replace 7-0 bits bits                                            */
            puiBuffer[uiAry] = ((unsigned int)ucBuf) | (puiBuffer[uiAry] & 0xFFFFFF00);
        }
        else if(1 == uiFpgaAddrOffset)
        {
            /* replace 15-8 bits bits                                           */
            puiBuffer[uiAry] = ((unsigned int)ucBuf << 8) | (puiBuffer[uiAry] & 0xFFFF00FF);
        }
        else if(2 == uiFpgaAddrOffset)
        {
            /* replace 23-16 bits bits                                          */
            puiBuffer[uiAry] = ((unsigned int)ucBuf << 16) | (puiBuffer[uiAry] & 0xFF00FFFF);
        }
        else
        {
            /* replace 31-24 bits                                               */
            puiBuffer[uiAry] = ((unsigned int)ucBuf << 24) | (puiBuffer[uiAry] & 0x00FFFFFF);
        }
    }

    /* write 32 bits to FPGA                                                */
    for(i=0; i<ulCountFromFpga; i++)
    {
        XILINX_FPGA_WRITE(puiBuffer[i], ulCountFromFpgaStart+(i*uiWide));
    }

    *ppos += ulCount;

    spin_unlock(&m_stSpinLock);
    kfree(puiBuffer);
    puiBuffer = NULL;

    return ulCount;

ERR_LABEL :
    spin_unlock(&m_stSpinLock);
    if (NULL != puiBuffer)
    {
        kfree(puiBuffer);
        puiBuffer = NULL;
    }

    return -EINVAL;

}

static ssize_t xilinx_fpga_read(struct file *file, char __user *buf,
        size_t size, loff_t *ppos)
{

    unsigned int  ulPos = *ppos;
    unsigned int  ulCount = 0;
    unsigned int  ulCountFromFpgaStart = 0;
    unsigned int  ulCountFromFpga = 0;
    unsigned int i = 0;
    unsigned int j = 0;
    unsigned int iRet = 0;
    unsigned int *puiBuffer = NULL;
    unsigned char *pucBuffer = NULL;
    unsigned int uiWide = 0;

    spin_lock(&m_stSpinLock);

    uiWide = 4;

    if (ulPos > FPGA_ADD_LEN)
    {
        printk("#### kernel : _fpga_read offset overflow.\n");
        return -EINVAL;
    }

    if ((ulPos + size) > FPGA_ADD_LEN)
    {
        ulCount = FPGA_ADD_LEN - ulPos;
    }
    else
    {
        ulCount = size;
    }

    /* if you lseek(0x0001_0001), and read(1), FPGA driver will still
     * read 32 bits (11 22 33 44) from address 0x0001_0000, but only returns
     * the 2nd byte (0x22) to the caller;
     */
    ulCountFromFpgaStart = ulPos - (ulPos % uiWide);
    ulCountFromFpga = (ulPos%uiWide + ulCount + uiWide - 1)/uiWide;

    puiBuffer = (unsigned int *)kmalloc(2*ulCount + 8, 0);
    if (NULL == puiBuffer)
    {
        printk("#### kernel : kmalloc puiBuffer err.\n");
        goto ERR_LABEL;
    }

    /* read 32 bits from FPGA                                                   */
    for(i=0,j=0; i < ulCountFromFpga; i++, j+=2)
    {
        puiBuffer[i] = XILINX_FPGA_READ(ulCountFromFpgaStart+(i*uiWide));
    }

    if(2 == uiWide)
    {
        pucBuffer = (unsigned char *)kmalloc(2*ulCount + 8, 0);
        if (NULL == pucBuffer)
        {
            printk("#### kernel : kmalloc pucBuffer err.\n");
            goto ERR_LABEL;
        }

        /*
         * puiBuffer return 0x0000_xxxx(4 bytes), the valid value is the low 2 bytes
         * Copy the value 2 bytes to pucBuffer.
         * the ulCountFromFpga <= ulCount ==> the 2*ulCountFromFpga <2*ulCount+8, so
         * the following copy is save.
         */
        for(i=0,j=0; i < ulCountFromFpga; i++,j+=2)
        {
            memcpy(pucBuffer + j, &puiBuffer[i], 2);
        }

        /* copy 8 bits data to user namespace                                       */
        iRet = copy_to_user((unsigned char *)buf, (unsigned char *)pucBuffer + (ulPos % uiWide), ulCount);
        if (iRet > 0)
        {
            printk("#### kernel : _fpga_read copy_to_user err.\n");
            goto ERR_LABEL;
        }
    }
    else
    {
        /* copy 8 bits data to user namespace                                       */
        iRet = copy_to_user((unsigned char *)buf, (unsigned char *)puiBuffer + (ulPos % uiWide), ulCount);
        if (iRet > 0)
        {
            printk("#### kernel : _fpga_read copy_to_user err.\n");
            goto ERR_LABEL;
        }
    }

    *ppos += ulCount;

    spin_unlock(&m_stSpinLock);
    kfree(puiBuffer);
    puiBuffer = NULL;

    kfree(pucBuffer);
    pucBuffer = NULL;

    return ulCount;

ERR_LABEL :
    spin_unlock(&m_stSpinLock);
    if (NULL != puiBuffer)
    {
        kfree(puiBuffer);
        puiBuffer = NULL;
    }

    if (NULL != pucBuffer)
    {
        kfree(pucBuffer);
        pucBuffer = NULL;
    }

    return -EINVAL;

}

static loff_t xilinx_fpga_seek(struct file *file, loff_t off, int whence)
{
    unsigned long ulOffset = 0;

    spin_lock(&m_stSpinLock);

    switch (whence)
    {
        case SEEK_SET :
            ulOffset = off;
            break;

        case SEEK_CUR :
            ulOffset = file->f_pos + off;
            break;

        default :
            spin_unlock(&m_stSpinLock);
            return file->f_pos;
    }

    if (((file->f_pos) > FPGA_ADD_LEN) || (ulOffset > FPGA_ADD_LEN))
    {
        printk("#### kernel : _fpga_lseek offset overflow err.\n");
        goto ERR_LABEL;
    }

    file->f_pos = ulOffset;

    spin_unlock(&m_stSpinLock);

    return file->f_pos;
ERR_LABEL :
    spin_unlock(&m_stSpinLock);

    return -EINVAL;
}

static long xilinx_fpga_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    long lRes = 0;
    unsigned int uiLen;

    if(_IOC_TYPE(cmd) != MAGIC_NUM)
    {
        return -EINVAL;
    }

    if(_IOC_NR(cmd) > FPGA_MAX_CMD)
    {
        return -EINVAL;
    }

    spin_lock(&m_stSpinLock);

    switch(cmd)
    {
    case FPGA_GET_DRV_VER :
        if (copy_to_user((S8 *)arg, FPGA_DRV_VER, strlen(FPGA_DRV_VER)))
        {
            lRes = -EINVAL;
        }
        break;
    case FPGA_GET_DRV_VER_STR_LEN :
        uiLen = strlen(FPGA_DRV_VER);
        if (copy_to_user((U32 *)arg, &uiLen, sizeof(uiLen)))
        {
            lRes = -EINVAL;
        }
        break;
    default :
        //PRINTF("%s(), cpld %d INVALID COMMAND.\r\n", __FUNCTION__, iMinorNum);
        lRes = -EINVAL;
        break;
    }

    spin_unlock(&m_stSpinLock);

    return lRes;
}

static const struct file_operations xilinx_ops = {
    .owner   = THIS_MODULE,
    .open = xilinx_fpga_open,
    .read = xilinx_fpga_read,
    .llseek = xilinx_fpga_seek,
    .write = xilinx_fpga_write,
    .unlocked_ioctl = xilinx_fpga_ioctl,
    .compat_ioctl = xilinx_fpga_ioctl,
    .release = xilinx_fpga_release,
};

static struct miscdevice fpga_misc_device =
{
    FPGA_MINOR,
    FPGA_DEV_FILE_NAME,
    &xilinx_ops,
};

static int xilinx_fpga_probe(struct pci_dev *pdev, const struct pci_device_id *ent)
{
    int rc = -EFAULT;
    resource_size_t pciaddr;

    dev_info(&pdev->dev, "In xilinx_fpga_probe()\n");

    rc = pci_enable_device(pdev);
    if (rc) {
        dev_err(&pdev->dev, "Fail to enable pci device\n");
        goto err;
    }
    gDev = pdev;
    rc = pci_request_regions(pdev, DRV_NAME);
    if (rc) {
        dev_err(&pdev->dev, "Fail to request regions\n");
        goto err_disable;
    }

    pciaddr = pci_resource_start(pdev, 0);
    if (!pciaddr) {
        rc = -EIO;
        dev_err(&pdev->dev, "no MMIO resource\n");
        goto err_release_regions;
    }

    gBaseVirt = ioremap(pciaddr, FPGA_ADD_LEN);
    if (!gBaseVirt) {
        rc = -EIO;
        dev_err(&pdev->dev, "Cannot map PCI MMIO\n");
        goto err_release_regions;
    }

    /* add for msi*/
    nl_sk = netlink_kernel_create(&init_net, MYPROTO, NULL);
    if (!nl_sk) {
        pr_err("Error creating socket.\n");
        return -10;
    }

    if (pci_enable_msi(pdev) != 0) {
        printk("%s: pci_enable_msi error\n", FPGA_DEV_FILE_NAME);
    }
    
    gIrq = pdev->irq;
    printk("%s: Init: Device IRQ: %X, gBaseVirt: %p\n", FPGA_DEV_FILE_NAME, gIrq, gBaseVirt);

    printk("%s: ISR Setup..\n", FPGA_DEV_FILE_NAME);
    if (0 > request_irq(gIrq, &xilinx_fpga_irqhandle, 0, FPGA_DEV_FILE_NAME, gDev)) {
        printk("%s: Init: Unable to allocate IRQ",FPGA_DEV_FILE_NAME);
        goto err_release_regions;
    }
    
    gStatFlags = 1;
 
    pci_set_master(pdev);
    misc_register(&fpga_misc_device);
    return 0;

err_release_regions:
    pci_release_regions(pdev);
err_disable:
    pci_disable_device(pdev);
err:
    return rc;
}

static void xilinx_fpga_remove(struct pci_dev *pdev)
{
    if (1 == gStatFlags) {
        (void) free_irq(gIrq, gDev);
        gStatFlags = 0;
    }
    pci_disable_msi(pdev);

    pci_release_regions(pdev);

    pci_disable_device(pdev);

    iounmap(gBaseVirt);

    misc_deregister(&fpga_misc_device);
    dev_info(&pdev->dev, "xilinx_fpga_remove()\n");
    netlink_kernel_release(nl_sk);  
}

static struct pci_driver xilinx_fpga_driver = {
    .name = DRV_NAME,
    .id_table = xilinx_fpga_pci_tbl,
    .probe = xilinx_fpga_probe,
    .remove = xilinx_fpga_remove,
};

static int __init xilinx_fpga_init(void)
{
    return pci_register_driver(&xilinx_fpga_driver);
}

static void __exit xilinx_fpga_exit(void)
{
    return pci_unregister_driver(&xilinx_fpga_driver);
}

module_init(xilinx_fpga_init);
module_exit(xilinx_fpga_exit);

MODULE_AUTHOR("Jia Guo <jiag@oplink.com.cn>");
MODULE_DESCRIPTION("xilinx fpga pcie driver");
MODULE_LICENSE("GPL");
