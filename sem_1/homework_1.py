# Сценарий Foursquare
# Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию
# (например, кофейни, музеи, парки и т.д.).
# Используйте API Foursquare для поиска заведений в указанной категории.
# Получите название заведения, его адрес и рейтинг для каждого из них.
# Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.

import requests

KEY = "fsq3JVybUFf/EMfqxyL3KyAuLBxX3pawQdCTzBO5TwrqMNk="    
URL = "https://api.foursquare.com/v3/places/search"

print("Это сценарий, который предложит пользователю ввести на английском языке интересующую его категорию\n\
(например, coffee, sport, airport и т.д.).\nИспользуется API Foursquare для поиска заведений в указанной категории.\n\
Используется локализация пользователя. Будет выведено: категория заведения, название и адрес\n")

temp = input("Введите категорию: ")


params = {
  	"query": temp,
  	"open_now": "true",
  	"sort":"DISTANCE"
}

headers = {
    "Accept": "application/json",
    "Authorization": KEY
}

response = requests.request("GET", URL, headers=headers, params=params)
data = response.json()["results"]

for i in range(len(data)):
	category = data[i]["categories"][0]["name"]
	name = data[i]["name"]
	address = data[i]["location"]["formatted_address"]
 
	print(f"{category} - {name} => {address}")
