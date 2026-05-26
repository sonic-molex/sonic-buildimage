# SONIC ocs-molex Demo Instructions

This doc contains the procedure to compile, run and test the SONiC-OCS image, the prototype the team currently has.  
For SONiC compilation environment setup, please refer to [sonic-buildimage](https://github.com/sonic-net/sonic-buildimage) and [README.md](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)

# HOWTO Build ocs-molex image

``` bash
make init
make configure PLATFORM=ocs-molex
make BLDENV=bookworm SONIC_BUILD_JOBS=8 SONIC_OVERRIDE_BUILD_VARS=' INCLUDE_EXTERNAL_PATCHES=y ' target/sonic-ocs-molex.bin
```

# HOWTO Install ONIE
## Download ONIE
Download ONIE image directly from [onie-images](https://github.com/sonic-molex/onie/tree/2022.08br/build/images)

```bash
wget https://raw.githubusercontent.com/sonic-molex/onie/refs/heads/2022.08br/build/images/onie-recovery-x86_64-ocs-molex_16x16-r0.iso
```

## Burn ONIE image to disk
Insert USB image burning tool with msata disk to a linux server. Suppose the disk is sdb.

For more details about ONIE, please visit [ONIE](https://opencomputeproject.github.io/onie/)

```bash
lum@ubuntu:~$ cd ~/share/sonic
lum@ubuntu:~/share/sonic$ ll
total 863724
drwxrwxr-x 2 lum lum      4096  8月  2 03:36 ./
drwxrwxr-x 3 lum lum      4096  8月  2 00:47 ../
-rw-r--r-- 1 lum lum  28377088  8月  2 00:47 onie-recovery-x86_64-ocs-molex_16x16-r0.iso
-rwxr-xr-x 1 lum lum 854478830  8月  2 08:29 sonic-ocs-molex.bin*
lum@ubuntu:~/share/sonic$ 
lum@ubuntu:~/share/sonic$ dd if=onie-recovery-x86_64-ocs-molex_16x16-r0.iso of=/dev/sdb bs=1M
```

## Install ONIE to device

Need to enable UEFI in BIOS, and set 1st boot option to msata disk first.
```
                             GNU GRUB  version 2.04

 /----------------------------------------------------------------------------\
 | ONIE: Rescue                                                               | 
 |*ONIE: Embed ONIE                                                           |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            | 
 \----------------------------------------------------------------------------/

      Use the ^ and v keys to select which entry is highlighted.          
      Press enter to boot the selected OS, `e' to edit the commands       
      before booting or `c' for a command-line. ESC to return previous    
      menu.   

```

Select `ONIE: Embed ONIE` option to install ONIE to device. The device will be restarted automatically after installation. And the grub menu will be changed displayed as follows:
```
                            GNU GRUB  version 2.04

 +----------------------------------------------------------------------------+
 |*ONIE: Install OS                                                           | 
 | ONIE: Rescue                                                               |
 | ONIE: Uninstall OS                                                         |
 | ONIE: Update ONIE                                                          |
 | ONIE: Embed ONIE                                                           |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            | 
 +----------------------------------------------------------------------------+

      Use the ^ and v keys to select which entry is highlighted.          
      Press enter to boot the selected OS, `e' to edit the commands       
      before booting or `c' for a command-line.
```

# HOWTO Install SONiC OCS image
For all network installation scenarios, ONIE expects the NOS installer image to be available on the network via HTTP.

Before installation, the device must connect to network and pingable to HTTP server.

## Start HTTP Server
It's very easy to use mongoose  to start a HTTP server. After that just copy SONIC OCS image to HTTP share folder directly.

```bash
um@ubuntu:~/share/sonic$ ls
http-server  onie-recovery-x86_64-ocs-molex_16x16-r0.iso  sonic-ocs-molex.bin
lum@ubuntu:~/share/sonic$ 
lum@ubuntu:~/share/sonic$ ./http-server 
7a0367b7 2 main.c:175:main              Mongoose version : v7.17
7a0367b7 2 main.c:176:main              HTTP listener    : http://0.0.0.0:8000
7a0367b7 2 main.c:177:main              HTTPS listener   : https://0.0.0.0:8443
7a0367b7 2 main.c:178:main              Web root         : [/mnt/sda/lum/share/sonic]
7a0367b7 2 main.c:179:main              Upload dir       : [unset]
```

## Enter ONIE OS Install Mode
Select `ONIE: Install OS` option enter OS install mode.

```bash
                             GNU GRUB  version 2.04

 +----------------------------------------------------------------------------+
 |*ONIE: Install OS                                                           | 
 | ONIE: Rescue                                                               |
 | ONIE: Uninstall OS                                                         |
 | ONIE: Update ONIE                                                          |
 | ONIE: Embed ONIE                                                           |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            | 
 +----------------------------------------------------------------------------+

      Use the ^ and v keys to select which entry is highlighted.          
      Press enter to boot the selected OS, `e' to edit the commands       
      before booting or `c' for a command-line.                           
   The highlighted entry will be executed automatically in 0s.                 
  Booting `ONIE: Install OS'

ONIE: OS Install Mode ...
Platform  : x86_64-ocs-molex_16x16-r0
Version   : 2022.08
Build Date: 2025-07-31T16:47+08:00
error: no suitable video mode found.
Booting in blind mode
Info: Mounting kernel filesystems... done.
...
```

## Stop NOS Auto Discover
Wait for 3-5 minute for ONIE setup, input `onie-discover-stop` command to stop NOS automatically discovery when you see `Starting: discover... done.`.

```bash
discover: installer mode detected.  Running installer.
Starting: discover... done.

Please press Enter to activate this console. Info: eth0:  Checking link... down.
ONIE: eth0: link down.  Skipping configuration.
ONIE: Failed to configure eth0 interface
ONIE: Starting ONIE Service Discovery
Info: Attempting tftp://onie-server/00-30-64-34-a1-9b/onie-installer-x86_64-intel_coreboot_rangeley-r0 ...
Info: Attempting tftp://onie-server/onie-installer-x86_64-ocs-molex_16x16-r0 ...
Info: Attempting tftp://onie-server/onie-installer-x86_64-ocs-molex_16x16-r0.bin ...
Info: Attempting tftp://onie-server/onie-installer-x86_64-ocs-molex_16x16 ...
Info: Attempting tftp://onie-server/onie-installer-x86_64-ocs-molex_16x16.bin ...
Info: Attempting tftp://onie-server/onie-installer-ocs-molex_16x16 ...
Info: Attempting tftp://onie-server/onie-installer-ocs-molex_16x16.bin ...
Info: Attempting tftp://onie-server/onie-installer-x86_64-none ...
Info: Attempting tftp://onie-server/onie-installer-x86_64-none.bin ...
Info: Attempting tftp://onie-server/onie-installer-x86_64 ...
Info: Attempting tftp://onie-server/onie-installer-x86_64.bin ...
Info: Attempting tftp://onie-server/onie-installer ...
Info: Attempting tftp://onie-server/onie-installer.bin ...
Info: Sleeping for 20 seconds 
...

onie-discover-stop

Stopping: discover... done.
```

## Install SONiC OCS image
Suppose HTTP server IP is 172.16.166.22. Use `onie-nos-install` command to install NOS.

```bash
onie-nos-install http://172.16.166.22:8000/sonic-ocs-molex.bin

ONIE: Executing installer: http://172.16.166.22:8000/sonic-ocs-molex.bin
...
Verifying image checksum ... OK.
[   26.094547] hrtimer: interrupt took 8161630 ns
Preparing image archive ... OK.
Installing SONiC in ONIE
ONIE Installer: platform: x86_64-ocs-molex_16x16-r0
onie_platform: x86_64-ocs-molex_16x16-r0
...
```

The device will be restarted automatically after installation. And the grub menu will be changed displayed as follows:

```bash
                             GNU GRUB  version 2.02

 +----------------------------------------------------------------------------+
 |*SONiC-OS-ocs.0-dirty-20250728.102930                                       | 
 | ONIE                                                                       |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            | 
 +----------------------------------------------------------------------------+

      Use the ^ and v keys to select which entry is highlighted.
      Press enter to boot the selected OS, `e' to edit the commands       
      before booting or `c' for a command-line.

                             GNU GRUB  version 2.02

...
[   19.256320] rc.local[630]: + onie_partition_type=gpt
[   19.320309] rc.local[630]: + onie_platform=x86_64-ocs-molex_16x16-r0
[   19.398101] rc.local[630]: + onie_root_dir=/mnt/onie-boot/onie
[   19.476439] rc.local[630]: + onie_skip_ethmgmt_macs=no
[   19.548327] rc.local[630]: + onie_switch_asic=none
[   19.608335] rc.local[630]: + onie_uefi_arch=x64
[   19.668351] rc.local[630]: + onie_uefi_boot_loader=grubx64.efi
[   19.744523] rc.local[630]: + onie_vendor_id=343
[   19.808025] rc.local[630]: + onie_version=2022.08-dirty
[   19.872361] rc.local[630]: + program_console_speed
[   19.939160] rc.local[647]: + cat /proc/cmdline
[   20.003982] rc.local[648]: + grep -Eo console=tty(S|AMA)[0-9]+,[0-9]+
[   20.088089] rc.local[651]: + cut -d , -f2
[   20.153119] rc.local[630]: + speed=9600
[   20.208308] rc.local[630]: + [ -z 9600 ]
[   20.256255] rc.local[630]: + CONSOLE_SPEED=9600
[   20.318338] rc.local[656]: + grep agetty /lib/systemd/system/serial-getty@.service
[   20.413882] rc.local[657]: + grep keep-baud
[   20.468313] rc.local[657]: ExecStart=-/sbin/agetty -o '-p -- \\u' --keep-baud 115200,57600,38400,9600 - $TERM
[FAILED] Failed to start determine-…eboot cause determination service.
[   20.597746] rc.local[630]: + [ 0 = 0 ]
[   20.760668] rc.local[630]: + sed -i s|\-\-keep\-baud .* %I| 9600 %I|g /lib/systemd/system/serial-getty@.service
[   20.888632] rc.local[630]: + systemctl daemon-reload
[   20.960357] rc.local[630]: + [ -f /host/image-ocs.0-dirty-20250801.142133/platform/firsttime ]
[   21.068316] rc.local[630]: + echo First boot detected. Performing first boot tasks...
[   21.164555] rc.local[630]: First boot detected. Performing first boot tasks...
[   21.256680] rc.local[630]: + [ -n  ]
[   21.300386] rc.local[630]: + [ -n x86_64-ocs-molex_16x16-r0 ]
[   21.376338] rc.local[630]: + platform=x86_64-ocs-molex_16x16-r0
[   21.452322] rc.local[630]: + [ -d /host/old_config ]
[   21.516286] rc.local[630]: + [ -f /host/minigraph.xml ]
[   21.588355] rc.local[630]: + [ -n  ]
[   21.632348] rc.local[630]: + touch /tmp/pending_config_initialization
[   21.720323] rc.local[630]: + touch /tmp/notify_firstboot_to_platform
[   21.808417] rc.local[630]: + [ ! -d /host/reboot-cause/platform ]
[   21.888320] rc.local[630]: + mkdir -p /host/reboot-cause/platform
[   21.964252] rc.local[630]: + [ -d /host/image-ocs.0-dirty-20250801.142133/platform/x86_64-ocs-molex_16x16-r0 ]
[   22.092322] rc.local[630]: + sync
[   22.136333] rc.local[630]: + [ -n x86_64-ocs-molex_16x16-r0 ]
[   22.212588] rc.local[630]: + [ -n  ]
[   22.256320] rc.local[630]: + mkdir -p /var/platform
[   22.320396] rc.local[630]: + [ -f /etc/default/kdump-tools ]
[   22.396388] rc.local[630]: + sed -i -e s/__PLATFORM__/x86_64-ocs-molex_16x16-r0/g /etc/default/kdump-tools
[   22.516336] rc.local[630]: + firsttime_exit
[   22.572326] rc.local[630]: + rm -rf /host/image-ocs.0-dirty-20250801.142133/platform/firsttime
[   22.680337] rc.local[630]: + exit 0

Debian GNU/Linux 12 sonic ttyS0

sonic login:
```

# HOWTO use SONiC OCS
## Login
Input user and password to login, which are configured in config file, admin/YourPaSsWoRd for default.
```
sonic login: admin
Password: 
Linux sonic 6.1.0-29-2-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.123-1 (2025-01-02) x86_64
You are on
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --

Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.

Help:    https://sonic-net.github.io/SONiC/

admin@sonic:~$ 
```

## Show PMON platform information
### Show summary information
```bash
Last login: Thu May 29 23:13:43 2025 from 172.16.161.114
admin@sonic:~$ show platform summary
Platform: x86_64-ocs-molex_16x16-r0
HwSKU: OCS
ASIC: ocs-molex
ASIC Count: 1
Serial Number: H3603928
Model Number: 1831800089
Hardware Revision: 1.01
Switch Type: ocs
admin@sonic:~$
```

### Show PSU information
```bash
admin@sonic:~$ show platform psu
PSU    Model          Serial               HW Rev      Voltage (V)    Current (A)    Power (W)  Status    LED
-----  -------------  -------------------  --------  -------------  -------------  -----------  --------  -----
PSU 1  G1251-0550WNJ  G1251551NJ240101384  R00               12.07           2.12        25.62  OK        green
PSU 2  G1251-0550WNJ  G1251551NJ240101388  R00               12.06           2.56        30.87  OK        green
admin@sonic:~$
```

### Show fan information
```bash
admin@sonic:~$ show platform fan
  Drawer    LED            FAN    Speed              Direction    Presence    Status          Timestamp
--------  -----  -------------  -------  ---------------------  ----------  --------  -----------------
FanTray0  green  FanTray0-Fan0     100%  FAN_DIRECTION_EXHAUST     Present        OK  20250530 02:55:06
FanTray0  green  FanTray0-Fan1     100%  FAN_DIRECTION_EXHAUST     Present        OK  20250530 02:55:06
FanTray0  green  FanTray0-Fan2     100%  FAN_DIRECTION_EXHAUST     Present        OK  20250530 02:55:06
FanTray0  green  FanTray0-Fan3      98%  FAN_DIRECTION_EXHAUST     Present        OK  20250530 02:55:06
     N/A  green       PSU0-Fan     100%   FAN_DIRECTION_INTAKE     Present        OK  20250530 02:55:06
     N/A  green       PSU1-Fan     100%   FAN_DIRECTION_INTAKE     Present        OK  20250530 02:55:06
admin@sonic:~$
```

### Show thermal information
```bash
admin@sonic:~$ show platform temperature
        Sensor    Temperature    High TH    Low TH    Crit High TH    Crit Low TH    Warning          Timestamp
--------------  -------------  ---------  --------  --------------  -------------  ---------  -----------------
  System Board              0         75        -5              70              0      False  20250530 02:56:06
System Exhaust              0         75        -5              70              0      False  20250530 02:56:06
admin@sonic:~$
```

### Show firmware information
```bash
admin@sonic:~$ show platform firmware status
Chassis    Module       Component    Version    Description
---------  -----------  -----------  ---------  -------------------------------------------------------------
OCS        LINE-CARD0   OCS0-0       N/A        Optical Circuit Switch of 16x16
           SUPERVISOR0  BIOS         5.6.5      Performs initialization of hardware components during booting
                        FPGA         0.04.0002  Platform managment controller for on-board components
                        CPLD         0.04.0001  Used for managing IO modules
                        ONIE         2022.08    Open network install environment
admin@sonic:~$
```

## Redis
We have added the following tables to support data of OCS. 
- For CONFIG_DB (DB 4)
  - OCS_PORT
  - OCS_CROSS_CONNECT
- For STATE_DB (DB 6)
  - OCS_PORT_TABLE
  - OCS_CROSS_CONNECT_TABLE

## CLI Support for OCS
We use SONiC CLI Auto-generation tool to support SONiC OCS CLI by ocs yang model. For more detail please refer to [SONiC CLI Auto-generation tool](https://github.com/sonic-net/SONiC/blob/master/doc/cli_auto_generation/cli_auto_generation.md)

### Generate OCS CLI command
```bash
sudo -i
root@sonic:~# sonic-cli-gen generate show sonic-ocs
INFO:sonic-cli-gen: Auto-generation successful! Location: /usr/local/lib/python3.11/dist-packages/show/plugins/auto/sonic-ocs_yang.py

root@sonic:~# sonic-cli-gen generate config sonic-ocs
INFO:sonic-cli-gen: Auto-generation successful! Location: /usr/local/lib/python3.11/dist-packages/config/plugins/auto/sonic-ocs_yang.py
```

### Features
- show ocs-port
- show ocs-port-table
- show ocs-cross-connect
- show ocs-cross-connect-table
- config ocs-port
- config ocs-cross-connect

### Show OCS port configuration
```bash
root@sonic:~# show ocs-port
SIMPLEX PORT ID    LABEL           CONFIG STATUS
-----------------  --------------  ---------------
1A                 ingress_port1   normal
1B                 egress_port1    normal
2A                 ingress_port2   normal
2B                 egress_port2    normal
3A                 ingress_port3   normal
3B                 egress_port3    normal
4A                 ingress_port4   normal
4B                 egress_port4    normal
5A                 ingress_port5   normal
5B                 egress_port5    normal
6A                 ingress_port6   normal
6B                 egress_port6    normal
7A                 ingress_port7   normal
7B                 egress_port7    normal
8A                 ingress_port8   normal
8B                 egress_port8    normal
9A                 ingress_port9   normal
9B                 egress_port9    normal
10A                ingress_port10  normal
10B                egress_port10   normal
11A                ingress_port11  normal
11B                egress_port11   normal
12A                ingress_port12  normal
12B                egress_port12   normal
13A                ingress_port13  normal
13B                egress_port13   normal
14A                ingress_port14  normal
14B                egress_port14   normal
15A                ingress_port15  normal
15B                egress_port15   normal
16A                ingress_port16  normal
16B                egress_port16   normal
root@sonic:~#
```

**Column descriptions:**

| Column | Description |
|--------|-------------|
| SIMPLEX PORT ID | Unique identifier for the port (e.g. `1A` for A-side port 1, `1B` for B-side port 1) |
| LABEL | User-facing label for cable tracing / LLDP-like neighbor identification (e.g. `ingress_port1`) |
| CONFIG STATUS | Configurable override status: `normal` (default, determined by cross-connect presence), `force_blocked` (port blocked regardless of cross-connect state), or `powered_off` (first optical element powered off) |

### Show OCS port state
```bash
root@sonic:~# show ocs-port-table 
SIMPLEX PORT ID    CONNECTOR TYPE      CONNECTOR PIN  TARGET SIMPLEX PORT ID    OPER STATUS
-----------------  ----------------  ---------------  ------------------------  -------------
1A                 Duplex LC                       0  16B                       connected
1B                 Duplex LC                       0  16A                       connected
2A                 Duplex LC                       0  15B                       connected
2B                 Duplex LC                       0  15A                       connected
3A                 Duplex LC                       0  14B                       connected
3B                 Duplex LC                       0  14A                       connected
4A                 Duplex LC                       0  13B                       connected
4B                 Duplex LC                       0  13A                       connected
5A                 Duplex LC                       0  12B                       connected
5B                 Duplex LC                       0  12A                       connected
6A                 Duplex LC                       0  11B                       connected
6B                 Duplex LC                       0  11A                       connected
7A                 Duplex LC                       0  10B                       connected
7B                 Duplex LC                       0  10A                       connected
8A                 Duplex LC                       0  9B                        connected
8B                 Duplex LC                       0  9A                        connected
9A                 Duplex LC                       0  8B                        connected
9B                 Duplex LC                       0  8A                        connected
10A                Duplex LC                       0  7B                        connected
10B                Duplex LC                       0  7A                        connected
11A                Duplex LC                       0  6B                        connected
11B                Duplex LC                       0  6A                        connected
12A                Duplex LC                       0  5B                        connected
12B                Duplex LC                       0  5A                        connected
13A                Duplex LC                       0  4B                        connected
13B                Duplex LC                       0  4A                        connected
14A                Duplex LC                       0  3B                        connected
14B                Duplex LC                       0  3A                        connected
15A                Duplex LC                       0  2B                        connected
15B                Duplex LC                       0  2A                        connected
16A                Duplex LC                       0  1B                        connected
16B                Duplex LC                       0  1A                        connected
root@sonic:~# 
```

**Column descriptions:**

| Column | Description |
|--------|-------------|
| SIMPLEX PORT ID | Unique identifier for the port |
| CONNECTOR TYPE | Physical connector type (e.g. `Duplex LC`, `MPO/MTP`) |
| CONNECTOR PIN | Position of the fiber strand in the connector |
| TARGET SIMPLEX PORT ID | The remote port this port is connected to via a cross-connect; reflects current cross-connect configuration state |
| OPER STATUS | Operational status: `blocked` (default, no active connection), `connected` (light path established, IL within 0.5 dB of target), `tuning` (IL > 0.5 dB of target, transient), `powered_off` (first optical element powered off), or `failed` (hardware failure) |

### Show OCS cross connect configuration
```bash
root@sonic:~# show ocs-cross-connect
CROSS CONNECT ID    A SIDE    B SIDE
------------------  --------  --------
1A-16B              1A        16B
2A-15B              2A        15B
3A-14B              3A        14B
4A-13B              4A        13B
5A-12B              5A        12B
6A-11B              6A        11B
7A-10B              7A        10B
8A-9B               8A        9B
9A-8B               9A        8B
10A-7B              10A       7B
11A-6B              11A       6B
12A-5B              12A       5B
13A-4B              13A       4B
14A-3B              14A       3B
15A-2B              15A       2B
16A-1B              16A       1B
root@sonic:~#
```

**Column descriptions:**

| Column | Description |
|--------|-------------|
| CROSS CONNECT ID | Unique identifier for the cross-connect (e.g. `1A-16B`) |
| A SIDE | A-side simplex port of the connection (e.g. `1A`). Port naming: `<n>A` for A-side, where n is 1–68. |
| B SIDE | B-side simplex port of the connection (e.g. `16B`). Port naming: `<n>B` for B-side, where n is 1–68. |

### Show OCS cross connect state
```bash
root@sonic:~# show ocs-cross-connect-table 
CROSS CONNECT ID    STATUS    PHYSICAL PATH
------------------  --------  --------------------------------
1A-16B              enabled   1A, panel IN 1, panel OUT 16, 16
2A-15B              enabled   2A, panel IN 2, panel OUT 15, 15
3A-14B              enabled   3A, panel IN 3, panel OUT 14, 14
4A-13B              enabled   4A, panel IN 4, panel OUT 13, 13
5A-12B              enabled   5A, panel IN 5, panel OUT 12, 12
6A-11B              enabled   6A, panel IN 6, panel OUT 11, 11
7A-10B              enabled   7A, panel IN 7, panel OUT 10, 10
8A-9B               enabled   8A, panel IN 8, panel OUT 9, 9B
9A-8B               enabled   9A, panel IN 9, panel OUT 8, 8B
10A-7B              enabled   10A, panel IN 10, panel OUT 7, 7
11A-6B              enabled   11A, panel IN 11, panel OUT 6, 6
12A-5B              enabled   12A, panel IN 12, panel OUT 5, 5
13A-4B              enabled   13A, panel IN 13, panel OUT 4, 4
14A-3B              enabled   14A, panel IN 14, panel OUT 3, 3
15A-2B              enabled   15A, panel IN 15, panel OUT 2, 2
16A-1B              enabled   16A, panel IN 16, panel OUT 1, 1
root@sonic:~# 
```

**Column descriptions:**

| Column | Description |
|--------|-------------|
| CROSS CONNECT ID | Unique identifier for the cross-connect (matches the provisioned key) |
| STATUS | Operational status: `enabled` (connection active, light path established), `disabled` (connection inactive — port blocked/powered off, or default/HAL error), or `invalid` (port conflict detected, connection cannot be established) |
| PHYSICAL PATH | Ordered sequence of elements in the physical light path, from the A-side simplex port through internal switch elements to the B-side simplex port (e.g. `1A, panel IN 1, panel OUT 16, 16B`) |

### Config OCS port
```bash
root@sonic:~# config ocs-port update 1A --config-status force_blocked
root@sonic:~# show ocs-port
SIMPLEX PORT ID    LABEL           CONFIG STATUS
-----------------  --------------  ---------------
1A                 ingress_port1   force_blocked
1B                 egress_port1    normal
2A                 ingress_port2   normal
2B                 egress_port2    normal
3A                 ingress_port3   normal
3B                 egress_port3    normal
4A                 ingress_port4   normal
4B                 egress_port4    normal
5A                 ingress_port5   normal
5B                 egress_port5    normal
6A                 ingress_port6   normal
6B                 egress_port6    normal
7A                 ingress_port7   normal
7B                 egress_port7    normal
8A                 ingress_port8   normal
8B                 egress_port8    normal
9A                 ingress_port9   normal
9B                 egress_port9    normal
10A                ingress_port10  normal
10B                egress_port10   normal
11A                ingress_port11  normal
11B                egress_port11   normal
12A                ingress_port12  normal
12B                egress_port12   normal
13A                ingress_port13  normal
13B                egress_port13   normal
14A                ingress_port14  normal
14B                egress_port14   normal
15A                ingress_port15  normal
15B                egress_port15   normal
16A                ingress_port16  normal
16B                egress_port16   normal
root@sonic:~#
root@sonic:~# show ocs-port-table
SIMPLEX PORT ID    CONNECTOR TYPE      CONNECTOR PIN  TARGET SIMPLEX PORT ID    OPER STATUS
-----------------  ----------------  ---------------  ------------------------  -------------
1A                 Duplex LC                       0  16B                       blocked
1B                 Duplex LC                       0  16A                       connected
2A                 Duplex LC                       0  15B                       connected
2B                 Duplex LC                       0  15A                       connected
3A                 Duplex LC                       0  14B                       connected
3B                 Duplex LC                       0  14A                       connected
4A                 Duplex LC                       0  13B                       connected
4B                 Duplex LC                       0  13A                       connected
5A                 Duplex LC                       0  12B                       connected
5B                 Duplex LC                       0  12A                       connected
6A                 Duplex LC                       0  11B                       connected
6B                 Duplex LC                       0  11A                       connected
7A                 Duplex LC                       0  10B                       connected
7B                 Duplex LC                       0  10A                       connected
8A                 Duplex LC                       0  9B                        connected
8B                 Duplex LC                       0  9A                        connected
9A                 Duplex LC                       0  8B                        connected
9B                 Duplex LC                       0  8A                        connected
10A                Duplex LC                       0  7B                        connected
10B                Duplex LC                       0  7A                        connected
11A                Duplex LC                       0  6B                        connected
11B                Duplex LC                       0  6A                        connected
12A                Duplex LC                       0  5B                        connected
12B                Duplex LC                       0  5A                        connected
13A                Duplex LC                       0  4B                        connected
13B                Duplex LC                       0  4A                        connected
14A                Duplex LC                       0  3B                        connected
14B                Duplex LC                       0  3A                        connected
15A                Duplex LC                       0  2B                        connected
15B                Duplex LC                       0  2A                        connected
16A                Duplex LC                       0  1B                        connected
16B                Duplex LC                       0  1A                        connected
root@sonic:~# 
```

### Config OCS cross connect
```bash
root@sonic:~# config ocs-cross-connect delete 1A-16B
root@sonic:~# show ocs-cross-connect
CROSS CONNECT ID    A SIDE    B SIDE
------------------  --------  --------
2A-15B              2A        15B
3A-14B              3A        14B
4A-13B              4A        13B
5A-12B              5A        12B
6A-11B              6A        11B
7A-10B              7A        10B
8A-9B               8A        9B
9A-8B               9A        8B
10A-7B              10A       7B
11A-6B              11A       6B
12A-5B              12A       5B
13A-4B              13A       4B
14A-3B              14A       3B
15A-2B              15A       2B
16A-1B              16A       1B
root@sonic:~# show ocs-cross-connect-table 
CROSS CONNECT ID    STATUS    PHYSICAL PATH
------------------  --------  --------------------------------
2A-15B              enabled   2A, panel IN 2, panel OUT 15, 15
3A-14B              enabled   3A, panel IN 3, panel OUT 14, 14
4A-13B              enabled   4A, panel IN 4, panel OUT 13, 13
5A-12B              enabled   5A, panel IN 5, panel OUT 12, 12
6A-11B              enabled   6A, panel IN 6, panel OUT 11, 11
7A-10B              enabled   7A, panel IN 7, panel OUT 10, 10
8A-9B               enabled   8A, panel IN 8, panel OUT 9, 9B
9A-8B               enabled   9A, panel IN 9, panel OUT 8, 8B
10A-7B              enabled   10A, panel IN 10, panel OUT 7, 7
11A-6B              enabled   11A, panel IN 11, panel OUT 6, 6
12A-5B              enabled   12A, panel IN 12, panel OUT 5, 5
13A-4B              enabled   13A, panel IN 13, panel OUT 4, 4
14A-3B              enabled   14A, panel IN 14, panel OUT 3, 3
15A-2B              enabled   15A, panel IN 15, panel OUT 2, 2
16A-1B              enabled   16A, panel IN 16, panel OUT 1, 1
root@sonic:~#
root@sonic:~# config ocs-cross-connect add 1A-16B --a-side 1A --b-side 16B
root@sonic:~# show ocs-cross-connect
CROSS CONNECT ID    A SIDE    B SIDE
------------------  --------  --------
1A-16B              1A        16B
2A-15B              2A        15B
3A-14B              3A        14B
4A-13B              4A        13B
5A-12B              5A        12B
6A-11B              6A        11B
7A-10B              7A        10B
8A-9B               8A        9B
9A-8B               9A        8B
10A-7B              10A       7B
11A-6B              11A       6B
12A-5B              12A       5B
13A-4B              13A       4B
14A-3B              14A       3B
15A-2B              15A       2B
16A-1B              16A       1B
root@sonic:~# show ocs-cross-connect-table 
CROSS CONNECT ID    STATUS    PHYSICAL PATH
------------------  --------  --------------------------------
1A-16B              enabled   1A, panel IN 1, panel OUT 16, 16
2A-15B              enabled   2A, panel IN 2, panel OUT 15, 15
3A-14B              enabled   3A, panel IN 3, panel OUT 14, 14
4A-13B              enabled   4A, panel IN 4, panel OUT 13, 13
5A-12B              enabled   5A, panel IN 5, panel OUT 12, 12
6A-11B              enabled   6A, panel IN 6, panel OUT 11, 11
7A-10B              enabled   7A, panel IN 7, panel OUT 10, 10
8A-9B               enabled   8A, panel IN 8, panel OUT 9, 9B
9A-8B               enabled   9A, panel IN 9, panel OUT 8, 8B
10A-7B              enabled   10A, panel IN 10, panel OUT 7, 7
11A-6B              enabled   11A, panel IN 11, panel OUT 6, 6
12A-5B              enabled   12A, panel IN 12, panel OUT 5, 5
13A-4B              enabled   13A, panel IN 13, panel OUT 4, 4
14A-3B              enabled   14A, panel IN 14, panel OUT 3, 3
15A-2B              enabled   15A, panel IN 15, panel OUT 2, 2
16A-1B              enabled   16A, panel IN 16, panel OUT 1, 1
root@sonic:~#
```


## REST API Support for OCS
REST API follows RESTCONF protocol

In ```sonic-mgmt-common```, REST APIs are generated from ```sonic-ocs.yang``` yang model.

### Show OCS port configuration
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_PORT" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2422  100  2422    0     0  89076      0 --:--:-- --:--:-- --:--:-- 89703
{
  "sonic-ocs:OCS_PORT": {
    "OCS_PORT_LIST": [
      {
        "config_status": "normal",
        "label": "ingress_port1",
        "simplex_port_id": "1A"
      },
      {
        "config_status": "normal",
        "label": "egress_port1",
        "simplex_port_id": "1B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port2",
        "simplex_port_id": "2A"
      },
      {
        "config_status": "normal",
        "label": "egress_port2",
        "simplex_port_id": "2B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port3",
        "simplex_port_id": "3A"
      },
      {
        "config_status": "normal",
        "label": "egress_port3",
        "simplex_port_id": "3B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port4",
        "simplex_port_id": "4A"
      },
      {
        "config_status": "normal",
        "label": "egress_port4",
        "simplex_port_id": "4B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port5",
        "simplex_port_id": "5A"
      },
      {
        "config_status": "normal",
        "label": "egress_port5",
        "simplex_port_id": "5B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port6",
        "simplex_port_id": "6A"
      },
      {
        "config_status": "normal",
        "label": "egress_port6",
        "simplex_port_id": "6B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port7",
        "simplex_port_id": "7A"
      },
      {
        "config_status": "normal",
        "label": "egress_port7",
        "simplex_port_id": "7B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port8",
        "simplex_port_id": "8A"
      },
      {
        "config_status": "normal",
        "label": "egress_port8",
        "simplex_port_id": "8B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port9",
        "simplex_port_id": "9A"
      },
      {
        "config_status": "normal",
        "label": "egress_port9",
        "simplex_port_id": "9B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port10",
        "simplex_port_id": "10A"
      },
      {
        "config_status": "normal",
        "label": "egress_port10",
        "simplex_port_id": "10B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port11",
        "simplex_port_id": "11A"
      },
      {
        "config_status": "normal",
        "label": "egress_port11",
        "simplex_port_id": "11B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port12",
        "simplex_port_id": "12A"
      },
      {
        "config_status": "normal",
        "label": "egress_port12",
        "simplex_port_id": "12B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port13",
        "simplex_port_id": "13A"
      },
      {
        "config_status": "normal",
        "label": "egress_port13",
        "simplex_port_id": "13B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port14",
        "simplex_port_id": "14A"
      },
      {
        "config_status": "normal",
        "label": "egress_port14",
        "simplex_port_id": "14B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port15",
        "simplex_port_id": "15A"
      },
      {
        "config_status": "normal",
        "label": "egress_port15",
        "simplex_port_id": "15B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port16",
        "simplex_port_id": "16A"
      },
      {
        "config_status": "normal",
        "label": "egress_port16",
        "simplex_port_id": "16B"
      }
    ]
  }
}
admin@sonic:~$
```

### Show OCS port state
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_PORT_TABLE" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  4236    0  4236    0     0   173k      0 --:--:-- --:--:-- --:--:--  179k
{
  "sonic-ocs:OCS_PORT_TABLE": {
    "OCS_PORT_LIST": [
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "1A",
        "target_simplex_port_id": "16B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "1B",
        "target_simplex_port_id": "16A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "2A",
        "target_simplex_port_id": "15B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "2B",
        "target_simplex_port_id": "15A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "3A",
        "target_simplex_port_id": "14B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "3B",
        "target_simplex_port_id": "14A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "4A",
        "target_simplex_port_id": "13B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "4B",
        "target_simplex_port_id": "13A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "5A",
        "target_simplex_port_id": "12B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "5B",
        "target_simplex_port_id": "12A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "6A",
        "target_simplex_port_id": "11B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "6B",
        "target_simplex_port_id": "11A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "7A",
        "target_simplex_port_id": "10B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "7B",
        "target_simplex_port_id": "10A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "8A",
        "target_simplex_port_id": "9B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "8B",
        "target_simplex_port_id": "9A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "9A",
        "target_simplex_port_id": "8B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "9B",
        "target_simplex_port_id": "8A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "10A",
        "target_simplex_port_id": "7B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "10B",
        "target_simplex_port_id": "7A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "11A",
        "target_simplex_port_id": "6B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "11B",
        "target_simplex_port_id": "6A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "12A",
        "target_simplex_port_id": "5B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "12B",
        "target_simplex_port_id": "5A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "13A",
        "target_simplex_port_id": "4B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "13B",
        "target_simplex_port_id": "4A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "14A",
        "target_simplex_port_id": "3B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "14B",
        "target_simplex_port_id": "3A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "15A",
        "target_simplex_port_id": "2B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "15B",
        "target_simplex_port_id": "2A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "16A",
        "target_simplex_port_id": "1B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "16B",
        "target_simplex_port_id": "1A"
      }
    ]
  }
}
admin@sonic:~$
```

### Show OCS cross connect configuration 
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_CROSS_CONNECT" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   941  100   941    0     0  45181      0 --:--:-- --:--:-- --:--:-- 47050
{
  "sonic-ocs:OCS_CROSS_CONNECT": {
    "OCS_CROSS_CONNECT_LIST": [
      {
        "a_side": "2A",
        "b_side": "15B",
        "cross_connect_id": "2A-15B"
      },
      {
        "a_side": "3A",
        "b_side": "14B",
        "cross_connect_id": "3A-14B"
      },
      {
        "a_side": "4A",
        "b_side": "13B",
        "cross_connect_id": "4A-13B"
      },
      {
        "a_side": "5A",
        "b_side": "12B",
        "cross_connect_id": "5A-12B"
      },
      {
        "a_side": "6A",
        "b_side": "11B",
        "cross_connect_id": "6A-11B"
      },
      {
        "a_side": "7A",
        "b_side": "10B",
        "cross_connect_id": "7A-10B"
      },
      {
        "a_side": "8A",
        "b_side": "9B",
        "cross_connect_id": "8A-9B"
      },
      {
        "a_side": "9A",
        "b_side": "8B",
        "cross_connect_id": "9A-8B"
      },
      {
        "a_side": "10A",
        "b_side": "7B",
        "cross_connect_id": "10A-7B"
      },
      {
        "a_side": "11A",
        "b_side": "6B",
        "cross_connect_id": "11A-6B"
      },
      {
        "a_side": "12A",
        "b_side": "5B",
        "cross_connect_id": "12A-5B"
      },
      {
        "a_side": "13A",
        "b_side": "4B",
        "cross_connect_id": "13A-4B"
      },
      {
        "a_side": "14A",
        "b_side": "3B",
        "cross_connect_id": "14A-3B"
      },
      {
        "a_side": "15A",
        "b_side": "2B",
        "cross_connect_id": "15A-2B"
      },
      {
        "a_side": "16A",
        "b_side": "1B",
        "cross_connect_id": "16A-1B"
      }
    ]
  }
}
admin@sonic:~$
```


### Show OCS cross connect state 
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_CROSS_CONNECT_TABLE" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   848  100   848    0     0  39535      0 --:--:-- --:--:-- --:--:-- 40380
{
  "sonic-ocs:OCS_CROSS_CONNECT_TABLE": {
    "OCS_CROSS_CONNECT_LIST": [
      {
        "cross_connect_id": "2A-15B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "3A-14B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "4A-13B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "5A-12B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "6A-11B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "7A-10B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "8A-9B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "9A-8B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "10A-7B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "11A-6B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "12A-5B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "13A-4B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "14A-3B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "15A-2B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "16A-1B",
        "status": "enabled"
      }
    ]
  }
}
admin@sonic:~$
```

### Add OCS cross connect (REST API, single entry)

Use **PATCH** on the `OCS_CROSS_CONNECT` container to add one entry. The server merges it (adds if new, silently updates if key already exists).

```bash
curl -k -X PATCH "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_CROSS_CONNECT" \
  -H "Content-Type: application/yang-data+json" \
  -H "accept: application/yang-data+json" \
  -d '{
    "sonic-ocs:OCS_CROSS_CONNECT": {
      "OCS_CROSS_CONNECT_LIST": [
        { "cross_connect_id": "8A-61B", "a_side": "8A", "b_side": "61B" }
      ]
    }
  }' -w "\nHTTP code: %{http_code}\n"
```

- Success: HTTP 204. Verify with `show ocs-cross-connect-table`.

### Delete single OCS cross connect (REST API)

**DELETE** one list entry by key (`cross_connect_id`):

```bash
curl -k -X DELETE "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_CROSS_CONNECT/OCS_CROSS_CONNECT_LIST=8A-9B" \
  -H "accept: application/yang-data+json" -w "\nHTTP code: %{http_code}\n"
```

- Success: HTTP 200 or 204. Verify with `show ocs-cross-connect-table`.

### Bulk update OCS cross connects (REST API — `bulk-update` RPC)

The `bulk-update` RPC supports bulk delete, bulk add, or both in a single atomic request. All deletes execute before adds within one CONFIG_DB transaction. The response reports counts and any failed keys.

> **Initial state for all cases below:** 68 cross-connects in full-mesh configuration: `1A-68B`, `2A-67B`, ... `68A-1B` (port *i*A connected to port *(69−i)*B). All connections should be `enabled`. Restore to this state before running each case. Use `show ocs-cross-connect-table` to verify.

**Endpoint:** `POST /restconf/operations/sonic-ocs:bulk-update`

**Request body fields:**
- `delete` (optional): list of `cross_connect_id` keys to delete
- `add` (optional): list of entries to add (each with `cross_connect_id`, `a_side`, `b_side`)

**Response fields:**
- `deleted_count`: number of entries deleted
- `added_count`: number of entries added
- `failed_keys` (if any): keys that failed to process

#### Case 1: Bulk add only (new keys, no port conflicts)

Add entries whose keys don't exist and whose ports are not used by existing connections.

```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "add": [
        { "cross_connect_id": "1A-68B", "a_side": "1A", "b_side": "68B" },
        { "cross_connect_id": "2A-67B", "a_side": "2A", "b_side": "67B" },
        { "cross_connect_id": "3A-66B", "a_side": "3A", "b_side": "66B" }
      ]
    }
  }'
