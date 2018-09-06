# -*- coding: UTF-8 -*-
#!DATE: 2018/7/19 14:51
#!@Author: yingying
import scrapy
import urllib2
import urllib
import json
import requests
import MySQLdb
import time
from scrapy.selector import Selector

#当前有效网址：http://sns.sseinfo.com/ajax/userfeeds.do?typeCode=company&type=11&pageSize=10&uid=65&page=2&_=1534767027645
#利用回复时间插入表
#插入前检查表是否存在，再决定是创建表还是插入
default_encoding = 'utf-8'
defaultencoding = 'utf-8'
class SSESubUpdateIndexSpider(scrapy.Spider):
    name = 'SSEUpdateInd'
    custom_settings = {'ITEM_PIPELINES': {'CompanyInfoSpider.pipelinesSSEUpdatemysql.SSEUpdateSqlPipeline': 1}}
    allowed_domains = ['sns.sseinfo.com']
    start_urls = ['http://sns.sseinfo.com/']
    AJAX_URL = 'http://sns.sseinfo.com/ajax/getCompany.do'
    compNameList = []
    AskQuesNameList = []
    AskQuestionList = []
    AskTimeList = []
    ReplyQuesList = []
    ReQuesTimeList = []
    RepIDList = []
    RepNameList = []
    page = 0

    def getCompName(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="cn_sse_crawl", charset="utf8")
        self.cursor = self.conn.cursor()
        self.cursor.execute("select id,name from sse_id limit 1")
        self.conn.commit()
        self.compNameList = self.cursor.fetchall()

    def request_ajax_data(self, url, fdata):
        params = json.dumps(fdata)
        req = urllib2.Request(url, params)
        req.add_header('type', 'post')
        req.add_header('contentType', 'application/x-www-form-urlencoded')
        req.add_header('url', 'ajax/getCompany.do')
        response = requests.post(url, data=fdata)
        return response.text

    def parse(self, response):
        ajax_body = {"data":""}
        self.getCompName()
        for compName in self.compNameList:
            compid = compName[0]
            compname = compName[1]
            ajax_body['data'] = ''.join(compname)
            try:
                tempid = self.request_ajax_data(self.AJAX_URL, ajax_body)
                self.page = 1
                tempurl = 'http://sns.sseinfo.com/ajax/userfeeds.do?typeCode=company&type=11&pageSize=10&uid=' + tempid + '&page='
                while self.page <= 5:
                    currenturl = tempurl + str(self.page) + '&_=1534767027645'
                    responsenow = requests.get(currenturl, timeout=1)
                    if responsenow.text < 10000:
                        break
                    self.parser_html(responsenow, compid, compname)
                    time.sleep(1)
                    self.page = self.page + 1
            except:
                print('parse failed>>>>>>>>>')

    def parser_html(self, response, compid, compname):
        AskQNameList = Selector(text=response.text).xpath(
            "//div[@class='m_feed_detail']/div[1]/p/text()").extract()
        for AskQName in AskQNameList:
            self.AskQuesNameList.append(AskQName)
        tempint = 0
        AskQueList = Selector(text=response.text).xpath(
            "//div[@class='m_feed_detail']/div[2]/div[2]/text()").extract()
        for AskQue in AskQueList:
            if tempint % 2 != 0:
                self.AskQuestionList.append(AskQue.strip())
            tempint = tempint + 1
        AskTList = Selector(text=response.text).xpath(
            "//div[@class='m_feed_detail']/div[2]/div[4]/div[2]/span/text()").extract()
        for AskT in AskTList:
            self.AskTimeList.append(AskT)
        ReplyQList = Selector(text=response.text).xpath(
            "//div[@class='m_feed_detail m_qa']/div[3]/div[2]/text()").extract()
        for ReplyQ in ReplyQList:
            self.ReplyQuesList.append(ReplyQ.strip())
        ReQTimeList = Selector(text=response.text).xpath(
            "//div[@class='m_feed_detail m_qa']/div[4]/div[3]/span/text()").extract()
        for ReQTime in ReQTimeList:
            self.ReQuesTimeList.append(ReQTime.strip())
        i = 0
        while i < len(ReQTimeList):
            #self.RepIDList.append(compid)
            self.RepNameList.append(compname)
            i = i + 1

