#!/usr/bin/env python
#encoding=utf-8

import sys,os,time
from daemonize import startstop

wdt_cmd_line = '/opt/sem5000_monitor/evoc_wdt %d'

def main_routine():
    ''' 守护进程的主操作函数 '''
    c = 0
    lasttime = time.localtime().tm_hour
    # 等待10分钟，等待其他进程就绪
    #time.sleep(600)
    while 1:
        curtime = time.localtime().tm_hour
        # 暂每小时重启一次
        if curtime == lasttime:
            # 记录时间到stdout
            sys.stdout.write ('%d: %s' % (c, time.ctime(time.time())) )
            sys.stdout.flush()

            # 调用命令行，设置看门狗定时器超时时间
            cl = wdt_cmd_line % 60
            os.system(cl)
            sys.stdout.flush()
        else:
            sys.stdout.write ('Reboot now.\n')
            sys.stdout.flush()
            os.system('shutdown -r now')

        c = c + 1
        time.sleep(10)


def exit_clean():
    ''' 守护进程结束后调用本函数，做清理工作 '''
    cl = wdt_cmd_line % 0
    os.system(cl)
    sys.stdout.write('monitor exit.\n')

if __name__ == "__main__":
    # 
    startstop(stdout='/home/sem5000/sem5000_monitor.log', pidfile='/home/sem5000/sem5000_monitor.pid')
    if sys.argv[1] in ('start', 'restart'):
        main_routine()
    if sys.argv[1] in ('stop',):
        exit_clean()

