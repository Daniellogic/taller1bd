import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from urlparse import urlparse

from storeeventsscraper.items import UniandesItem

class UniandesSpider(CrawlSpider):
    name="uniandes"
    allowed_domains = ["uniandes.edu.co"]
    start_urls = [
#        "http://uniandes.edu.co/",
#        "http://www.uniandes.edu.co/mapa-del-sitio-1",
         "https://economia.uniandes.edu.co/",
#        "http://eventos.uniandes.edu.co/",
#        "http://eventos.uniandes.edu.co/s/1384/events/social2.aspx?sid=1384&gid=26&sitebuilder=1&pgid=1250&sitebuilder=1&contentbuilder=1",
        "http://ingenieria.uniandes.edu.co/paginas/home.aspx",
         "http://administracion.uniandes.edu.co/",
    ]
    
    rules = (
        #Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(@href,"facultades")]',))),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(@title,"Facultad")]',))),
        #Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(@title,"Facultad") or contains(@title,"Departamento")]',))),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//div[contains(@class,"eventListing")]//tr[contains(@align,"top")]',)), callback="parse_items"),#, follow= True),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(@href,"icalrepeat.detail")]',)),callback="parse_items"),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"detalleeventos")]',)),callback="parse_items"),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(translate(@class, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"ev_link_row")]',)),callback="parse_items"),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"layout=event")]',)),callback="parse_items"),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co',"facultad\/noticias-economia","facultad\/destacados"), restrict_xpaths=('//*[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"layout=detailevents")]',)),callback="parse_items"),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"event")]',))),
        Rule(LinkExtractor(allow=(), deny=('eventos\.uniandes\.edu\.co'), restrict_xpaths=('//*[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"icagenda")]',))),
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
        #Eventos Artes
        for sel in response.xpath('//div[@id="jevents_body"]'):
            item = UniandesItem()
            item['domain'] = domain
            item['title'] = response.xpath('//div[position()=1]/span[position()=1]/text()').extract()
            item['dates'] = sel.xpath('.//span[contains(@class,"hf_event")]/text()').extract()
            item['desc'] = sel.xpath('.//p/text()').extract()
            item['owner'] = sel.xpath('//a[starts-with(@href, "mailto")]/text()').extract()
            yield item
        #Eventos CienciasSociales
        for sel in response.xpath('//div[@id="icagenda"]'):
            item = UniandesItem()
            item['domain'] = domain
            item['title'] = response.xpath('.//h2/text()').extract()
            item['dates'] = sel.xpath('.//div[contains(@class,"details")]//text()').extract()
            item['desc'] = sel.xpath('.//div[@id="detail-desc"]//text()').extract()
            item['owner'] = sel.xpath('//a[starts-with(@href, "mailto")]/text()').extract()
            yield item
        #Eventos Derecho
        for sel in response.xpath('//table[@id="jevents_body"]'):
            item = UniandesItem()
            item['domain'] = domain
            item['title'] = sel.xpath('.//tr[contains(@class,"headingrow")]//text()').extract()
            item['dates'] = sel.xpath('.//td[contains(@class,"ev_detail repeat")]//text()').extract()
            item['desc'] = sel.xpath('.//td[contains(concat(" ", @class, " "), " ev_detail ") and not (contains(@class,"repeat"))]//text()').extract()
            item['owner'] = sel.xpath('.//a[starts-with(@href, "mailto")]/text()').extract()
            yield item
        #Eventos Economia
        for sel in response.xpath('//div[contains(@class,"wrapper_centrar_contenido row")]'):
            item = UniandesItem()
            item['domain'] = domain
            item['title'] = sel.xpath('(.//div[contains(@class,"titulo") and contains(@class,"col-xs")])[1]/text()').extract()
            item['dates'] = sel.xpath('(.//div[contains(@class,"titulo") and contains(@class,"col-xs")])[2]/text()').extract()
            item['desc'] = sel.xpath('./div[position()=5]/div//text()').extract()
            item['owner'] = sel.xpath('.//a[starts-with(@href, "mailto")]/text()').extract()
            yield item
    custom_settings = {
        'DEPTH_LIMIT': '3',
    }
