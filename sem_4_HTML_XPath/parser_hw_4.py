import requests
from lxml import html
from pymongo import MongoClient
import time

# url = "https://www.imdb.com/chart/boxoffice/"

# Функция для скрейпинга табличных данных со страницы
def scrape_page_data(url):
    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
    tree = html.fromstring(response.content)

    table_rows = tree.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-between sc-71ed9118-0 kxsUNk compact-list-view ipc-metadata-list--base']/li/div[@class='ipc-metadata-list-summary-item__c']//div[@class='ipc-metadata-list-summary-item__tc']/div[@class='sc-be6f1408-0 gVGktK cli-children']")

    data = []
    for row in table_rows:
        gross = row.xpath(".//ul/li/span[@class='sc-8f57e62c-2 elpuzG']/text()")
        vote = row.xpath(".//span/div/span/span/text()")[1].strip()
        vote = float(vote[:-1])*1000 if vote[:-2:-1] == "K" else vote
        data.append({
            'name': row.xpath(".//div/a/h3/text()")[0][3::].strip(),
            'weekend_gross_mln_dollars': float(gross[0][1:-1].strip()),
            'total_gross_mln_dollars': float(gross[1][1:-1].strip()),
            'weeks_released': int(gross[2].strip()),
            'rating': float(row.xpath(".//span/div/span/text()")[0].strip()),
            'vote_count': int(vote),
        })
    return data


# print(scrape_page_data(url))


# Функция для сохранения данных в MongoDB
def save_data_to_mongo(data):
    client = MongoClient('localhost', 27017)
    db = client['imdb_com']
    collection = db['chart_boxoffice']
    collection.insert_many(data)

# Main function
def main():
    url = "https://www.imdb.com/chart/boxoffice/"

    # for page in range(1, 7):
    #     print(f"Scraping page {page}...")
    #     url = base_url + str(page)
    data = scrape_page_data(url)
    save_data_to_mongo(data)
    # time.sleep(5)

if __name__ == "__main__":
    main()