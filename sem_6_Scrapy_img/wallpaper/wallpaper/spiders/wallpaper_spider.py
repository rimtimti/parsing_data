import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WallpaperSpiderSpider(CrawlSpider):
    name = "wallpaper_spider"
    allowed_domains = ["ru.wallpaper.mob.org"]
    start_urls = ["https://ru.wallpaper.mob.org/pc/best/"]

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths="//img[@class='image-gallery-image__image']/@src"
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        print(response.url)
