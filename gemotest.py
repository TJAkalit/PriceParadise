import requests
import bs4
import xlwt


r = requests.Session()
awn = r.get('https://www.gemotest.ru/novorossiysk/catalog/po-laboratornym-napravleniyam/samye-populyarnye-issledovaniya/?CITY_CODE=novorossiysk&EKG_HOME=0')
print(awn)

with open('index.html', 'rb') as ds:

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Лист 1')
    ws.write(0, 0, 'Услуга')
    ws.write(0, 1, 'Цена')

    awn = bs4.BeautifulSoup(ds.read().decode(), features = "html.parser")
    awn = awn.findAll("table", {"class": "d-col_xs_12 d-tal catalog-table"})
    i = 1
    for st in awn:
        ws.write(i, 0, st.find("a").contents[0].strip())
        ws.write(i, 1, st.find('div', {"class": "h3 d-mb_0"}).contents[0])
        # print(st.find("a").contents[0].strip())
        # print(st.find('div', {"class": "h3 d-mb_0"}).contents[0])
        i += 1

    wb.save('test.xls')

