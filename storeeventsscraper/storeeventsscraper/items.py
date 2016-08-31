# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy_djangoitem import DjangoItem
#from crawling.models import Event

class StoreeventsscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#class EventItem(DjangoItem):
#    django_model = Event

class UniandesItem(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    dates = scrapy.Field()
    desc = scrapy.Field()
    owner = scrapy.Field()
    
