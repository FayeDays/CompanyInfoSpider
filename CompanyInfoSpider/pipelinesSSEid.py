# -*- coding: utf-8 -*-
#!DATE: 2018/7/15 13:26
#!@Author: yingying
import sys
import MySQLdb
import re

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class CncompanyidSpiderFastPipeline(object):
    companylist = []

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456",db="cn_sse_crawl",charset="utf8")
        self.cursor = self.conn.cursor()
        # 存入数据之前清空表：
        isexists = self.table_exists(self.cursor, "sse_id")
        if isexists == 1:
            self.cursor.execute("truncate table sse_id")
            self.conn.commit()
        else:
            self.cursor.execute("create table sse_id(id char(6) not null, name char(20) not null, primary key(id))")
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

    # 批量插入mysql数据库
    def bulk_insert_to_mysql(self, bulkdata):
        try:
            print "the length of the data-------", len(self.companylist)
            sql = "insert into sse_id (id, name) values(%s, %s)"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def process_item(self, item, spider):
        self.companylist.append([item['CompanyID'], item['CompanyName']])
        if len(self.companylist) == 1000:
            self.bulk_insert_to_mysql(self.companylist)
            # 清空缓冲区
            del self.companylist[:]
        return item

    def close_spider(self, spider):
        print "closing spider,last commit", len(self.companylist)
        self.bulk_insert_to_mysql(self.companylist)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()