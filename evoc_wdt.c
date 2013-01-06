#include <sys/io.h>  
#include <unistd.h>  
#include <stdio.h>  
#include <stdlib.h>

#define INDEX_PORT 0x2e
#define DATA_PORT 0x2f

/* 初始化看门够定时器,成功返回0，失败返回-1 */
int InitWDT(void)
{
    /* 申请IO端口操作权限  */
    if (ioperm(INDEX_PORT, 2, 1) == -1) {
        printf("Port permission failed.\n");
        return -1;
    }

    /* 初始化WDT */
    outb(0x87, INDEX_PORT);
    outb(0x87, INDEX_PORT);
    outb(0x07, INDEX_PORT);
    outb(0x08, DATA_PORT);
    outb(0x30, INDEX_PORT);
    outb(0x01, DATA_PORT);
    
    return 0;
}

/* 设置看门狗定时器，timeout单位为秒，如超过240秒，内部除以60按分钟计算；最大值为15000； */
int SetWDT(int timeout)
{
    unsigned char val;

    if (timeout < 0) {
        printf("Wrong parameter timeout, must be 0~15000.");
        return -1;
    }

    /* 申请IO端口操作权限  */
    if (ioperm(INDEX_PORT, 2, 1) == -1) {
        printf("Port permission failed.\n");
        return -1;
    }
    
    /* 设置为超时复位模式 */
    outb(0x2d, INDEX_PORT);
    val = inb(DATA_PORT);
    val &= 0xfe;
    outb(val, DATA_PORT);
    
    /* 换算超时时间 */
    outb(0xf5, INDEX_PORT);
    if (timeout > 240) {  /* 分模式 */
        val = timeout/60;
        outb(0x08, DATA_PORT);
    }
    else {                /* 秒模式 */
        val = timeout;
        outb(0x00, DATA_PORT);
    }
    
    /* 设置超时时间，如果时间设置为0，则停止定时器 */
    outb(0xf6, INDEX_PORT);
    if (val == 0) {
        outb(0x00, DATA_PORT);
    }
    else {
        outb(val, DATA_PORT);
    }
}


int main()
{
    int retval = 0;
    if ((retval = InitWDT()) == 0) {
        retval = SetWDT(10);
    }
    return retval;
} 
