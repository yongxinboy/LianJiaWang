# -*- coding: utf-8 -*-
#判断链接是否重复，重复显示存在，不存在放入库中

import scrapy
import re
from scrapy.selector import HtmlXPathSelector
# from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
from time import sleep
# from scrapy.linkextractors import LinkExtractor
from lianjia.spiders import bloomfilter
import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient(host="127.0.0.1")
db = client.ershoufang  # 库名dianping
collection = db.ershoufangInfo

import redis  # 导入redis数据库

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

ii = 0


class houseClassSpider(scrapy.Spider):
    name = "house4"
    allowed_domains = ["lianjia.com"]  # 允许访问的域
    bf = bloomfilter.BloomFilter()

    def __init__(self):
        # headers = {
        #     'Accept': '*/*',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'zh-CN,zh;q=0.9',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'
        # }
        start_urls = []
        urlList = r.lrange('bigArea', 0,-1)
        ii = 0
        self.dict = {}
        for item in urlList:
            itemStr = str(item, encoding="utf-8")
            arr = itemStr.split(',')
            classid = arr[0]
            url = arr[1]
            start_urls.append(url)
            self.dict[url] = {"classid": classid,"urls":url, "num": 0}
            # ii += 1
            # if ii > 1:
            #     break
        print(start_urls)
        self.start_urls = start_urls

    # def start_requests(self):
    #     for url in self.start_urls:
    #         # yield SplashRequest(url, self.parse, args={'wait': 0.5})
    #         yield Request(url,callback=self.parse,headers=self.headers)
    def parse(self, response):
        classInfo = self.dict[response.url]
        objectid = classInfo['classid']
        headurl = classInfo['urls']
        num = classInfo['num']
        hxs = HtmlXPathSelector(response)
        hxsObj = hxs.select('//div[@data-role="ershoufang"]/div/a')
        for secItem in hxsObj:
            className = secItem.select('text()').extract()
            classUrl = secItem.select('@href').extract()
            print(className)
            #print(classUrl)
            if classUrl[0].find("https://lf.lianjia.com") >= 0:
                classUrl2 = classUrl[0]
            else:
                classUrl2="https://bj.lianjia.com"+classUrl[0]

                print(classUrl2)
                if self.bf.isContains(classUrl2):  # 判断字符串是否存在
                    print('exists!')
                else:
                    self.bf.insert(classUrl2)
                    d = '%s' % (classUrl2)
                    r.lpush('quchong4', d)
