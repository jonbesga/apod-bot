import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.selector import Selector


class ApodScraperItem(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    explanation = scrapy.Field()
    credits = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


def extract_credits(credit_sel):
    credits = list()
    for credit in credit_sel:
        cred = Selector(text=credit)
        link = cred.xpath("//@href").get()
        name = cred.xpath("//text()").get()
        credits.append({"link": link, "name": name})
    return credits


def add_base_url(value, loader_context):
    response = loader_context.get("response")
    return response.urljoin(value)


class ApodScraperItemLoader(ItemLoader):
    default_item_class = ApodScraperItem

    date_in = MapCompose(str.strip)
    date_out = TakeFirst()
    title_in = MapCompose(str.strip)
    title_out = Join()
    image_urls_in = MapCompose(add_base_url)
    credits_in = Compose(extract_credits)
