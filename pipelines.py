# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface


import csv
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request


class PhotoPipeline():
    def open_spider(self, spider):
        # Открываем файл для записи данных в формате CSV
        self.file = open("photo.csv", "w", newline='', encoding='utf-8')
        self.items = []

    def close_spider(self, spider):
        # Если список не пуст, то записываем данные в CSV файл
        if self.items:
            # Получаем все ключи из первого элемента списка
            fieldnames = self.items[0].keys()
            writer = csv.DictWriter(self.file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.items)
        self.file.close()

    def process_item(self, item, spider):
        # Добавляем элемент в список для последующей записи в CSV файл
        self.items.append(ItemAdapter(item).asdict())
        return item


class PhotoSavePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # Если у элемента есть URL, то создаем запрос на скачивание изображения
        if item['url']:
            yield Request(item['url'])

    def item_completed(self, results, item, info):
        # Если результаты запроса были успешными, то добавляем путь к изображению в элемент
        if results:
            item['image_path'] = [itm[1]['path'] for itm in results if itm[0]][0]
        return item
