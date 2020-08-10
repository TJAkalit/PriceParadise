import xlwt
import requests
import bs4

wb = xlwt.Workbook()
ws = wb.add_sheet('List 1')
i = 0
ws.write(i, 0, 'Исследование')                                                                                                       # Заголовки таблицы
ws.write(i, 1, 'Код')
ws.write(i, 2, 'Цена')

jar = requests.cookies.RequestsCookieJar()
jar.set('Region', f'%d0%9d%d0%be%d0%b2%d0%be%d1%80%d0%be%d1%81%d1%81%d0%b8%d0%b9%d1%81%d0%ba', path = '/', domain = '.helix.ru')     # Текущий город поиска цен
jar.set('RegionConfirm', 'Yes', path = '/', domain = '.helix.ru')                                                                    # Берётся из куки 

Session = requests.Session()
response = Session.get('https://helix.ru/catalog', cookies = jar).text

soup = bs4.BeautifulSoup(response, 'html.parser')
catalog = soup.find('div', {'class': 'Catalog-Content-Nomenclature-Complexes'}).findAll('div', {'class': 'Catalog-Container-Item'})

for item in catalog:
    
    i += 1
    ws.write(i, 0, item.find('div', {'class': 'Catalog-Container-Item-TitleBlock-Title-Mini'}).b.contents[0])                        # Исследование
    ws.write(i, 1, item.span.span.contents[0][1:-1])                                                                                 # Код, отсечение квадратных скобок
    ws.write(i, 2, item.find('span', {'class': 'Catalog-Container-Item-PriceBlock-Price-No-Discount'}).b.contents[0])                # Цена

catalog = soup.find('div', {'class': 'Catalog-Content-Nomenclature-Singles'}).findAll('div', {'class': 'Catalog-Container-Item'})

for item in catalog:
    # Маленький контейнер внизу с коронавирусом(((((((((
    i += 1
    ws.write(i, 0, item.find('div', {'class': 'Catalog-Container-Item-TitleBlock-Title-Mini'}).b.contents[0])                        # Исследование
    ws.write(i, 1, item.span.span.contents[0][1:-1])                                                                                 # Код, отсечение квадратных скобок
    ws.write(i, 2, item.find('span', {'class': 'Catalog-Container-Item-PriceBlock-Price-No-Discount'}).b.contents[0])                # Цена

wb.save('helix.xls')                                                                                                                 # Сохранение таблицы