```

**Expected response:**
```json
{"sonic-ocs:output":{"deleted_count":0,"added_count":3}}
```

All three entries are created and become `enabled` on hardware.

#### Case 2: Bulk delete only

Delete entries by key. Non-existent keys are silently skipped.

```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "delete": ["1A-68B", "2A-67B", "3A-66B"]
    }
  }'
```

**Expected response:**
```json
{"sonic-ocs:output":{"deleted_count":3,"added_count":0}}
```

#### Case 3: Delete and add (reconfigure — new keys, no port conflicts)

Typical use case: reconfigure all connections. Deletes free up ports, adds claim them.

```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "delete": ["1A-68B", "2A-67B"],
      "add": [
        { "cross_connect_id": "1A-1B", "a_side": "1A", "b_side": "1B" },
        { "cross_connect_id": "2A-2B", "a_side": "2A", "b_side": "2B" }
      ]
    }
  }'
```

**Expected response:**
```json
{"sonic-ocs:output":{"deleted_count":2,"added_count":2}}
```

Deletes execute first (freeing ports 1A, 68B, 2A, 67B), then adds claim the freed ports. Both new entries become `enabled`.

#### Case 4: Bulk add, new keys, port conflicts (forced-add)

When adding **2 or more** entries whose keys are new but whose ports conflict with existing connections, **forced-add** semantics apply: new connections take priority, and conflicting existing connections are marked `invalid`. No pre-delete is required — just add on top.

**Example:** Add `1A-1B` and `2A-2B` directly. Port 1A is already used by `1A-68B`, port 2A by `2A-67B`. Both new entries conflict.

```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "add": [
        { "cross_connect_id": "1A-1B", "a_side": "1A", "b_side": "1B" },
        { "cross_connect_id": "2A-2B", "a_side": "2A", "b_side": "2B" }
      ]
    }
  }'
