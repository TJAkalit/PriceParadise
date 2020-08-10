import requests
import bs4
import xlwt

sess = requests.Session()

wb = xlwt.Workbook()
ws = wb.add_sheet('Page 1')
i = 0
ws.write(0, 0, 'Услуга')                                                                                              # Заголовки таблицы
ws.write(0, 1, 'Код')
ws.write(0, 2, 'Цена')

for page in range(1, 68):

    response = sess.get(f'https://www.cl-lab.info/analysis/list/all?page={page}').text                                # Запрос к разным страницам справочника через GET
    soup = bs4.BeautifulSoup(response, 'html.parser')
    trs = soup.findAll('tr')
    trs.pop(0)

    for tr in trs:

        i += 1
        ws.write(i, 0, tr.a.contents[0])                                                                              # Услуга
        ws.write(i, 1, tr.td.contents[0][1:-1])                                                                       # Код
        ws.write(i, 2, tr.findAll('div', {'class': 'text dynamic_content'})[1].contents[0].contents[0].split(' ')[0]) # Цена

wb.save('cl.xls')                                                                                                     # Сохранение таблицы в файл