#!/usr/bin/env python
#encoding=utf-8

from ctypes import *

path = '/home/wlx/projects/evoc_wdt'

wdt = cdll.LoadLibrary(path + '/evoc_wdt.so')

if wdt.InitWDT() == 0:
    wdt.SetWDT(0)
    wdt.SetWDT(-1)
