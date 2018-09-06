# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CompanyinfospiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    CompanyID = scrapy.Field()
    CompanyName = scrapy.Field()

    FansComID = scrapy.Field()
    FansComName = scrapy.Field()
    FansComAllFans = scrapy.Field()
    FansComAllReply = scrapy.Field()

    AskedCompID = scrapy.Field()
    AskedCompName = scrapy.Field()
    AskedCompAllAsk = scrapy.Field()
    AskedCompAllReply = scrapy.Field()

    FansInvName = scrapy.Field()
    FansInvAllFans = scrapy.Field()
    FansInvAllAsk = scrapy.Field()

    AskInvName = scrapy.Field()
    AskAllAsk = scrapy.Field()
    AskTenDaysAsk = scrapy.Field()
    AskInvAllFans = scrapy.Field()

    MostRepComName = scrapy.Field()
    MostRepComID = scrapy.Field()
    MostRepAllRep = scrapy.Field()
    MostRepTenDaysReply = scrapy.Field()
    MostRepInvAllFans = scrapy.Field()

    MostRepRateComName = scrapy.Field()
    MostRepRateAllRep = scrapy.Field()
    MostRepRateAllFans = scrapy.Field()

    FansObserName = scrapy.Field()
    FansObserAllFans = scrapy.Field()
    FansObserAllAsk = scrapy.Field()

    LeastRepComID = scrapy.Field()
    LeastRepComName = scrapy.Field()
    LeastLastWeekRate = scrapy.Field()

    AskQuesName = scrapy.Field()
    AskedComID = scrapy.Field()
    AskedComName = scrapy.Field()
    AskQuestion = scrapy.Field()
    ReComName = scrapy.Field()
    ReAskQuesName = scrapy.Field()
    ReplyQuestion = scrapy.Field()
    AskTime = scrapy.Field()
    ReQuesTime = scrapy.Field()

    RepAskName = scrapy.Field()
    RepComID = scrapy.Field()
    RepComName = scrapy.Field()
    RepAskQuestion = scrapy.Field()
    ReplyQuestion = scrapy.Field()
    RepAskTime = scrapy.Field()
    ReplyTime = scrapy.Field()

    IrmComID = scrapy.Field()
    IrmComName = scrapy.Field()
    IrmInfName = scrapy.Field()
    IrmInfTime = scrapy.Field()

    InterComID = scrapy.Field()
    InterComName = scrapy.Field()
    InterTitle = scrapy.Field()
    InterTime = scrapy.Field()

    MostSRAskName = scrapy.Field()
    MostSRComID = scrapy.Field()
    MostSRComName = scrapy.Field()
    MostSRAskQuestion = scrapy.Field()
    MostSRQuestion = scrapy.Field()
    MostSRAskTime = scrapy.Field()
    MostSRReTime = scrapy.Field()

    MicroBlComID = scrapy.Field()
    MicroBlComName = scrapy.Field()
    MicroBlTitle = scrapy.Field()
    MicroBlTime = scrapy.Field()