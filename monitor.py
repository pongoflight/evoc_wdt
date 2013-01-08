#!/usr/bin/env python
#encoding=utf-8

import sys,os,time
from daemonize import startstop

# 命令行：绝对路径/evoc_wdt d%
wdt_cmd_line = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'evoc_wdt %d')
# pid文件，日志文件路径
pid_file = '/home/sem5000/sem5000_monitor.pid'
log_file = '/home/sem5000/sem5000_monitor.log'

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


# 主入口函数
if __name__ == "__main__":
    # startstop函数处理start/stop/restart，其中start/restart将本进程daemon化，stop将发送KILL信号至已启动的进程；
    startstop(stdout=log_file, pidfile=pid_file)
    if sys.argv[1] in ('start', 'restart'):
        main_routine()
    if sys.argv[1] in ('stop',):
        exit_clean()

