import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import MybookScrapperItem
from itemloaders.processors import MapCompose

from mybook_scrapper.settings import IMAGES_STORE


class MybookSpider(CrawlSpider):
    name = "mybook"
    allowed_domains = ["mybook.ru"]
    start_urls = ["https://mybook.ru/tags/russkaya-fantastika/"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//div[@class='e4xwgl-0 iJwsmp']/a"),
            callback="parse_item",
            follow=True,
        ),
        # Rule(
        #     LinkExtractor(restrict_xpaths="//div[@class='m4n24q-0 bkolKJ']/a"),
        # ),
    )

    def parse_item(self, response):
        # print(response.url)
        loader = ItemLoader(item=MybookScrapperItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath("name", "//div[@class='m4n24q-0 hJyrxa']/h1/text()")
        loader.add_xpath("author", "//div[@class='m4n24q-0 bkolKJ']/a/div/div/text()")
        loader.add_xpath(
            "time", "//div[@class='ant-col sc-1c0xbiw-9 eSjGMZ']/p[1]/text()"
        )
        loader.add_xpath(
            "size", "//div[@class='ant-col sc-1c0xbiw-9 eSjGMZ']/p[2]/text()"
        )
        loader.add_xpath(
            "year", "//div[@class='ant-col sc-1c0xbiw-9 eSjGMZ']/p[3]/text()"
        )
        loader.add_xpath(
            "age", "//div[@class='ant-col sc-1c0xbiw-9 eSjGMZ']/p[4]/text()"
        )

        link = (
            response.xpath("//div[@class='hh1ehr-0 kkiIwl']/picture/img/@srcset")
            .get()
            .split(",")[0]
        )

        loader.add_value("image_url", link)

        # file_name = link.split("/")[-1]
        # with open(f"{IMAGES_STORE}/{file_name}", "wb") as f:
        #     f.write(response.body)

        yield loader.load_item()
