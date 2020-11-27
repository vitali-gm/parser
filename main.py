import csv
from parser import Parser


URLS = ['https://www.yakaboo.ua/ua/goluboe-salo.html']
FILE = 'product.csv'

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        headers_file = ['Назва', 'Стара ціна', 'Ціна', 'Опис', 'Автор', 'Видавництво', 'Серія книг', 'Мова', 'Рік видання', 'Вік', 'Кількість сторінок', 'Ілюстрації']
        writer.writerow(headers_file)

        for item in items:
            ch = item['characteristics']
            line_item = [item['name'], item['price'].get('old_price', ''), item['price']['price'], item['description'], ch.get('avtor', ''), ch.get('edition', ''), 
            ch.get('series_book', ''), ch.get('lang', ''), ch.get('publish_year', ''), ch.get('age', ''), ch.get('count_pages', ''), ch.get('illustrations', '')]

            for image in item['images']:
                line_item.append(image)
            
            writer.writerow(line_item)


products = []
parser = Parser()
for url in URLS:
    product = parser.get_html(url)
    print(product)
    # products.append(product)

# save_file(products, FILE)
