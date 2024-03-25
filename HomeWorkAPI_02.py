import requests
from bs4 import BeautifulSoup
import json

# Отправляем GET-запрос к веб-сайту
url = "http://books.toscrape.com/"
response = requests.get(url)

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Извлекаем информацию о книгах
books_info = []

# Находим все ссылки на книги
book_urls = [url + x.a['href'] for x in soup.find_all('h3')]

for book_url in book_urls:
    book_response = requests.get(book_url)
    book_soup = BeautifulSoup(book_response.content, 'html.parser')
    
    title = book_soup.h1.text
    price = float(book_soup.find('p', class_='price_color').text.replace('£', ''))
    stock = int(book_soup.find('p', class_='instock availability').text.split()[2][1:])
    instock = 'In stock (' + str(stock) +' available)'
    description = book_soup.find('meta', {'name': 'description'})['content']

    book_info = {
        'title': title,
        'price': price,
        'stock': instock,
        'description': description
    }

    books_info.append(book_info)

# Сохраняем информацию в JSON-файле
with open('books_info.json', 'w') as f:
    json.dump(books_info, f, indent=4)

print("Информация о книгах сохранена в файле books_info.json")