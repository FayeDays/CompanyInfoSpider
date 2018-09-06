#!DATE: 2018/7/15 18:42
#!@Author: yingying

import scrapy
from scrapy import cmdline
name = 'CNCompanyID'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())