```

**Expected response:** `{"sonic-ocs:output":{"deleted_count":0,"added_count":2}}`

**Expected state (verify with `show ocs-cross-connect-table`):**
- `1A-1B` → **enabled** (new, took over port 1A from 1A-68B)
- `2A-2B` → **enabled** (new, took over port 2A from 2A-67B)
- `1A-68B` → **invalid** (existing, lost port 1A; port 68B parked)
- `2A-67B` → **invalid** (existing, lost port 2A; port 67B parked)
- Total entries = 70 (68 original + 2 new; the 2 invalidated ones still exist)

Invalidated connections stay `invalid` permanently until explicitly deleted and re-added. To restore, delete both old and new, then re-add originals:
```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{"sonic-ocs:input":{"delete":["1A-1B","2A-2B","1A-68B","2A-67B"],"add":[{"cross_connect_id":"1A-68B","a_side":"1A","b_side":"68B"},{"cross_connect_id":"2A-67B","a_side":"2A","b_side":"67B"}]}}'
```

#### Case 5: Single add, new key, port conflict (no forced-add)

When adding exactly **1** entry whose key is new but whose port conflicts with an existing connection, the **new** connection is marked `invalid` and the existing one is unchanged. This is the opposite of the multi-entry behavior (Case 4) because single-entry adds use the singular SAI API which does not support forced-add.

```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "add": [
        { "cross_connect_id": "1A-1B", "a_side": "1A", "b_side": "1B" }
      ]
    }
  }'
