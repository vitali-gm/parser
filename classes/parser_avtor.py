import requests
from bs4 import BeautifulSoup
import datetime
import time

class Parser:

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36', 'accept': '*/*'}

    def get_html(self, url, params = None):
        try:
            html = requests.get(url, headers=self.headers, params=params)
            if html.status_code == 200:
                return html.text
            return None
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
            print('time sleep')
            time.sleep(10)
            return self.get_html(url, params=params)
        except requests.exceptions.MissingSchema:
            return None
    
    def get_content(self, html):
        if html != None:
            soap = BeautifulSoup(html, 'html.parser')
            modal_product_media_block = soap.find('div', class_='modal_product-media')

            if modal_product_media_block != None:
                container = soap.find('div', class_='wrapper')
                return container.find('table', class_='product-attributes__table')
        return None

    def get_info(self, block):
        info_block_array = block.find_all('tr')
        info = {}
        for item in info_block_array:
            params = item.find_all('td')
            key = ''
            if params[0].get_text(strip=True) == 'Повне ім\'я:':
                key = 'full_name'
            elif params[0].get_text(strip=True) == 'Дата народження:':
                key = 'birthday'
            info[key] = params[1].get_text(strip=True)
        return info

    def get_images(self, block):
        images = []

        images_block = block.find_all('img')
        for item in images_block:
            images.append(item.get('data-original'))
        return images

    def get_avtor(self, url):
        try:
            html = requests.get(url, headers=self.headers)
            if html.status_code == 200:
                soap = BeautifulSoup(html.text, 'html.parser')
                block = soap.find('div', class_='main-container')

                data_block = block.find('div', class_='product-shop span6')
                if data_block != None:
                    image_block = block.find('ul', class_='media-content')

                    info_block = data_block.find('div', class_='product-attributes')
                    info = self.get_info(info_block)

                    text_block = data_block.find('section', class_='full_html')
                    text_block_array = text_block.find_all('p')
                    text = ''
                    for text_block_item in text_block_array:
                        text += text_block_item.get_text()

                    images = self.get_images(image_block)
                    
                    return {
                        'info': info,
                        'text': text,
                        'images': images
                    }
            return None
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
            print('time sleep')
            time.sleep(10)
            return self.get_avtor(url)
        except requests.exceptions.MissingSchema:
            return None

    def get_avtors(self, url):
        html = self.get_html(url)
        content = self.get_content(html)
        avtors = []
        names = []
        if content != None:
            attribute = content.find('tr')
            links = attribute.find_all('a')
            for link_tag in links:
                href = link_tag.get('href')
                name = link_tag.get_text(strip=True)
                if not name in names:
                    names.append(name)
                    avtor = self.get_avtor(href)
                    if avtor != None:
                        avtors.append(avtor)
        return avtors