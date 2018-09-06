# -*- coding: utf-8 -*-
#!DATE: 2018/7/19 14:57
#!@Author: yingying
import sys
import MySQLdb
from CompanyInfoSpider.spiders.SSE_SubIndex import SSESubIndexSpider
import time
import re

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class SSESubIndexSpiderSqlPipeline(object):
    allQlist = []

    def open_spider(self, spider):
        #print "open_spider............................"
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456",db="cn_sse_crawl",charset="utf8")
        self.cursor = self.conn.cursor()
        # 存入数据之前清空表：
        isexists = self.table_exists(self.cursor, "sse_askrep")
        if isexists == 1:
            self.cursor.execute("truncate table sse_askrep")
            self.conn.commit()
        else:
            self.cursor.execute("create table sse_askrep(name char(20) not null, askname char(30), aques text, atime char(30), rques text, rtime char(30))")
            self.conn.commit()
        isexists = self.table_exists(self.cursor, "lastupdate")
        if isexists == 0:
            self.cursor.execute("create table lastupdate(comp char(3) not null, time char(30) not null, primary key(comp))")
            self.conn.commit()
        else:
            self.cursor.execute("delete from lastupdate where comp = 'sse'")
            self.conn.commit()


    def table_exists(self, con, table_name):  # 这个函数用来判断表是否存在
        sql = "show tables;"
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0  # 不存在返回0

    def process_list(self):
        SSESubAllList = SSESubIndexSpider()

        updatetableprop = "lastupdate (comp, time) values(%s, %s)"
        updatelist = []
        temptime = self.replacetime(SSESubAllList.ReQuesTimeList[0])
        print "jjjjjjjjjjjjjjj", temptime
        updatelist.append(["sse", temptime])
        self.bulk_insert_to_mysql(updatelist, updatetableprop)
        print "len(SSESubAllList.AskQuesNameList)............................", len(SSESubAllList.AskQuesNameList)

        tableprop = "sse_askrep (name, askname, aques, atime, rques, rtime) values(%s, %s, %s, %s, %s, %s)"
        for index in range(len(SSESubAllList.AskTimeList)):
            tempint = 0
            tempasktime = self.replacetime(SSESubAllList.AskTimeList[index])
            temptime = self.replacetime(SSESubAllList.ReQuesTimeList[index])
            try:
                tempAskQuestionList = str(SSESubAllList.AskQuestionList[index])
                tempint = tempint + 1
                tempReplyQuesList = str(SSESubAllList.ReplyQuesList[index])
                tempint = tempint + 1
                self.allQlist.append([SSESubAllList.RepNameList[index], SSESubAllList.AskQuesNameList[index],
                                      tempAskQuestionList, tempasktime,
                                      tempReplyQuesList, temptime])
            except:
                print "except>>>>>."
                if tempint == 1:
                    self.allQlist.append([SSESubAllList.RepNameList[index], SSESubAllList.AskQuesNameList[index],
                                          SSESubAllList.AskQuestionList[index], tempasktime,
                                          "", temptime])
            if len(self.allQlist) == 1000:
                print "len(SSESubAllList.allQlist)............................", len(self.allQlist)
                self.bulk_insert_to_mysql(self.allQlist, tableprop)
                del self.allQlist[:]
        print "len(SSESubAllList.allQlist)............................", len(self.allQlist)
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