```

**Expected response:** `{"sonic-ocs:output":{"deleted_count":0,"added_count":1}}`

**Expected state:**
- `1A-1B` → **invalid** (new connection rejected due to port conflict on 1A)
- `1A-68B` → **enabled** (existing connection unchanged)
- Total entries = 69 (the invalid entry still exists)

To clean up, delete the invalid entry:
```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{"sonic-ocs:input":{"delete":["1A-1B"]}}'
```

To force the new connection to take over instead, include at least 2 entries in the add list (triggers the bulk SAI path with forced-add).

#### Case 6: Bulk add, existing keys, no port conflict (silently skipped)

When adding entries whose `cross_connect_id` keys already exist in the system, orchagent routes them to the update path instead of the create path. The update path does **not** trigger forced-add, does **not** flush hardware, and cannot change an `invalid` connection back to `enabled`. The entries are effectively skipped silently at the hardware level, regardless of whether there is a port conflict.

This applies to both single and bulk adds with existing keys.

```bash
# All three keys already exist with the same port assignments
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "add": [
        { "cross_connect_id": "1A-68B", "a_side": "1A", "b_side": "68B" },
        { "cross_connect_id": "2A-67B", "a_side": "2A", "b_side": "67B" },
        { "cross_connect_id": "3A-66B", "a_side": "3A", "b_side": "66B" }
      ]
    }
  }'
