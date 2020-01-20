# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ImdbCrawlerItem(Item):
    theaterName = Field()
    theaterAddress = Field()
    theaterPhone = Field()
    movieTitle = Field()
    contentRating = Field()
    duration = Field()
    userRating = Field()
    currentRank = Field()
    showday = Field()
    showtimes = Field()
    pass
