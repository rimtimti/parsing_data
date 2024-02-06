# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
# и извлечь информацию о всех книгах на сайте во всех категориях:
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.

from random import randint
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json

HOST = "https://books.toscrape.com"
url = HOST + "/index.html"

data = []
while True:
    # Запрос веб-страницы
    response = requests.get(url)

    # Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # ищем на странице ссылку на следующую страницу
    try:
        next_page_link = soup.find("li", {"class": "next"}).find("a").get("href")
    except:
        next_page_link = ""

    # на этом сайте с 3-й страницы линки без /catalogue/ и все товары тоже
    if re.sub(r"[^\d]+", "", next_page_link) == "3":
        HOST += "/catalogue/"

    # Поиск ссылок на отдельные продукты
    release_links = []

    for link in soup.find_all("div", ("class", "image_container")):
        a_tag = link.find("a")
        if a_tag:
            release_links.append(a_tag.get("href"))

    # Объединение ссылок с базовым URL-адресом для создания списка URL-адресов
    url_joined = [urllib.parse.urljoin(HOST, link) for link in release_links]

    # открываем каждую ссылку и парсим данные товара в словарь
    for url in url_joined:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            },
        )
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            name = soup.find("li", {"class": "active"}).text
        except:
            name = ""

        try:
            price_in_pounds = float(soup.find("p", {"class": "price_color"}).text[1::])
        except:
            price_in_pounds = ""

        try:
            temp = soup.find("p", {"class": "instock availability"}).text
            in_stock = int(re.sub(r"[^\d.]+", "", temp))
        except:
            in_stock = ""

        try:
            description = soup.find("p", {"class": ""}).text
        except:
            description = ""

        row_data = {
            "name": name,
            "price_in_pounds": price_in_pounds,
            "in_stock": in_stock,
            "description": description,
        }

        data.append(row_data)
        time.sleep(randint(10, 20))

    # если следующей страницы нет, конец цикла, иначе дальше
    if next_page_link == "":
        break
    else:
        url = urllib.parse.urljoin(HOST, next_page_link)


# сохранение данных в JSON-файл
with open("books_toscrape_com_data.json", "w") as f:
    json.dump(data, f)
