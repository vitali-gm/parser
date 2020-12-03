import requests
from bs4 import BeautifulSoup
import math
from parser import Parser
import csv


def read_ids():
    with open('ids.csv', newline='') as csvfile:
        ids = []
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            ids.append(row[0])
        return ids

def get_breadcrumb(breadcrumbs, key):
    if key <len(breadcrumbs):
        return breadcrumbs[key]
    return ""

def scan(ids):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36', 'accept': '*/*'}

    parser = Parser()

    with open('product.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        headers_file = ['id', 'category1', 'category2', 'category3', 'category4', 'name', 'desc', 'regular_price', 'price', 'authot', 'edition', 'series_book', 'lang', 'publish_year', 'age', 'count_pages', 'illustrations']
        for i in range(30):
            headers_file.append('thumbnail' + str(i + 1))
        writer.writerow(headers_file)

        number = 1

        for id in ids:
            print(str(number) + ' | ' + id)
            href = 'https://www.yakaboo.ua/ua/search/?multi=0&cat=&q=' + str(id) 
            product = parser.get_html(href)
            if product != None:
                ch = product['characteristics']
                breadcrumbs = product['breadcrumbs']
                line_item = [id, get_breadcrumb(breadcrumbs, 2), get_breadcrumb(breadcrumbs, 3), get_breadcrumb(breadcrumbs, 4), get_breadcrumb(breadcrumbs, 5), product['name'], product['description'], product['price']['old_price'], product['price']['price'], ch.get('avtor', ''), ch.get('edition', ''), 
                ch.get('series_book', ''), ch.get('lang', ''), ch.get('publish_year', ''), ch.get('age', ''), ch.get('count_pages', ''), ch.get('illustrations', '')]

                for image in product['images']:
                    line_item.append(image)
                
                writer.writerow(line_item)
                number += 1


ids = read_ids()
scan(ids)