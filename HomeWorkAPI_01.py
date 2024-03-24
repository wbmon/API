import requests
import json
import os
import sys
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
city = input("Введите название города: ")

print("Введите номер категории:")
while True:
    print('''        1. Музеи
        2. Кафе
        3. Рестораны
        4. Парки
        5. Развлечения
        6. Покупки
        0. Выйти из программы''')
    cmd = input("Выберите пункт: ")
    
    if cmd == "1":
        select = "Музеи"
        break
    elif cmd == "2":
        select = "Кафе"
        break
    elif cmd == "3":
        select = "Рестораны"
        break
    elif cmd == "4":
        select = "Парки"
        break
    elif cmd == "5":
        select = "Развлечения"
        break
    elif cmd == "6":
        select = "Покупки"
        break
    elif cmd == "0":
        select = ""
        break
    else:
        print("Вы ввели не правильное значение")

if select == "": sys.exit()

params = {
    "client_id": os.getenv("client_id"),
    "client_secret": os.getenv("client_secret"),
    "near": city,
    "query": select
}

headers = {
    "Accept": "application/json",
    "Authorization": os.getenv("auth")
}

# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params,headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    print("_"*30)
    data = json.loads(response.text)
    venues = data["results"]

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    for venue in venues:
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["formatted_address"])
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
