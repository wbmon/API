import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_data_with_selenium(url):
    service = Service()
    driver = webdriver.Chrome(service=service)

    while True:
        try:
            driver.get(url=url)
            time.sleep(2)

            with open("index_selenium.html", "w") as file:
                file.write(driver.page_source)

        except Exception as ex:
            print(ex)

        with open("index_selenium.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        hotels_cards = soup.find_all("div", class_="reviews-travel__item")

        hotels_data = []

        for hotel in hotels_cards:
            hotel_title = hotel.find("div", class_="h4").text.strip() if hotel.find("div", class_="h4") else ""
            hotel_reviews = hotel.find("div", class_="reviews-travel__text").text.strip() if hotel.find("div",
                                                                                                        class_="reviews-travel__text") else ""
            hotel_url = hotel.find("a").get("href") if hotel.find("a") else ""

            # Создаем словарь с данными отеля
            hotel_dict = {
                "title": hotel_title,
                "reviews": hotel_reviews,
                "url": hotel_url
            }

            # Добавляем словарь в список
            hotels_data.append(hotel_dict)

        # Открываем файл для чтения и загружаем существующие данные
        try:
            with open("hotels.json", "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        # Объединяем существующие данные с новыми
        existing_data.extend(hotels_data)

        # Открываем файл для записи и сохраняем обновленные данные
        with open("hotels.json", "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        try:
            pagination_next = driver.find_element(By.CLASS_NAME, "pagination-next")
            if pagination_next:
                url = pagination_next.get_attribute('href')
        except:
            break


def main():
    # Пробовал разные сценарии
    # get_data_with_selenium("https://www.tury.ru/hotel/?cn=0&ct=0&cat=1317&txt_geo=&srch=&s=0")
    get_data_with_selenium("https://www.tury.ru/hotel/?cat=1320")


if __name__ == '__main__':
    main()
