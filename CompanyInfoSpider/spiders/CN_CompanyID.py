#!DATE: 2018/7/17 9:51
#!@Author: yingying
# -*- coding: utf-8 -*-
import scrapy

from CompanyInfoSpider.items import CompanyinfospiderItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class CNSSEcompanyidSpider(scrapy.Spider):
    name = 'CNCompanyID'
    custom_settings = { 'ITEM_PIPELINES':{'CompanyInfoSpider.pipelinesCNid.CncompanyidSpiderFastPipeline': 1}}
    allowed_domains = ['dl.app.gtja.com']
    start_urls = ['http://dl.app.gtja.com/public/fyevent/stockfile/sz_stkinfo.txt']
    #rules = [Rule(LinkExtractor(allow=['sz_stkinfo\.txt']), 'parse'),Rule(LinkExtractor(allow=['sh_stkinfo\.txt']), 'parse')]

    def parse(self, response):
        item = CompanyinfospiderItem()
        item['url'] = response.url
        initinfo = response.body
        items = initinfo.split(';')
        for i in range(len(items)):
            if items[i].strip() == '':
                print("Empty Item\t")
                break
            else:
                pass
            companyinfo = items[i].split(',')
            item['CompanyID'] = companyinfo[0]
            item['CompanyName'] = companyinfo[1]
            yield item

