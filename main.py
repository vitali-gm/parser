import csv
from parser import Parser


URLS = ['https://www.yakaboo.ua/ua/toreadori-z-vasjukivki.html', 'https://www.yakaboo.ua/ua/velike-misto-malen-kij-zajchik-abo-med-dlja-mami.html', 'https://www.yakaboo.ua/ua/charlie-and-the-chocolate-factory.html', 'https://www.yakaboo.ua/ua/trista-poezij.html', 'https://www.yakaboo.ua/ua/charli-i-velikij-skljanij-lift.html', 'https://www.yakaboo.ua/ua/matilda.html', 'https://www.yakaboo.ua/ua/fantastichnij-mister-lis.html', 'https://www.yakaboo.ua/ua/bukova-zemlja.html', 'https://www.yakaboo.ua/ua/agencija-lokvud-i-k-cherep-scho-shepoche.html', 'https://www.yakaboo.ua/ua/vid-mi-1502878.html', 'https://www.yakaboo.ua/ua/garri-potter-i-kelih-vognju-iljustrovane-vidannja.html', 'https://www.yakaboo.ua/ua/shustrik-1375664.html', 'https://www.yakaboo.ua/ua/vdv-velikij-druzhnij-veleten.html', 'https://www.yakaboo.ua/ua/sherlok-golms-povne-vidannja-komplekt-z-2-knig.html', 'https://www.yakaboo.ua/ua/velika-iljustrovana-kniga-kazok.html', 'https://www.yakaboo.ua/ua/harry-potter-and-the-deathly-hallows.html', 'https://www.yakaboo.ua/ua/fantastichni-zviri-zlochini-grindel-val-da.html', 'https://www.yakaboo.ua/ua/garri-potter-i-v-jazen-azkabanu-iljustrovane-vidannja.html', 'https://www.yakaboo.ua/ua/james-and-the-giant-peach.html', 'https://www.yakaboo.ua/ua/harry-potter-and-the-prisoner-of-azkaban.html', 'https://www.yakaboo.ua/ua/harry-potter-and-the-halfblood-prince.html', 'https://www.yakaboo.ua/ua/antologija-ukrains-koi-poezii-hh-stolittja-vid-tichini-do-zhadana.html', 'https://www.yakaboo.ua/ua/harry-potter-and-the-order-of-the-phoenix.html', 'https://www.yakaboo.ua/ua/harry-potter-and-the-goblet-of-fire.html', 'https://www.yakaboo.ua/ua/nezvichajni-prigodi-ali.html', 'https://www.yakaboo.ua/ua/uljubleni-virshi-tom-3.html', 'https://www.yakaboo.ua/ua/zapiski-ukrains-kogo-samashedshogo.html', 'https://www.yakaboo.ua/ua/uljubleni-virshi-u-2-tomah-tom-2.html', 'https://www.yakaboo.ua/ua/the-tales-of-beedle-the-bard.html', 'https://www.yakaboo.ua/ua/fantastichni-zviri-i-de-ih-shukati-original-nij-scenarij.html', 'https://www.yakaboo.ua/ua/taemnicja-kozac-koi-shabli-1876831.html', 'https://www.yakaboo.ua/ua/korotkij-kurs-istorii-ukraini.html', 'https://www.yakaboo.ua/ua/litachok-rjativnichok-1243580.html', 'https://www.yakaboo.ua/ua/garri-potter-istorija-magii.html', 'https://www.yakaboo.ua/ua/nich-pered-rizdvom-1011880.html', 'https://www.yakaboo.ua/ua/ivan-sila-nejmovirni-prigodi.html', 'https://www.yakaboo.ua/ua/the-tragicall-historie-of-hamlet-prince-of-denmarke-1037350.html', 'https://www.yakaboo.ua/ua/galereja-kotiv-kototeka-okul-turenih-kotiv.html', 'https://www.yakaboo.ua/ua/100-kazok-najkraschi-ukrains-ki-narodni-kazki-tom-2.html', 'https://www.yakaboo.ua/ua/fantastichni-zviri-i-de-ih-shukati-velike-iljustrovane-vidannja.html', 'https://www.yakaboo.ua/ua/zbagnuti-rosiju-svidchennja-ochevidciv.html', 'https://www.yakaboo.ua/ua/bartimeus-kniga-1-amulet-samarkanda.html', 'https://www.yakaboo.ua/ua/chudove-chudovis-ko-u-3-knigah-kniga-1.html', 'https://www.yakaboo.ua/ua/romeo-i-dzhul-etta-1428213.html', 'https://www.yakaboo.ua/ua/100-kazok-najkraschi-ukrains-ki-narodni-kazki-tom-3.html', 'https://www.yakaboo.ua/ua/med-i-pashtet-fantastichni-vitrogoni.html', 'https://www.yakaboo.ua/ua/pidlitkam-pro-golovne-vse-scho-cikavit-hlopciv-ta-divchat.html', 'https://www.yakaboo.ua/ua/kazki-drakona-omel-ka.html']

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
    products.append(product)
    print('Number product ' + str(i))
    i += 1
save_file(products, FILE)
