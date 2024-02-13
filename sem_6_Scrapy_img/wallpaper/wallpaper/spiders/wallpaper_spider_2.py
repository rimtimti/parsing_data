import scrapy
from wallpaper.settings import IMAGES_STORE


class WallpaperSpider2Spider(scrapy.Spider):
    name = "wallpaper_spider_2"
    # allowed_domains = ["ru.wallpaper.mob.org"]
    start_urls = ["https://ru.wallpaper.mob.org/best/"]

    def parse(self, response):
        for image in response.xpath("//img[@class='image-gallery-image__image']"):
            if image.xpath("@src").extract_first():
                image_url = image.xpath("@src").extract_first()
            else:
                image_url = image.xpath("@data-src").extract_first()

            yield scrapy.Request(response.urljoin(image_url), self.save_image)

    def save_image(self, response):
        file_name = response.url.split("/")[-1]
        with open(f"{IMAGES_STORE}/{file_name}", "wb") as f:
            f.write(response.body)