```

**Expected response:** `{"sonic-ocs:output":{"deleted_count":0,"added_count":3}}`

**Expected state:**
- Response shows `added_count: 3` (CONFIG_DB accepted the writes)
- But hardware state does not change — orchagent sees all three keys already exist in its internal map and routes to update, not create
- `show ocs-cross-connect-table` shows all 68 entries still `enabled`, unchanged

This is true even if you change `a_side`/`b_side` in the add — orchagent still routes existing keys to the update path which does not reconfigure hardware.

**This also applies to `invalid` entries.** After a forced-add (Case 4), the old connections are marked `invalid` but their keys still exist in orchagent's internal map. Re-adding those same keys does **not** restore them to `enabled` — the update path cannot change `invalid` back to `enabled` or trigger a hardware flush. For example, after Case 4 leaves `1A-68B` as `invalid`, adding `1A-68B` again is silently skipped:

```bash
# 1A-68B is currently invalid (from a prior forced-add)
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "add": [
        { "cross_connect_id": "1A-68B", "a_side": "1A", "b_side": "68B" }
      ]
    }
  }'
```

**Expected:** `added_count: 1` in the response, but `1A-68B` stays `invalid` on hardware.

**Workaround:** To reconfigure entries with the same key names (whether `enabled` or `invalid`), include both `delete` and `add` in one request. Deletes execute first, clearing the internal key map. The subsequent adds then go through the create path normally:

```bash
curl -sk -X POST "https://localhost/restconf/operations/sonic-ocs:bulk-update" \
  -H "Content-Type: application/yang-data+json" \
  -d '{
    "sonic-ocs:input": {
      "delete": ["1A-68B", "2A-67B", "3A-66B"],
      "add": [
        { "cross_connect_id": "1A-68B", "a_side": "1A", "b_side": "68B" },
        { "cross_connect_id": "2A-67B", "a_side": "2A", "b_side": "67B" },
        { "cross_connect_id": "3A-66B", "a_side": "3A", "b_side": "66B" }
      ]
    }
  }'
```

#### Summary of conflict behavior

| Scenario | Add count | Keys exist? | Port conflict? | New entry status | Existing entry status |
|----------|-----------|-------------|----------------|------------------|-----------------------|
| New keys, no conflict | any | no | no | enabled | unchanged |
| New key, port conflict | 1 | no | yes | **invalid** | unchanged (enabled) |
| New keys, port conflict | 2+ | no | yes | **enabled** (forced-add) | **invalid** |
| Existing keys (enabled) | any | yes (enabled) | n/a | silently skipped (no HW change) | unchanged (enabled) |
| Existing keys (invalid) | any | yes (invalid) | n/a | silently skipped (stays invalid) | unchanged (invalid) |
| Existing keys, port conflict | any | yes | yes | silently skipped (no HW change) | unchanged |
| Delete + add same key | any | yes→no | n/a | enabled (fresh create) | deleted first |
