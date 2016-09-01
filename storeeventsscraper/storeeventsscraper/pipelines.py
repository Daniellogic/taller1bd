# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json


class StoreeventsscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class FilterDuplicateEventsPipeline(object):
    def __init__(self):
        self.events_seen = set()
    
    def process_item(self,item,spider):
        idstring = str(item['title'])
        if idstring in self.events_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.events_seen.add(idstring)
            return item
            

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('eventospipeline.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item