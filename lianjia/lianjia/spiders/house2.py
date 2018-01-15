import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
from urllib.request import urlopen
#from urllib.request import Request
from bs4 import BeautifulSoup
from lxml import etree
from bson.objectid import ObjectId

import pymongo
client = pymongo.MongoClient(host="127.0.0.1")
db = client.ershoufang          #库名dianping
collection = db.bigArea
import redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
import scrapy
from scrapy.http import Request
import http.cookiejar
from scrapy.http.cookies import CookieJar
import requests
#from scrapy_splash import SplashRequest

class houseClassSpider(scrapy.Spider):
    name = "house2"
    allowed_domains = ['lianjia.com']  # 允许访问的域

    start_urls = [
        #"http://bj.maitian.cn/esfall",
        "https://bj.lianjia.com/ershoufang/chaoyang/",
    ]
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'
        }

    def start_requests(self):
        for url in self.start_urls:
            # yield SplashRequest(url, self.parse, args={'wait': 0.5})
            yield Request(url,callback=self.parse,headers=self.headers)
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        hxs=response.xpath('//ul[@class="sellListContent"]/li[@class="clear"]')
        # for hx in hxs:
        names=hxs[0].select('//div[@class="title"]/a[@class=""]/text()').extract()
        adds=response.xpath('//div[@class="address"]/div[@class="houseInfo"]/a/text()').extract()
        followInfo = response.xpath('//div[@class="followInfo"]/text()').extract()
        totalPrice = response.xpath('//div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract()
        unitPrice=response.xpath('//div[@class="unitPrice"]/span/text()').extract()
        tag=response.xpath('//div[@class="tag"]/span/text()').extract()
        for i in range(len(names)):
            print("房名:"+names[i])
            print("地名:"+adds[i])
            print("关注:"+followInfo[i])
            print("总价格:"+totalPrice[i])
            print("单元价格:"+unitPrice[i])
            print("其他信息:"+tag[i])

            #=====================================================================================================
            # if classUrl[0].find("https://lf.lianjia.com/ershoufang") >= 0:
            #     classUrl2 = classUrl[0]
            # else:
            #     classUrl2="https://lf.lianjia.com/ershoufang"+classUrl[0]
            # print(className[0])
            # print(classUrl2)



