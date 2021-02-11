import scrapy

class Scraped_Files(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

class BhavcopySpider(scrapy.Spider):
    name = 'bhavcopy'
    allowed_domains = ['www.bseindia.com']
    start_urls = ['https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx/']

    def parse(self, response):
        relative_url = response.xpath("//a[@id='ContentPlaceHolder1_btnhylZip']/@href").get()
        # relative_url = response.urljoin(relative_url)
        i = Scraped_Files()
        i['file_urls'] = [relative_url]

        yield i
