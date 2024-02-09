import scrapy


class SerialsSpiderSpider(scrapy.Spider):
    name = "most_popular_tv_shows"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://imdb.com/chart/tvmeter/?ref_=chttp_ql_5"]

    def parse(self, response):
        for shows in response.xpath(
            "//main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div"
        ):
            current_rank = int(shows.xpath(".//div[1]/text()").get())

            change_rank = shows.xpath(".//div[1]/span/@aria-label").get()
            change_rank = change_rank.split()
            if change_rank[1] == "down":
                change_rank = -1 * int(change_rank[2])
            elif change_rank[1] == "up":
                change_rank = int(change_rank[2])
            else:
                change_rank = 0

            name = shows.xpath(".//div[2]/a/h3/text()").get()

            close = shows.xpath(".//div[3]/span[1]/text()").get()
            open = int(close[:4])
            if len(close) > 4:
                close = close.split("–")
                if close[1] != "" and close[1] != " ":
                    close = int(close[1])
                else:
                    close = ""

            episodes = int(shows.xpath(".//div[3]/span[2]/text()").get()[:-4])

            rating = shows.xpath(".//span/div/span/text()").get()
            if rating != None:
                rating = float(rating)

            votes = shows.xpath(".//span/div/span/span/text()[2]").get()
            if votes != None:
                votes = round(float(votes[:-1]) * 1000)

            if name:
                yield {
                    "current_rank": current_rank,
                    "change_rank": change_rank,
                    "show": name,
                    "open": open,
                    "close": close,
                    "episodes": episodes,
                    "rating": rating,
                    "votes": votes,
                }
