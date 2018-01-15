# -*- coding: utf-8 -*-
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

import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient(host="127.0.0.1")
db = client.ershoufang  # 库名dianping
collection = db.ershoufangInfo

import redis  # 导入redis数据库

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

ii = 0


class houseClassSpider(scrapy.Spider):
    name = "house3"
    allowed_domains = ["lianjia.com"]  # 允许访问的域
    #start_urls = ['https://bj.lianjia.com/ershoufang/']

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
            ii += 1
            if ii > 1:
                break
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
        if num > 2:
            return None
        hxs = HtmlXPathSelector(response)
        hxs=response.xpath('//ul[@class="sellListContent"]/li[@class="clear"]')
        # for hx in hxs:
        names=hxs[0].select('//div[@class="title"]/a[@class=""]/text()').extract()
        url=response.xpath('//div[@class="title"]/a[@class=""]/@href').extract()
        adds=response.xpath('//div[@class="address"]/div[@class="houseInfo"]/a/text()').extract()
        followInfo = response.xpath('//div[@class="followInfo"]/text()').extract()
        totalPrice = response.xpath('//div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract()
        unitPrice=response.xpath('//div[@class="unitPrice"]/span/text()').extract()
        tag=response.xpath('//div[@class="tag"]/span/text()').extract()
        for i in range(len(names)):
        #     # name = "房名:" + names[i]
        #     # adress = "地名:" + adds[i]
        #     # followInfos = "关注:" + followInfo[i]
        #     # totalPrices= "总价格:" + totalPrice[i] + "万"
        #     # unitPrices = "单元价格:" + unitPrice[i]
        #     # tags = "其他信息:" + tag[i]
        #     # urls = "链接:" + url[i]
            name = names[i]
            adress = adds[i]
            followInfos = followInfo[i]
            totalPrices = totalPrice[i] + "万"
            unitPrices = unitPrice[i]
            tags = tag[i]
            urls = url[i]
            print(name)
            print(adress)
            print(followInfos)
            print(totalPrices)
            print(unitPrices)
            print(tags)
            print(urls)
        print('11111111111111111111111111111111111111111111111111111111111111111111111111111')
    #         classid =self.insertMongo(name,adress,followInfos,totalPrices,unitPrices,tags,urls,ObjectId(objectid))
    #
    # def insertMongo(self,name,adress,followInfos,totalPrices,unitPrices,tags,urls,pid):
    #     classid = collection.insert({'房名': name, '地址': adress, '关注': followInfos, '总价格': totalPrices, '单元价格': unitPrices, '其他信息': tags,'房源链接': urls, 'pid': pid})
    #     return classid
    #    --------------------------不用调用方法直接取下一页------------------------------------------------------------------------------
        nextPages=response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract()[0]
        data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        #print(data)
        sq = re.search(r"\d+", data).group()
        #print(type(sq))
        #nextPage=re.sub("{page}",sq,nextPages)
        #next ="https://bj.lianjia.com/" + nextPage
        a=1
        sq1 =int(sq)
        if a<sq1:
            a+=1
        #for a in range(2,sq1+1):
        next = headurl+"pg%i/"%(a)
        print('-------------------------')
        print(next)
        print('----------------------------')
        classInfo['num'] += 1
        self.dict[next] = classInfo
        request = Request(next, callback=self.parse)
        yield request
#****************************************************************下一页方法
            # nextPages = hxs.select('//div[@class="page-box house-lst-page-box"]/li/a/@href')
            # print(len(nextPages))
            # nextPage = nextPages.extract()[len(nextPages) - 1]
            # # print(headurl)
            # nextPage = headurl + nextPage
            # # print(nextPage)
            # classInfo['num'] += 1
            # self.dict[nextPage] = classInfo
            # request = Request(nextPage, callback=self.parse)
            # yield request
            # print('--------end--------------')
# *****************************************************************下一页方法

        #classid = collection.insert({'name': name, 'adress': adress,'followInfo':followInfos,'totalPrice':totalPrices,'unitPrice':unitPrices,'tag':tags,'url':urls,'pid':pid})
        #return classid
