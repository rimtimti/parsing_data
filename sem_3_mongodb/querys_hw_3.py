from pymongo import MongoClient
import json

# создание экземпляра клиента
client = MongoClient()

# подключение к базе данных и коллекции
db = client["books_toscrape_com"]
collection = db["scrape"]

# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[200]

# Вывод объекта JSON
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f"Число записей в базе данных: {count}")

# # # фильтрация документов по критериям
# query = {"properties.fatalities": "Yes"}
# print(f"Количество документов c категорией fatalities: {collection.count_documents(query)}")

# # # Использование проекции
# query = {"properties.fatalities": "Yes"}
# projection = {"properties.lightcond": 1, "properties.weather": 1, "_id": 0}
# proj_docs = collection.find(query, projection)
# for doc in proj_docs:
#     print(doc)

# Использование оператора $lt и $gte
query = {"price_in_pounds": {"$lt": 30}}
print(f"Количество книг c price < 30: {collection.count_documents(query)}")
query = {"price_in_pounds": {"$gte": 30}}
print(f"Количество книг c price >= 30: {collection.count_documents(query)}")

# Использование оператора $lt и $gte
query = {"in_stock": {"$lt": 10}}
print(f"Количество книг в наличии < 10: {collection.count_documents(query)}")
query = {"in_stock": {"$gte": 10}}
print(f"Количество книг в наличии >= 10: {collection.count_documents(query)}")

# Использование оператора $regex
query = {"description": {"$regex": "travel"}}
print(
    f"Количество книг, содержащих в description 'travel': {collection.count_documents(query)}"
)

# Использование оператора $regex
query = {"description": {"$regex": "art"}}
print(
    f"Количество книг, содержащих в description 'art': {collection.count_documents(query)}"
)

# Использование оператора $regex
query = {"name": {"$regex": "Dark"}}
print(f"Количество книг, содержащих в name 'Dark': {collection.count_documents(query)}")

# # Использование оператора $in
# query = {"properties.rdclass": {"$in": ["US ROUTE", "STATE SECONDARY ROUTE"]}}
# print(f"Количество документов в категории rdclass: {collection.count_documents(query)}")

# # Использование оператора $all
# query = {"properties.rdconfigur": {"$all": ["TWO-WAY", "DIVIDED"]}}
# print(f"Количество документов в категории rdconfigur: {collection.count_documents(query)}")

# # Использование оператора $ne
# query = {"properties.rdcondition" : {"$ne": "DRY"}}
# print(f"Количество документов в категории rdcondition: {collection.count_documents(query)}")
