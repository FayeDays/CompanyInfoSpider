# -*- coding: utf-8 -*-
#!DATE: 2018/7/19 14:57
#!@Author: yingying
import sys
import MySQLdb
import re
from CompanyInfoSpider.spiders.CN_SubIndexAll import CNSubAllIndexSpider

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
        isexists = self.table_exists(self.cursor, "cn_askrep")
        if isexists == 1:
            self.cursor.execute("truncate table cn_askrep")
            self.conn.commit()
        else:
            self.cursor.execute(
                "create table cn_askrep(name char(20) not null, aques text, atime char(30), rques text, rtime char(30))")
            self.conn.commit()
        isexists = self.table_exists(self.cursor, "lastupdate")
        if isexists == 0:
            self.cursor.execute(
                "create table lastupdate(comp char(3) not null, time char(30) not null, primary key(comp))")
            self.conn.commit()
        else:
            self.cursor.execute("delete from lastupdate where comp = 'cn'")
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
        CNSubAllList = CNSubAllIndexSpider()

        print "len(CNSubAllList.ReQuesTimeList)>>>>>>>>>>>>>>>>", len(CNSubAllList.ReQuesTimeList)
        updatetableprop = "lastupdate (comp, time) values(%s, %s)"
        updatelist = []
        updatelist.append(["cn", CNSubAllList.ReQuesTimeList[0]])
        self.bulk_insert_to_mysql(updatelist, updatetableprop)

        tableprop = "cn_askrep (name, aques, atime, rques, rtime) values(%s, %s, %s, %s, %s)"
        for index in range(len(CNSubAllList.AskTimeList)):
            self.allQlist.append(
                [CNSubAllList.RepNameList[index],
                 CNSubAllList.AskQuestionList[index], CNSubAllList.AskTimeList[index],
                 CNSubAllList.ReplyQuesList[index], CNSubAllList.ReQuesTimeList[index]])
            if len(self.allQlist) == 1000:
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
        self.process_list()
        del self.allQlist[:]
        self.conn.commit()
        self.cursor.close()
        self.conn.close()