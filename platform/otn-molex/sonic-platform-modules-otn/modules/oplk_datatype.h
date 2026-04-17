/***MODU+*********************************************************************/
/* Copyright(C), 2015, OPLINK Tech.Co.,Ltd                                   */
/* FileName    : oplk_datatype.h                                             */
/* Description : The data type define.                                       */
/* History     :                                                             */
/*     [Author]   [Date]      [Version]    [Description]                     */
/* [1]    FeiTu   2015/04/22  Ver 1.0.0    Initial file.                     */
/***MODU-*********************************************************************/

#ifndef __OPLK_DATATYPE_H__
#define __OPLK_DATATYPE_H__

/***TYP+**********************************************************************/
/* Data type redefinition.                                                   */
/***DEF-**********************************************************************/
typedef float                 FLOAT;
typedef unsigned long         U64;
typedef long                  S64;
typedef unsigned int          *PDWORD, DWORD, ULONG, U32, UINT;
typedef int                   *PLONG, LONG, S32, INT;
typedef unsigned short        *PWORD, WORD, U16,USHORT;
typedef short                 S16, SHORT;
typedef unsigned char         *PBYTE, BYTE, U8, UCHAR, BOOL;
typedef char                  *PSCHAR, S8, CHAR;
typedef void                  VOID;

/***DEF+**********************************************************************/
/* define NULL UCHAR/USHORT/ULONG value                                      */
/***DEF-**********************************************************************/
#define NULL_BYTE            (0xFF)
#define NULL_WORD            (0xFFFF)
#define NULL_DWORD           (0xFFFFFFFF)

/***DEF+**********************************************************************/
/* define OK or ERR.                                                         */
/***DEF-**********************************************************************/
#define NULL_PTR             (0)
#define VAL_OK               (1)
#define VAL_ERR              (0)

#define NULL                 ((void *)0)

/***DEF+**********************************************************************/
/* Define max or min value.                                                  */
/***DEF-**********************************************************************/
#define MAX(a,b)                        ((a) > (b) ? (a) : (b))
#define MIN(a,b)                        ((a) < (b) ? (a) : (b))

/***DEF+**********************************************************************/
/* Kinetis is little endian ARCH,                                            */
/* Modify from the big-endian to little-endian                               */
/***DEF-**********************************************************************/
#define TRUE    (1==1)
#define FALSE   (!TRUE)


#define OK    (0)

/* error code */
#define ERR_GENERAL                (-1)
#define ERR_PARA                   (-2)
#define ERR_PARA_NUM               (-3)
#define ERR_FILE_CAN_NOT_CREATE    (-4)
#define ERR_UART_CAN_NOT_OPEN      (-5)
#define ERR_UART_CFG               (-6)
#define ERR_UART_OPEN              (-7)
#define ERR_UART_SET               (-8)
#define ERR_UART_RECV              (-9)
#define ERR_UART_SEND              (-10)
#define ERR_UART_PIN_CFG           (-11)
#define ERR_MEM_OPEN               (-12)
#define ERR_MEM_MAP                (-13)
#define ERR_IO_MEM_MAP             (-14)

#endif   /* __OPLK_DATATYPE_H__ */
