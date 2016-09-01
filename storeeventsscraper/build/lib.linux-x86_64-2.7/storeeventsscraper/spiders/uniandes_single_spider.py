import scrapy

from storeeventsscraper.items import UniandesItem

class UniandesSingleSpider(scrapy.Spider):
    name = "uniandes_single"
    allowed_domains = ["uniandes.edu.co"]
    start_urls = [
#        "http://uniandes.edu.co/",
#        "http://eventos.uniandes.edu.co/"
        "http://eventos.uniandes.edu.co/s/1384/events/social2.aspx?sid=1384&gid=26&pgid=15328&cid=23908&ecid=23908&crid=0&calpgid=1250&calcid=3124"
    ]

    def parse(self, response):
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)
        for sel in response.xpath('//div[contains(@class, "eventWrapper")]'):
            item = UniandesItem()
            item['title'] = sel.xpath('div[contains(@class,"title")]/text()').extract()
            item['dates'] = sel.xpath('div[contains(@class,"dateLoc")]//text()').extract()
            item['desc'] = sel.xpath('div[contains(@class,"description")]//text()').extract()
            item['owner'] = sel.xpath('div[contains(@class,"contacts")]//text()').extract()
            yield item
            #print "Title: ",item['title'],"Desc: ",item['desc'],"Dates: ",item['dates'], "Owner: ", item['owner']