import requests
from bs4 import BeautifulSoup
import math
from parser import Parser
import csv

def get_breadcrumb(breadcrumbs, key):
    if key <len(breadcrumbs):
        return breadcrumbs[key]
    return ""


#todo refactor
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36', 'accept': '*/*'}

parser = Parser()
base_url = 'https://www.yakaboo.ua/ua/book_publisher/view/all/?lng=ukrainian'
html = requests.get(base_url, headers=headers)
if html.status_code == 200:
    soap = BeautifulSoup(html.text, 'html.parser')
    container = soap.find('div', class_='filter-letter')
    list_block = container.find('div', { 'id': 'langtab_ukrainian' })

    with open('product.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        headers_file = ['id', 'category1', 'category2', 'category3', 'category4', 'name', 'desc', 'regular_price', 'price', 'authot', 'edition', 'series_book', 'lang', 'publish_year', 'age', 'count_pages', 'illustrations']
        for i in range(30):
            headers_file.append('thumbnail' + str(i + 1))
        writer.writerow(headers_file)

        number_id = 6800
    
        for a in list_block.find_all('a'):
            html = requests.get(a.get('href'), headers=headers)
            if html.status_code == 200:
                soap = BeautifulSoup(html.text, 'html.parser')
                container = soap.find('table', class_='authors-catalog__table')
                a_tags = container.find_all('a')

                for tag in a_tags:
                    count = int(tag.next_element.next_element.get_text().strip('()'))
                    count_pages = math.ceil(count / 48)
                
                    for page in range(1, count_pages):
                        html = requests.get(tag.get('href'), headers=headers, params={'p': page})
                        print('Page number ' + str(page))

                        if html.status_code == 200:
                            soap = BeautifulSoup(html.text, 'html.parser')
                            container = soap.find('ul', class_='products-grid')

                            items_tags = container.find_all('div', class_='content')
                            urls = []
                            for item in items_tags:
                                print(item.find('a').get('href'))
                                product = parser.get_html(item.find('a').get('href'))
                                if product != None:
                                    ch = product['characteristics']
                                    breadcrumbs = product['breadcrumbs']
                                    line_item = [number_id, get_breadcrumb(breadcrumbs, 2), get_breadcrumb(breadcrumbs, 3), get_breadcrumb(breadcrumbs, 4), get_breadcrumb(breadcrumbs, 5), product['name'], product['description'], product['price']['old_price'], product['price']['price'], ch.get('avtor', ''), ch.get('edition', ''), 
                                    ch.get('series_book', ''), ch.get('lang', ''), ch.get('publish_year', ''), ch.get('age', ''), ch.get('count_pages', ''), ch.get('illustrations', '')]

                                    for image in product['images']:
                                        line_item.append(image)
                                    
                                    writer.writerow(line_item)
                                    number_id += 1
