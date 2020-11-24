import csv
from parser import Parser


URLS = ['https://www.yakaboo.ua/ua/lis-timko-ta-jogo-sad.html']
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
i = 1
for url in URLS:
    product = parser.get_html(url)
    print(product)
    products.append(product)
    print('Number product ' + str(i))
    i += 1
# save_file(products, FILE)
