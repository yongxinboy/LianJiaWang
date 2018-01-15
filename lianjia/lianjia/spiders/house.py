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
    name = "house"
    allowed_domains = ['lianjia.com']  # 允许访问的域
    start_urls = [
        #"http://bj.maitian.cn/esfall",
        "https://bj.lianjia.com/ershoufang/",
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
        hxsObj = hxs.select('//div[@class="position"]/dl/dd/div[@data-role="ershoufang"]/div/a')
        for secItem in hxsObj:
            className = secItem.select('text()').extract()
            classUrl = secItem.select('@href').extract()
            if classUrl[0].find("https://lf.lianjia.com") >= 0:
                classUrl2 = classUrl[0]
            else:
                classUrl2="https://bj.lianjia.com"+classUrl[0]
            # print('------------------------------------------------------------------------')
            print(classUrl2)
            print(className[0])
            # print('----------------------------------')

            classid= self.insertMongo(className[0], None)
            # self.pushRedis(classid, classUrl2)
            d = '%s,%s' % (classid, classUrl2)
            r.lpush('bigArea',d )
            # request = Request(classUrl2, callback=lambda response, pid=str(classid): self.parse_subClass(response, pid))
            # yield request
    #         classid=1
    #         print(classUrl2)
    #         request = Request(classUrl2, callback=lambda response, pid=str(classid): self.parse_subClass(response, pid))
    #         yield request
    #         # print("======================")
    #
    # def parse_subClass(self, response, pid):
    #     hxs = HtmlXPathSelector(response)
    #     hxsObj = hxs.select('//div[@class="position"]/dl/dd/div[@data-role="ershoufang"]/div/a')
    #     print(response.url)
    #     for secItem in hxsObj:
    #         className3 = secItem.select('text()').extract()
    #         classUrl3 = secItem.select('@href').extract()
    #         if  response.url.find("https://lf.lianjia.com") >= 0:
    #
    #             classUrl3 = "https://lf.lianjia.com"+classUrl3[0]
    #         else:
    #
    #             classUrl3 = "https://bj.lianjia.com"+classUrl3[0]
    #         print('-----------rrrrrrrrrrrrrrrrrr-----------------')
    #         print(className3[0])
    #         print(classUrl3)
    #         # classid = self.insertMongo(className2[0], ObjectId(pid))
    #         # self.pushRedis(classid, pid, classUrl2[0])
    #
    def insertMongo(self, areaname, pid):
        classid = collection.insert({'areaname': areaname, 'pid': pid})
        return classid

    # def pushRedis(self, classid, pid, url):
    #     bigArea = '%s,%s,%s' % (classid, pid, url)
    #     r.lpush('bigArea', bigArea)

