import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, time, timedelta
import time
import re
import json

HOST = "https://www.boxofficemojo.com"

# Запрос веб-страницы
url = HOST + "/intl/?ref_=bo_nb_hm_tab"
response = requests.get(url)

# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Поиск ссылок на отдельные продукты
release_links = []
tag = 'td'
class_name = 'a-text-left mojo-field-type-release mojo-cell-wide'

for link in soup.find_all(tag, ('class', class_name)):
    a_tag = link.find("a")
    if a_tag:
        release_links.append(a_tag.get('href'))

# Объединение ссылок с базовым URL-адресом для создания списка URL-адресов
url_joined = [urllib.parse.urljoin(HOST, link) for link in release_links]
   

data = []
for url in url_joined:
    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', {'class': 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})
    rows = table.find_all('div', {'class': 'a-section a-spacing-none'})

    row_data={}
    for row in rows:
        key = row.find('span').text.strip()
        value = row.find_all('span')[1].text.strip()
        if key == 'Opening':
            value = int(re.sub('[^0-9]', '', value))
        elif key == 'Release Date':
            value = value
        elif key == 'Running Time':
            time_delta = datetime.strptime(value, '%H hr %M min') - datetime(1900, 1, 1)
            value = time_delta.total_seconds()
        elif key == 'Genres':
            value = [genre.strip() for genre in value.split('\n') if genre.strip()]
        elif key == 'In Release':
            value = value.replace(' days/3 weeks', '').strip()
        elif key == 'Widest Release':
            value = int(re.sub('[^0-9]', '', value))
        
        row_data[key] = value
    
    data.append(row_data)
    time.sleep(10)

# сохранение данных в JSON-файл
with open('box_office_data.json', 'w') as f:
    json.dump(data, f)