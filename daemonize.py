#!/usr/bin/env python
#encoding=utf-8

import sys, os, time
from signal import SIGINT,SIGTERM,SIGKILL
 
def daemonize(stdout='/dev/null', stderr=None, stdin='/dev/null',
              pidfile=None, startmsg = 'started with pid %s' ):
    '''
        This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        These arguments are optional and default to /dev/null.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.
    '''
 
    # flush io
    sys.stdout.flush()
    sys.stderr.flush()
 
    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
 
    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()
 
    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0) # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
 
    # Open file descriptors and print start message
    if not stderr: stderr = stdout
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)  #unbuffered
    pid = str(os.getpid())
    sys.stderr.write("\n%s\n" % startmsg % pid)
    sys.stderr.flush()
    if pidfile: file(pidfile,'w+').write("%s\n" % pid)
 
    # Redirect standard file descriptors.
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    return

class DaemonizeError(Exception): pass

def startstop(stdout='/dev/null', stderr=None, stdin='/dev/null',
              pidfile='pid.txt', startmsg = 'started with pid %s', action=None ):
 
    if not action and len(sys.argv) > 1:
        action = sys.argv[1]
 
    if action:
        try:
            pf  = file(pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if 'stop' == action or 'restart' == action:
            if not pid:
                mess = "Could not stop, pid file '%s' missing.\n"
                raise DaemonizeError(mess % pidfile)
            try:
               while 1:
                   print "sending SIGINT to",pid
                   os.kill(pid,SIGINT)
                   time.sleep(2)
                   print "sending SIGTERM to",pid
                   os.kill(pid,SIGTERM)
                   time.sleep(2)
                   print "sending SIGKILL to",pid
                   os.kill(pid,SIGKILL)
                   time.sleep(1)
            except OSError, err:
               print "process has been terminated."
               os.remove(pidfile)
               if 'stop' == action:
                   return    ## sys.exit(0)
               action = 'start'
               pid = None
        if 'start' == action:
            if pid:
                print "pid file '%s' exists. Server still running with new pid.\n"
                #raise DaemonizeError(mess % pidfile)
            daemonize(stdout,stderr,stdin,pidfile,startmsg)
            return
    print "usage: %s start|stop|restart" % sys.argv[0]
    raise DaemonizeError("invalid command")

def test():
    '''
        This is an example main function run by the daemon.
        This prints a count and timestamp once per second.
    '''
    sys.stdout.write ('Message to stdout...\n')
    sys.stderr.write ('Message to stderr...\n')
    c = 0
    while 1:
        #sys.stdout.write ('%d: %s\n' % (c, time.ctime(time.time())) )
        #sys.stdout.flush()
        cl = '/home/sem5000/evoc_wdt-master/evoc_wdt 60'
        os.system(cl)
        c = c + 1
        time.sleep(10)
 
if __name__ == "__main__":
    startstop(stdout='/tmp/sem5000_monitor.log',
              pidfile='/tmp/sem5000_monitor.pid')
    if sys.argv[1]in ('start', 'restart'):
        test()
