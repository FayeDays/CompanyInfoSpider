# -*- coding: utf-8 -*-
#!DATE: 2018/7/19 14:57
#!@Author: yingying
import sys
import MySQLdb
from CompanyInfoSpider.spiders.SSE_UpdateSubIndex import SSESubUpdateIndexSpider
import time

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class SSEUpdateSqlPipeline(object):
    allQlist = []

    def open_spider(self, spider):
        #print "open_spider............................"
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456",db="cn_sse_crawl",charset="utf8")
        self.cursor = self.conn.cursor()

    def process_list(self):
        #print "process_list............................"
        SSESubAllList = SSESubUpdateIndexSpider()

        self.cursor.execute("select time from lastupdate where comp = 'sse'")
        self.conn.commit()
        lasttimelist = self.cursor.fetchall()
        lasttime = ''.join(str(lasttimelist))
        temptime = self.replacetime(SSESubAllList.ReQuesTimeList[0])
        updateprop = "update lastupdate set time = '%s' where comp = 'sse'" % (temptime)
        self.cursor.execute(updateprop)
        self.conn.commit()

        tableprop = "sse_askrep (name, askname, aques, atime, rques, rtime) values(%s, %s, %s, %s, %s, %s)"
        for index in range(len(SSESubAllList.AskTimeList)):
            tempint = 0
            currenttime = SSESubAllList.ReQuesTimeList[index]
            try:
                tempAskQuestionList = SSESubAllList.AskQuestionList[index]
                tempint = tempint + 1
                tempReplyQuesList = SSESubAllList.ReplyQuesList[index]
                tempint = tempint + 1

                if lasttime > currenttime:
                    break
                temptime = self.replacetime(SSESubAllList.ReQuesTimeList[index])
                self.allQlist.append([SSESubAllList.RepNameList[index], SSESubAllList.AskQuesNameList[index],
                                      tempAskQuestionList, SSESubAllList.AskTimeList[index],
                                      tempReplyQuesList, temptime])
            except:
                print "except>>>>>."
                if tempint == 1:
                    self.allQlist.append([SSESubAllList.RepNameList[index], SSESubAllList.AskQuesNameList[index],
                                          SSESubAllList.AskQuestionList[index], SSESubAllList.AskTimeList[index],
                                          "", SSESubAllList.ReQuesTimeList[index]])
            if len(self.allQlist) == 100:
                self.bulk_insert_to_mysql(self.allQlist, tableprop)
                del self.allQlist[:]
        self.bulk_insert_to_mysql(self.allQlist, tableprop)

    def replacetime(self, timestring):
        if timestring[1:4] == '分钟前':
            ReQuesTime = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
            tempmin = int(str(timestring[0]))
            temptime = ReQuesTime + ' ' + time.strftime('%H:%M', time.localtime(time.time() - 60 * tempmin))
            return temptime
        if timestring[2:5] == '分钟前':
            ReQuesTime = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
            tempmin = int(str(timestring[0:1]))
            temptime = ReQuesTime + ' ' + time.strftime('%H:%M', time.localtime(time.time() - 60 * tempmin))
            return temptime
        if timestring[1:4] == '小时前':
            ReQuesTime = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
            temph = int(str(timestring[0]))
            temptime = ReQuesTime + ' ' + time.strftime('%H:%M', time.localtime(time.time() - 3600 * temph))
            return temptime
        if timestring[2:5] == '小时前':
            ReQuesTime = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
            temph = int(str(timestring[0:1]))
            temptime = ReQuesTime + ' ' + time.strftime('%H:%M', time.localtime(time.time() - 3600 * temph))
            return temptime
        if timestring[0:1] == '昨天':
            ReQuesTime = time.strftime('%Y年%m月%d日', time.localtime(time.time() - 86400))
            temptime = timestring.replace('昨天', ReQuesTime)
            return temptime
        if len(timestring) < 13:
            ReQuesTime = time.strftime('%Y年', time.localtime(time.time()))
            temptime = ReQuesTime + timestring
            return temptime
        else:
            return timestring

    def bulk_insert_to_mysql(self, bulkdata, tableprop):
        try:
            sql = "insert into "+tableprop
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def close_spider(self, spider):
        #print "close_spider............................"
        self.process_list()
        del self.allQlist[:]
        self.conn.commit()
        self.cursor.close()
        self.conn.close()