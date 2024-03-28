from pymongo import MongoClient
import json

# создание экземпляра клиента
client = MongoClient()

# подключение к базе данных и коллекции
db = client['books_data']
collection = db['books']

# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]

# Вывод объекта JSON
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

# Использование оператора $lt и $gte
query = {"price": {"$lt": 30}}
print(f"Количество книг дешевле 30: {collection.count_documents(query)}")
query = {"price": {"$gte": 30}}
print(f"Количество книг дороже или равно 30: {collection.count_documents(query)}")

# Использование оператора $regex
query = {"stock": {"$regex": "In stock", "$options": "i"}}
print(f"Количество документов, содержащих 'In': {collection.count_documents(query)}")