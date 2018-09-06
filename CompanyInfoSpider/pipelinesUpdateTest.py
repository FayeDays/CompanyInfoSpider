# -*- coding: utf-8 -*-
#!DATE: 2018/7/19 14:57
#!@Author: yingying
import sys
import MySQLdb
from CompanyInfoSpider.spiders.CN_UpdateSubIndexAll import CNSubUpdateIndexSpider

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
class CNTestPipeline(object):
    allQlist = []
    lastRlist = []
    irmInflist = []
    interClist = []
    mostSRlist = []
    microBllist = []

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456",db="cn_sse_crawl",charset="utf8")
        self.cursor = self.conn.cursor()
        #print "open_spider............................"
        # 存入数据之前清空表：
        self.cursor.execute("truncate table cn_askrep")
        self.conn.commit()

    def process_list(self):
        CNSubAllList = CNSubUpdateIndexSpider()

        self.cursor.execute("select time from lastupdate where comp = 'cn'")
        self.conn.commit()
        lasttimelist = self.cursor.fetchall()
        lasttime = ''.join(str(lasttimelist))
        updateprop = "update lastupdate set time = '%s' where comp = 'cn'" % (CNSubAllList.ReQuesTimeList[0])
        #updateprop = "update lastupdate set time = " + ''.join(CNSubAllList.ReQuesTimeList[0]) + " where comp = 'cn'"
        self.cursor.execute(updateprop)
        self.conn.commit()

        print "len(CNSubAllList.AskQuesNameList)............................",len(CNSubAllList.AskTimeList)
        tableprop = "cn_askrep (id, name, aques, atime, rques, rtime) values(%s, %s, %s, %s, %s, %s)"
        for index in range(len(CNSubAllList.AskTimeList)):
            currenttime = CNSubAllList.ReQuesTimeList[index]
            if lasttime > currenttime:
                break
            self.allQlist.append(
                [CNSubAllList.RepIDList[index], CNSubAllList.RepNameList[index],
                 CNSubAllList.AskQuestionList[index], CNSubAllList.AskTimeList[index],
                 CNSubAllList.ReplyQuesList[index], CNSubAllList.ReQuesTimeList[index]])
            if len(self.allQlist) == 100:
                self.bulk_insert_to_mysql(self.allQlist, tableprop)
                del self.allQlist[:]
        self.bulk_insert_to_mysql(self.allQlist, tableprop)

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