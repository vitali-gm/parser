import csv
from parser import Parser


URLS = ['https://www.yakaboo.ua/ua/sem-smertej-jeveliny-hardkasl-2220673.html']
FILE = 'product.csv'

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        headers_file = ['id', 'category1', 'category2', 'category3', 'name', 'desc', 'regular_price', 'price', 'authot', 'edition', 'series_book', 'lang', 'publish_year', 'age', 'count_pages', 'illustrations']
        for i in range(30):
            headers_file.append('thumbnail' + str(i + 1))
        writer.writerow(headers_file)

        number_id = 6800

        for item in items:
            ch = item['characteristics']
            line_item = [number_id ,item['breadcrumbs'][2], item['breadcrumbs'][3], item['breadcrumbs'][4], item['name'], item['description'], item['price'].get('old_price', ''), item['price']['price'], ch.get('avtor', ''), ch.get('edition', ''), 
            ch.get('series_book', ''), ch.get('lang', ''), ch.get('publish_year', ''), ch.get('age', ''), ch.get('count_pages', ''), ch.get('illustrations', '')]

            for image in item['images']:
                line_item.append(image)
            
            writer.writerow(line_item)
            number_id += 1


products = []
parser = Parser()
for url in URLS:
    product = parser.get_html(url)
    print(product)
    products.append(product)

save_file(products, FILE)
