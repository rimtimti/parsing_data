# - использовать библиотеку requests в Python для отправки запросов GET, POST, PUT и DELETE
#               на конечную точку REST API https://jsonplaceholder.typicode.com/posts/1.
# - использовать методы requests.get(), requests.post(), requests.put() и requests.delete()
#               для отправки соответствующих HTTP-запросов.
# - проверить код состояния ответа и вывести текст ответа, если запрос был успешным.

# Инструкции:
# можно использовать предоставленный код в качестве отправной точки для своего решения.

import requests


url = "https://jsonplaceholder.typicode.com/posts/1"

# response = requests.get(url)
# if response.status_code // 100 == 2:
#     print("запрос успешен")
#     print(response.text)

# data = {"title": "name_1", "body": "body_1", "userId": 1}
# response = requests.post(url[:-2], json=data)
# if response.status_code // 100 == 2:
#     print("запрос успешен")
#     print(response.text)

# data = {"title": "name_2", "body": "body_2", "userId": 1, "put": "put"}
# response = requests.put(url, json=data)
# if response.status_code // 100 == 2:
#     print("запрос успешен")
#     print(response.text)

response = requests.delete(url)
if response.status_code // 100 == 2:
    print("запрос успешен")
    print(response.text)
