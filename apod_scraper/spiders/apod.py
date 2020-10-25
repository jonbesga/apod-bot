import scrapy
from ..items import ApodScraperItemLoader


class ApodSpider(scrapy.Spider):
    name = "apod"
    allowed_domains = ["apod.nasa.gov"]
    start_urls = ["https://apod.nasa.gov/apod/archivepixFull.html"]

    def parse(self, response):
        all_apod_links = response.xpath("/html/body/b/a/@href").getall()[:1]
        for link in all_apod_links:
            next_page = response.urljoin(link)
            yield response.follow(next_page, callback=self.parse_page)

    def parse_page(self, response):
        asil = ApodScraperItemLoader(response=response)
        asil.add_xpath("date", "/html/body/center[1]/p[2]/text()")
        asil.add_xpath("title", "/html/body/center[2]/b[1]/text()")
        asil.add_xpath("image_urls", "/html/body/center[1]/p[2]/a/@href")
        asil.add_xpath("explanation", "/html/body/p[1]")
        asil.add_xpath("credits", "/html/body/center[2]/a")
        yield asil.load_item()
