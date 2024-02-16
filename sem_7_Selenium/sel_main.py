import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://mybook.ru/tags/russkaya-fantastika/")

buttons = driver.find_elements(
    By.XPATH, "//li[@class='ant-menu-item sc-1oz7ss8-10 SQpMX']"
)

buttons[5].click()
buttons[7].click()


while True:
    try:
        next = driver.find_element(By.XPATH, "//div[@class='m4n24q-0 bkolKJ']/a")
        time.sleep(10)
        next.click()
    except:
        data = driver.find_elements(By.XPATH, "//div[@class='e4xwgl-1 gEQwGK']/a")

        links = []

        for el in data:
            url = el.get_attribute("href")
            links.append(url)
        break

driver.close()

data = []

for url in links:
    time.sleep(10)

    # Запрос веб-страницы
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        },
    )

    # Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        name = soup.find("h1", {"level": "h1"}).text
    except:
        name = ""

    try:
        author = soup.find("div", {"class": "dey4wx-1 jVKkXg"}).text
    except:
        author = ""

    temp = soup.find("div", {"class": "ant-col sc-1c0xbiw-9 eSjGMZ"}).text.split()

    try:
        pages = int(re.sub(r"[^\d.]+", "", temp[0]))
    except:
        pages = ""

    try:
        time_to_read_in_hours = int(re.sub(r"[^\d.]+", "", temp[-3]))
    except:
        time_to_read_in_hours = ""

    try:
        release = int(re.sub(r"[^\d.]+", "", temp[-2]))
    except:
        release = ""

    try:
        age_from = int(re.sub(r"[^\d.]+", "", temp[-1]))
    except:
        age_from = ""

    temp = soup.find("div", {"class": "ant-col sc-1c0xbiw-5 lotch"}).text.split()

    try:
        rating = float(re.sub(r"[^\d.]+", "", temp[0]))
    except:
        rating = ""

    try:
        votes = int(re.sub(r"[^\d.]+", "", temp[1]))
    except:
        votes = ""

    row_data = {
        "name": name,
        "author": author,
        "time_to_read_in_hours": time_to_read_in_hours,
        "release": release,
        "age_from": age_from,
        "rating": rating,
        "votes": votes,
    }
    data.append(row_data)

# # сохранение данных в JSON-файл
with open("books_from_mybook.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
