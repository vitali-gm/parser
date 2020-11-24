import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36', 'accept': '*/*'}

url = 'https://www.yakaboo.ua/ua/book_publisher/view/all/?lng=ukrainian'

html = requests.get(url, headers=headers)

if html.status_code == 200:
    soap = BeautifulSoup(html.text, 'html.parser')
    container = soap.find('table', class_='authors-catalog__table')

    links = []
    a_tags = container.find_all('a')

    for tag in a_tags:
        links.append({
            'href': tag.get('href'),
            'count': tag.next_element.next_element.get_text().strip('()')
        })

for link in links:
    # todo paginations
    html = requests.get(link['href'], headers=headers)

    if html.status_code == 200:
        soap = BeautifulSoup(html.text, 'html.parser')
        container = soap.find('ul', class_='products-grid')

        items_tags = container.find_all('div', class_='content')
        urls = []
        for item in items_tags:
            print(item.find('a').get('href'))