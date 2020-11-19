import requests
from bs4 import BeautifulSoup



URL = 'https://www.yakaboo.ua/ua/biologija-kompleksna-pidgotovka-do-zno.html'
# URL = 'https://www.yakaboo.ua/ua/biologija-tipovi-testovi-zavdannja-zno-2021.html'

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_breadcrumb(breadcrumb):
    breadcrumbs = []

    items = breadcrumb.find_all('li')

    for item in items: 
        text = item.find("span").get_text(strip=True)
        breadcrumbs.append(text)

    return breadcrumbs

def get_description(description_block):
    return description_block.find('div', class_='description-shadow').get_text(strip=True)

def get_price_with_block(price_block):
    block = price_block.find('span', class_='price')
    price = block.find_all('span')[0].get_text(strip=True)
    return price

def get_price(price_block):
    regular_price_block = price_block.find('span', class_='regular-price')

    if regular_price_block != None:
        price = get_price_with_block(regular_price_block)
        return {'price': price}
    else:
        old_price_block = price_block.find('p', class_='old-price')
        old_price = get_price_with_block(old_price_block)

        special_price_block = price_block.find('p', class_='special-price')
        special_price = get_price_with_block(special_price_block)

        
        return {'old_price': old_price, 'special_price': special_price}
        
def get_characteristics(attributes):

    characteristics = []

    for item in attributes:
        params = item.find_all('td')

        characteristics.append({
            'name': params[0].get_text(strip=True),
            'value': params[1].get_text(strip=True),
        })

    return characteristics
        
def get_images(modal_product_media_block):

    lists = modal_product_media_block.find_all('ul')

    for list in lists:
        images = list.find_all('img')
        if images != None:
            print(images[1])
       
        break


def get_content(html):
    soap = BeautifulSoup(html, 'html.parser')

    container = soap.find('div', class_='wrapper')

    attributes_block = container.find('div', class_='product-attributes').find_all('tr')

    breadcrumb_block = container.find('ul', class_='breadcrumb')

    description_block = container.find('div', class_='big-description')

    price_block = container.find('div', class_='price-box')

    modal_product_media_block = soap.find('div', class_='modal_product-media')

    product_name = container.find('div', class_='product-name').get_text()
    breadcrumbs = get_breadcrumb(breadcrumb_block)
    characteristics = get_characteristics(attributes_block)
    description = get_description(description_block)
    price = get_price(price_block)

    # get_images(modal_product_media_block)



def parse():
    html = get_html(URL)
    if html.status_code == 200:

        get_content(html.text)

    else: 
        print('EROOR')


parse()