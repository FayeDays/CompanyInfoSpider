# -*- coding: UTF-8 -*-
#!DATE: 2018/7/19 14:51
#!@Author: yingying
import requests
import scrapy
import time
import MySQLdb
from scrapy.selector import Selector

default_encoding = 'utf-8'
class CNSubUpdateIndexSpider(scrapy.Spider):
    name = 'CNUpdateInd'
    allowed_domains = ['irm.cninfo.com.cn']
    start_urls = ['http://irm.cninfo.com.cn/ircs/interaction/allQuestionsForSzse.do']
    ROOT_URL = 'http://irm.cninfo.com.cn/ircs/interaction/allQuestionsForSzse.do'
    custom_settings = {'ITEM_PIPELINES': {'CompanyInfoSpider.pipelinesUpdateTest.CNTestPipeline': 1}}
    varint = 0
    compIDList = []
    RepIDList = []
    RepNameList = []
    AskQuestionList = []
    AskTimeList = []
    ReplyQuesList = []
    ReQuesTimeList = []

    def getCompID(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="cn_sse_crawl", charset="utf8")
        self.cursor = self.conn.cursor()
        self.cursor.execute("select id,name from cn_id limit 1")
        self.conn.commit()
        self.compIDList = self.cursor.fetchall()

    def parse(self, response):
        formdata = {
            'categoryId': '',
            'code': '',
            'condition.keyWord': '',
            'condition.loginId': '',
            'condition.marketType': '',
            'condition.plate': '',
            'condition.provinceCode': '',
            'condition.questionAtr': '',
            'condition.questionCla': '',
            'condition.questioner': '',
            'condition.questionerType': '',
            'condition.searchRange': '',
            'condition.searchType': 'code',
            'condition.status': '',
            'pageNo': '',
            'pageSize': '10',
            'requestMethod': 'POST',
            'requestUri': '/ircs/interaction/lastRepliesforSzseSsgs.do',
            'source': '2'
        }
        self.getCompID()
        for compID in self.compIDList:
            tempid = ''.join(compID[0])
            tempname = ''.join(compID[1])
            currenturl = 'http://irm.cninfo.com.cn/ircs/interaction/lastRepliesforSzseSsgs.do?condition.type=1&condition.stockcode=' + tempid + '&condition.stocktype=S'
            try:
                self.varint = 1
                formdata['pageNo'] = str(self.varint)
                while self.varint <= 5:
                    responsenow = requests.post(currenturl, data=formdata, timeout=1)
                    self.parser_html(responsenow, tempid, tempname)
                    time.sleep(1)
                    self.varint = self.varint + 1
                    formdata['pageNo'] = str(self.varint)
            except:
                print('parse failed>>>>>>>>>')

    def parser_html(self, response, compid, compname):
        AskQueList = Selector(text=response.text).xpath(
            "//div[@class='wd_news']/ul/li/div[1]/p[2]/a/text()").extract()
        for AskQue in AskQueList:
            self.AskQuestionList.append(str(AskQue.strip()))
        AskTList = Selector(text=response.text).xpath(
            "//div[@class='wd_news']/ul/li/div[1]/p[2]/span/text()").extract()
        for AskT in AskTList:
            AskTTemp = AskT.strip().split('（')[1]
            self.AskTimeList.append(str(AskTTemp.split('）')[0]))
        ReplyQList = Selector(text=response.text).xpath(
            "//div[@class='wd_news']/ul/li/div[2]/p[2]/a/text()").extract()
        for ReplyQ in ReplyQList:
            self.ReplyQuesList.append(str(ReplyQ.strip()))
        ReQTimeList = Selector(text=response.text).xpath(
            "//div[@class='wd_news']/ul/li/div[3]/div[1]/span[1]/a/text()").extract()
        for ReQTime in ReQTimeList:
            ReQTimeTemp = ReQTime.strip().split('（')[1]
            self.ReQuesTimeList.append(str(ReQTimeTemp.split('）')[0]))
        i = 0
        while i < len(ReQTimeList):
            self.RepNameList.append(compname)
            i = i + 1