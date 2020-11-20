import requests
from bs4 import BeautifulSoup

class Parser:

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36', 'accept': '*/*'}

    def get_html(self, url, params=None):
        html = requests.get(url, headers=self.headers, params=params)
        if html.status_code == 200:
            return self.get_content(html.text)
        return None
        
    def get_breadcrumb(self, breadcrumb):
        breadcrumbs = []

        items = breadcrumb.find_all('li')

        for item in items: 
            text = item.find("span").get_text(strip=True)
            breadcrumbs.append(text)

        return breadcrumbs

    def get_description(self, description_block):
        return description_block.find('div', class_='description-shadow').get_text(strip=True)

    def get_price_with_block(self, price_block):
        block = price_block.find('span', class_='price')
        price = block.find_all('span')[0].get_text(strip=True)
        return price

    def get_price(self, price_block):
        regular_price_block = price_block.find('span', class_='regular-price')

        if regular_price_block != None:
            price = self.get_price_with_block(regular_price_block)
            return {'price': price}
        else:
            old_price_block = price_block.find('p', class_='old-price')
            old_price = self.get_price_with_block(old_price_block)

            special_price_block = price_block.find('p', class_='special-price')
            special_price = self.get_price_with_block(special_price_block)

            
            return {'old_price': old_price, 'price': special_price}
            
    def get_characteristics(self, attributes):
        characteristics = {}

        for item in attributes:
            params = item.find_all('td')

            key = ''
            if params[0].get_text(strip=True) == 'Автор':
                key = 'avtor'
            elif params[0].get_text(strip=True) == 'Видавництво':
                key = 'edition'
            elif params[0].get_text(strip=True) == 'Серія книг':
                key = 'series_book'
            elif params[0].get_text(strip=True) == 'Мова':
                key = 'lang'
            elif params[0].get_text(strip=True) == 'Рік видання':
                key = 'publish_year'
            elif params[0].get_text(strip=True) == 'Вік':
                key = 'age'
            elif params[0].get_text(strip=True) == 'Кількість сторінок':
                key = 'count_pages'
            elif params[0].get_text(strip=True) == 'Ілюстрації':
                key = 'illustrations'

            characteristics[key] = params[1].get_text(strip=True)

            # characteristics.append({
            #     'name': params[0].get_text(strip=True),
            #     'value': params[1].get_text(strip=True),
            # })

        return characteristics
            
    def get_images(self, modal_product_media_block):
        lists = modal_product_media_block.find('ul', class_='media-content')
        images_tags = lists.find_all('img')

        images = []

        for image in images_tags:
            images.append(image.get('data-original'))

        return images

    def get_content(self, html):
        soap = BeautifulSoup(html, 'html.parser')

        container = soap.find('div', class_='wrapper')

        attributes_block = container.find('div', class_='product-attributes').find_all('tr')

        breadcrumb_block = container.find('ul', class_='breadcrumb')

        description_block = container.find('div', class_='big-description')

        price_block = container.find('div', class_='price-box')

        modal_product_media_block = soap.find('div', class_='modal_product-media')

        product_name = container.find('div', class_='product-name').get_text()
        breadcrumbs = self.get_breadcrumb(breadcrumb_block)
        characteristics = self.get_characteristics(attributes_block)
        description = self.get_description(description_block)
        price = self.get_price(price_block)
        images = self.get_images(modal_product_media_block)

        product = {
        'name': product_name,
        'breadcrumbs': breadcrumbs,
        'description': description,
        'price': price,
        'characteristics': characteristics,
        'images': images
        }

        return product