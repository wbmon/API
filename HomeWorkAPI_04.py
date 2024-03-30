import requests
from lxml import html
import csv

# URL сайта
url = 'https://edu.gov.ru/press/news/'

# Строка агента пользователя для имитации веб-браузера
headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

# Отправка HTTP GET-запроса
response = requests.get(url, headers=headers)

# Проверка статуса ответа
if response.status_code == 200:
    # Парсинг HTML-содержимого
    tree = html.fromstring(response.content)

    # Выражение XPath для выбора элементов данных таблицы
    news_elements = tree.xpath('//h3/ancestor::*[contains(@class,"flex_3")]')

    # Открытие CSV-файла для записи
    with open('news_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Запись заголовков таблицы
        headers = ['Заголовок', 'Тескт новости']
        writer.writerow(headers)

        # Запись данных новостей
        for news in news_elements:
            # Извлечение данных новости из элемента
            title = news.xpath('.//a/text()')[0] if news.xpath('.//a/text()') else ''
            description = news.xpath('.//p/text()')[0] if news.xpath('.//p/text()') else ''

            # Запись данных в CSV-файл
            writer.writerow([title, description])
else:
    print('Ошибка при загрузке страницы:', response.status_code)