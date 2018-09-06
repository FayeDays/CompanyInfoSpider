# -*- coding: utf-8 -*-
#!DATE: 2018/7/19 14:57
#!@Author: yingying
#import sched
import time
import os
import threading
import sys

default_encoding = 'utf-8'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('C:\workspace\CompanyInfoSpider\CompanyInfoSpider\spiders')
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
def CNcompanyid():
    os.system("scrapy crawl CNCompanyID")
def SSEcompanyid():
    os.system("scrapy crawl SSECompanyID")
def UpdateCNSubAllInd():
    os.system("scrapy crawl CNUpdateInd")
def UpdateSSESubAllInd():
    os.system("scrapy crawl SSESubAllInd")


'''ReQuesTimea = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(time.time())).decode('utf-8')
ReQuesTimeb = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(time.time()-86400)).decode('utf-8')
ReQuesTimec = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(time.time()-8640)).decode('utf-8')

print ReQuesTimea, ReQuesTimeb, ReQuesTimec

if ReQuesTimea > ReQuesTimeb:
    print "ReQuesTimea>",ReQuesTimea
else:
    print "ReQuesTimeb>", ReQuesTimeb'''


starttime = time.time()
lasttime = starttime
while True:
    print starttime
    currenttime = time.time()
    time.sleep(1)
    if int(currenttime - starttime) > 86398 and int(currenttime - starttime) < 86404:
        t1 = threading.Thread(target=CNcompanyid)
        t1.start()
        t2 = threading.Thread(target=SSEcompanyid)
        t2.start()
        while t1.is_alive() == True or t2.is_alive() == True:
            time.sleep(1)
        starttime = time.time()
    print lasttime
    time.sleep(1)
    currenttime = time.time()
    print currenttime
    time.sleep(1)
    if int(currenttime - lasttime) > 298 and int(currenttime - lasttime) < 304:
        t3 = threading.Thread(target=UpdateCNSubAllInd)
        t3.start()
        t4 = threading.Thread(target=UpdateSSESubAllInd)
        t4.start()
        while t3.is_alive() == True or t4.is_alive() == True:
            time.sleep(1)
        lasttime = time.time()
    print "33333333333333333333333333"
    time.sleep(2)