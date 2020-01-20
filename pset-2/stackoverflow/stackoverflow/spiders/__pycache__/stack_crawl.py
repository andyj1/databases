from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from stackoverflow.items import StackItem


class StackSpider(CrawlSpider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?sort=newest",
    ]
    rules = (
        Rule(
            LinkExtractor(allow=('&page=\d')),
            callback='parse',
            follow=True
        ),
    )

    def parse(self, response):
        hxs = Selector(response)
        questions = hxs.xpath('//div[@class="summary"]/h3')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
