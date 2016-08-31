import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from urlparse import urlparse

from storeeventsscraper.items import UniandesItem

class UniandesSpider(CrawlSpider):
    name="uniandes"
    allowed_domains = ["uniandes.edu.co"]
    start_urls = [
        "http://uniandes.edu.co/",
#        "http://eventos.uniandes.edu.co/",
#        "http://eventos.uniandes.edu.co/s/1384/events/social2.aspx?sid=1384&gid=26&sitebuilder=1&pgid=1250&sitebuilder=1&contentbuilder=1",
#        "http://ingenieria.uniandes.edu.co/paginas/home.aspx",
#         "http://administracion.uniandes.edu.co/",
    ]
    
    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class,"eventListing")]//tr[contains(@align,"top")]',)), callback="parse_items"),#, follow= True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//*[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"detalle")]',)),callback="parse_items"),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//*[contains(translate(@class, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"ev_link_row")]',)),callback="parse_items"),
        Rule(SgmlLinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\', ), restrict_xpaths=('//*[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"event")]',))),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//*[contains(@href,"facultades")]',))),
    )
    
    def parse_items(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        #print domain
        #Eventos institucionales
        for sel in response.xpath('//div[contains(@class, "eventWrapper")]'):
            item = UniandesItem()
            item['domain'] = domain
            item['title'] = sel.xpath('div[contains(@class,"title")]//text()').extract()
            item['dates'] = sel.xpath('div[contains(@class,"dateLoc")]//text()').extract()
            item['desc'] = sel.xpath('div[contains(@class,"description")]//text()').extract()
            item['owner'] = sel.xpath('div[contains(@class,"contacts")]//text()').extract()
            yield item
        #Eventos ingenieria
        for sel in response.xpath('//div[contains(@class, "dual event")]'):
            if(sel.xpath('//div[@id="CuerpoEvento"]').extract() is not None):
                item = UniandesItem()
                item['domain'] = domain
                item['title'] = sel.xpath('//h2[@id="titulo"]//text()').extract()
                item['dates'] = sel.xpath('//div[contains(@class,"detail-date")]//text()').extract()
                item['desc'] = sel.xpath('//div[@id="CuerpoEvento"]//text()').extract()
                item['owner'] = sel.xpath('//a[starts-with(@href, "mailto")]/text()').extract()
                yield item
        #Eventos administracion
        for sel in response.xpath('//div[contains(concat(" ", @class, " "), " event-detail ")]'):
            item = UniandesItem()
            item['domain'] = domain
            item['title'] = sel.xpath('.//div[contains(@class,"header")]//h2/text()').extract()
            item['dates'] = sel.xpath('.//div[contains(@class,"date")]//div/text()').extract()
            item['desc'] = sel.xpath('.//div[contains(@class,"description")]//*/text()').extract()
            item['owner'] = sel.xpath('//a[starts-with(@href, "mailto")]/text()').extract()
            yield item
    custom_settings = {
        'DEPTH_LIMIT': '3',
    }
