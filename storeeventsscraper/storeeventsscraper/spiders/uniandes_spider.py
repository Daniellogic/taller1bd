import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from storeeventsscraper.items import UniandesItem

class UniandesSpider(CrawlSpider):
    name="uniandes"
    allowed_domains = ["uniandes.edu.co"]
    start_urls = [
#        "http://uniandes.edu.co/",
#        "http://eventos.uniandes.edu.co/"
        "http://eventos.uniandes.edu.co/s/1384/events/social2.aspx?sid=1384&gid=26&sitebuilder=1&pgid=1250&sitebuilder=1&contentbuilder=1"
    ]
    
    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class,"eventListing")]//tr[contains(@align,"top")]',)), callback="parse_items", follow= True),
    )
    
    def parse_items(self, response):
        for sel in response.xpath('//div[contains(@class, "eventWrapper")]'):
            item = UniandesItem()
            item['title'] = sel.xpath('div[contains(@class,"title")]//text()').extract()
            item['dates'] = sel.xpath('div[contains(@class,"dateLoc")]//text()').extract()
            item['desc'] = sel.xpath('div[contains(@class,"description")]//text()').extract()
            item['owner'] = sel.xpath('div[contains(@class,"contacts")]//text()').extract()
            yield item
