import requests
import csv
from classes.parser_avtor import Parser


def read_ids():
    with open('files/ids.csv', newline='') as csvfile:
        ids = []
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            ids.append(row[0])
        return ids

def scan(ids):
    parser = Parser()

    with open('files/avtors.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        headers_file = [
            'fullname',
            'birthday',
            'text'
        ]
        for i in range(10):
            headers_file.append('thumbnail' + str(i + 1))
        writer.writerow(headers_file)

        number = 1
        count = 1

        for id in ids:
            print(str(count) + ' | ' + str(number) + ' | ' + id)
            href = 'https://www.yakaboo.ua/ua/search/?multi=0&cat=&q=' + str(id) 
            avtors = parser.get_avtors(href)
            for avtor in avtors:
                line_item = [
                    avtor['info'].get('full_name', ''),
                    avtor['info'].get('birthday', ''),
                    avtor['text']
                ]

                for image in avtor['images']:
                    line_item.append(image)
                
                writer.writerow(line_item)
                number += 1
            count += 1
            
ids = read_ids()
scan(ids)