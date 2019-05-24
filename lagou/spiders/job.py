# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from lagou.items import ImageItem
import json,re

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/list_python']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,args = {'timeout':20,'images':0})

    def parse(self, response):
        data = json.loads(response.body)
        print(data)


class ImageSpider(scrapy.Spider): #爬取高像素图片，需要在setting打开 ImagesPipeline
    name = 'image'
    allowed_domains = ['alpha.wallhaven.cc']
    start_urls = ['https://alpha.wallhaven.cc/search']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,args = {'timeout':20})

    def parse(self, response):
        href_list = response.xpath('//li//a[@class="preview"]/@href').extract()
        for href in href_list[:20]:
            yield SplashRequest(url=href, callback=self.get_detail,args={'timeout': 20})

    def get_detail(self,response):
        item = ImageItem()
        images_urls = ["https://"+response.xpath('//*[@id="wallpaper"]/@src').extract_first()[2:]]
        item["images_urls"]=images_urls
        yield item

class SpiderSpider(scrapy.Spider):  #爬取JS普通案例
    name = 'spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,args = {'timeout':8,'images':0})
    def parse(self, response):
        authors = response.css('div.quote small.author::text').extract()
        quotes = response.css('div.quote span.text::text').extract()
        yield from (dict(zip(['author','quote'],item)) for item in zip(authors,quotes))
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            url = response.urljoin(next_url)#构造了翻页的绝对url地址
            yield SplashRequest(url,args = {'timeout':8,'images':0})

class JobSpider(scrapy.Spider): #爬取前程工作，保存数据到了mysql,需要在setting打开 Mysqlpipline
    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/040000,000000,0000,00,9,99,%25E7%25B3%25BB%25E7%25BB%259F%25E8%25BF%2590%25E7%25BB%25B4%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,' + '%d.html' %i for i in range(1,7)]

    def parse(self, response):
        for div in response.xpath('//div[@class="dw_table"]//div[@class="el"][position()>1]'):
            job = div.css('a::attr(title)').extract_first().strip()
            place = div.css('span.t3::text').extract_first().strip()
            company = div.css('span.t2 a::attr(title)').extract_first().strip()
            str = div.css('span.t4::text').extract_first()
            money  = float(re.findall(r'(.*?)-.*?',str)[0])
            url=div.css('a::attr(href)').extract_first()
            item = dict(job=job, company=company, money=money, place=place)
            yield scrapy.Request(url, meta={'item': item}, callback=self.get_detail)

    def get_detail(self, response):
        item = response.meta['item']
        job1 = response.xpath('//div[@class="bmsg job_msg inbox"]/p//text()').extract()
        job2 = response.xpath('//div[@class="bmsg job_msg inbox"]/div//text()').extract()
        job3 = response.xpath('//div[@class="bmsg job_msg inbox"]//text()').extract()
        jobs = [i for i in [i.strip() for i in job1 if i != ""]+[i.strip() for i in job2 if i != ""]+[i.strip() for i in job3 if i != ""] if i!= ""]
        item['required'] = "".join(jobs)
        yield item


