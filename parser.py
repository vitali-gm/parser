import requests
from bs4 import BeautifulSoup
import datetime

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
        if description_block != None: 
            description = description_block.find('div', class_='description-shadow')
            if description != None:
                return description.get_text(strip=True)
        return None

    def get_price_with_block(self, price_block):
        if price_block != None:
            block = price_block.find('span', class_='price')
            price = block.find_all('span')[0].get_text(strip=True)
            return price
        return None

    def get_price(self, price_block):
        if price_block != None:
            regular_price_block = price_block.find('span', class_='regular-price')

            if regular_price_block != None:
                price = self.get_price_with_block(regular_price_block)
                return {'old_price': None, 'price': price}
            else:
                old_price_block = price_block.find('p', class_='old-price')
                old_price = self.get_price_with_block(old_price_block)

                special_price_block = price_block.find('p', class_='special-price')
                special_price = self.get_price_with_block(special_price_block)
                
                return {'old_price': old_price, 'price': special_price}
        return {'old_price': None, 'price': None}
            
    def get_characteristics(self, attributes_block):

        if attributes_block != None:
            attributes = attributes_block.find_all('tr')

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

            return characteristics
        return None
            
    def get_images(self, modal_product_media_block):
        if modal_product_media_block != None:
            lists = modal_product_media_block.find('ul', class_='media-content')
            images_tags = lists.find_all('img')

            images = []

            for image in images_tags:
                images.append(image.get('data-original'))

            return images

    def get_availability(self, availability_block):
        #todo with date
        if availability_block != None:
            availability = availability_block.find('span')
            if availability != None:
                return availability.get_text(strip=True)
            else:
                availability = availability_block.find('div', class_='delivery_count')
                if availability != None:
                    date = availability.get_text(strip=True)
                    d = date.split(".")
                    x = datetime.date(int(d[2]), int(d[1]), int(d[0]))
                    res = x + datetime.timedelta(days=3)
                    return res.strftime("%d-%m-%Y")
        return None

    def get_content(self, html):
        soap = BeautifulSoup(html, 'html.parser')
        modal_product_media_block = soap.find('div', class_='modal_product-media')

        if modal_product_media_block != None:
            container = soap.find('div', class_='wrapper')
            attributes_block = container.find('div', class_='product-attributes')
            breadcrumb_block = container.find('ul', class_='breadcrumb')
            description_block = container.find('div', class_='big-description')
            price_block = container.find('div', class_='price-box')
            availability_block = container.find('div', class_='availability')

            product_name = container.find('div', class_='product-name').get_text() #todo
            breadcrumbs = self.get_breadcrumb(breadcrumb_block)
            characteristics = self.get_characteristics(attributes_block)
            description = self.get_description(description_block)
            price = self.get_price(price_block)
            images = self.get_images(modal_product_media_block)
            availability = self.get_availability(availability_block)

            product = {
                'name': product_name,
                'breadcrumbs': breadcrumbs,
                'description': description,
                'price': price,
                'characteristics': characteristics,
                'images': images,
                'availability': availability
            }

            return product
        return None