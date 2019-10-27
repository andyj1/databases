# -*- coding: utf-8 -*-
import scrapy
from imdb_crawler.items import ImdbCrawlerItem
from scrapy.selector import Selector

year = 2019
month = 10
day = 26

newday = day-1
class ShowtimesSpider(scrapy.Spider):
    
    name = 'imdb_crawler'
    allowed_domains = ['imdb.com']
    start_url = 'https://www.imdb.com/showtimes/'

    def start_requests(self):
        global year, month, day
        days = [day, day+1, day+2, day+3]
        for d in days:
            link = "https://www.imdb.com/showtimes/{0}-{1}-{2}".format(year, month, d)
            print("date: %s-%s-%s, link: %s" % (year,month,day, link))
            request = scrapy.Request(link, callback=self.parse_movies)
            request.meta['newday'] = d
            yield request

    def parse_movies(self, response):
        newday = response.meta['newday']
        i = 0
        selector = Selector(response)
        for sel in selector.xpath('//div[@class="list_item odd"]'):
            item = self.make_item(i, sel, newday)
            i = i + 1
            yield item

        i = 0
        for sel in selector.xpath('//div[@class="list_item even"]'):
            item = self.make_item(i, sel, newday)
            i = i + 1            
            yield item

    def make_item(self, i, sel, newday):
        item = ImdbCrawlerItem()
        item['theaterName'] = sel.xpath('//div[1]/h3/a/text()').extract()[i]
        theaterinfo = sel.xpath('//div[@class="address"]/div/span/text()').extract()
        item['theaterAddress'] = theaterinfo[i*6:i*6+4]
        item['theaterPhone'] = theaterinfo[i*6+5]
        eachmovie = sel.xpath('div[3]')
        if eachmovie:
            item['movieTitle'] = eachmovie.xpath('div[2]/h4/span/a/text()').extract()[0]
            item['contentRating'] = eachmovie.xpath('div[2]/p[@class="cert-runtime-genre"]/span/img/@title').extract()
            item['duration'] = eachmovie.xpath('div[2]/p[@class="cert-runtime-genre"]/time/text()').extract()
            item['userRating'] = eachmovie.xpath('div[2]/p[@class="cert-runtime-genre"]/span[@class="rating_txt"]/span[1]/strong/text()').extract()
            ranklist = eachmovie.xpath('div[2]/p[@class="cert-runtime-genre"]/span[@class="rating_txt"]/span[4]/strong/text()').extract()
            if ranklist:
                item['currentRank'] = [int(s) for s in ranklist[0].split() if s.isdigit()]
            item['showday'] = "{0}-{1}-{2}".format(year,month,newday)
            times = eachmovie.xpath('div[2]/div[@class="showtimes"]/a/text()').extract()
            item['showtimes'] = []
            for i in range(1, len(times)):
                if times[i] == ' Get Tickets':
                    break
                item['showtimes'].append(times[i])
        return item
