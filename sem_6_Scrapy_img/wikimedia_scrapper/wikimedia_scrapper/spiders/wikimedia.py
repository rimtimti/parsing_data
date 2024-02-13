import scrapy
from wikimedia_scrapper.settings import IMAGES_STORE


class WikimediaSpider(scrapy.Spider):
    name = "wikimedia"
    # allowed_domains = ["www.commons.wikimedia.org"]
    start_urls = [
        "https://commons.wikimedia.org/wiki/Category:Featured_pictures_on_Wikimedia_Commons"
    ]

    def parse(self, response):
        for image in response.xpath(
            '//*[@id="mw-category-media"]/ul/li/div[1]/span/a/img'
        ):
            image_url = image.xpath("@src").extract_first()
            yield scrapy.Request(response.urljoin(image_url), self.save_image)

    def save_image(self, response):
        file_name = response.url.split("/")[-1]
        with open(f"{IMAGES_STORE}/{file_name}", "wb") as f:
            f.write(response.body)
