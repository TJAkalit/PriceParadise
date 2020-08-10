import requests
import bs4
import xlwt

i = 0
wb = xlwt.Workbook()
ws = wb.add_sheet('Лист 1')
ws.write(i, 0, 'Исследование')
ws.write(i, 1, 'Код')
ws.write(i, 2, 'Цена')

SESSION = requests.Session()
response = SESSION.get('https://www.gemotest.ru/novorossiysk/catalog/po-laboratornym-napravleniyam/samye-populyarnye-issledovaniya/')
PAGE = bs4.BeautifulSoup(response.text, features = 'html.parser')

catalog = PAGE.findAll('table', {'class': 'd-col_xs_12 d-tal catalog-table'})

for item in catalog:

    i += 1
    ws.write(i, 0, item.tbody.tr.td.a.contents[0].strip())                        # Исследование
    ws.write(i, 1, item.tbody.tr.contents[3].contents[0])                         # Код
    ws.write(i, 2, item.tbody.tr.contents[7].div.div.div.contents[0].strip())     # Цена        

LOAD = PAGE.find('div', {'class': 'gt-catalog__load-more'}).a['data-id']          # Поиск data-id для AJAX запроса

while True:

    response = SESSION.get(f'https://www.gemotest.ru/novorossiysk/catalog/po-laboratornym-napravleniyam/samye-populyarnye-issledovaniya/?CITY_CODE=novorossiysk&EKG_HOME=0&ajax_cat=y&cat={LOAD}')
    PAGE = bs4.BeautifulSoup(response.text, features= 'html.parser')
    catalog = PAGE.findAll('table')

    for item in catalog:

        i += 1
        ws.write(i, 0, item.tbody.tr.td.a.contents[0].strip())                     # Исследование
        ws.write(i, 1, item.tbody.tr.contents[3].contents[0])                      # Код
        ws.write(i, 2, item.tbody.tr.contents[7].div.div.div.contents[0].strip())  # Цена  

    try:
        
        LOAD = PAGE.find('div', {'class': 'gt-catalog__load-more'}).a['data-id']   # Поиск data-id для AJAX запроса
    
    except:

        break

wb.save('gemotest.xls')