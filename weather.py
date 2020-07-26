import requests, xlwt
from bs4 import BeautifulSoup
from telegram.ext import Updater, MessageHandler, Filters;
telegram_token = '731520390:AAFPhAHpEiIQoJR7P_hSaXv9B4jIEPIDP9Y'

def parsing():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'}
    z = 0
    exist_link = 1
    array = []
    while exist_link != 0:
        exist_link = 0
        url = 'http://vk.com/@yvkurse?offset=' + str(z)
        news = requests.post(url, headers=headers)
        soup = BeautifulSoup(news.text, "lxml")
        pdata = soup.select("a", href='')
        pdata = pdata[4:]
        for i in range(len(pdata)):
            try:
                if (pdata[i]["href"] not in array) and (pdata[i]["href"].find('http') == -1):
                    array.append(pdata[i]["href"])
                    exist_link = 1
            except:
                exist_link = exist_link
        z += 19

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('1', cell_overwrite_ok=True)
    worksheet.write(0, 0, 'Заголовок')
    worksheet.write(0, 1, 'Текст')
    worksheet.write(0, 2, 'Ссылки на изображения')

    for i in range(len(array)):
        pics = ''
        text = ''
        url = 'http://vk.com/' + array[i]
        new = requests.get(url)
        soup = BeautifulSoup(new.text, "lxml")
        p = soup.select("p", class_='')
        h1 = soup.select("h1", class_='')
        image = soup.select("img", class_="article_carousel_img")
        for j in range(len(image)):
            try:
                if image[j]['src'].find('https://sun') != -1:
                    pics = pics + str(image[j]['src']) + '\n'

            except:
                i = i

        for j in range(len(pdata)):
            try:
                text = text + p[j].text.replace('\n', '')
            except:
                i = i
        # rows[i] =[[h1[0].text,text+'\n '], pics]
        worksheet.write(i + 1, 0, h1[0].text)
        worksheet.write(i + 1, 1, text + '\n')
        worksheet.write(i + 1, 2, pics)
    worksheet.col(0).width = 256 * 50
    worksheet.col(1).width = 256 * 100
    worksheet.col(2).width = 256 * 100
    workbook.save('events.xls')

def updateweather(array):
    url = 'https://yandex.ru/pogoda/month?lat=57.622949&lon=39.886458&via=f'
    weather = requests.get(url)
    soup = BeautifulSoup(weather.text, "lxml")
    info = ''
    pdata = soup.findAll('div', class_='climate-calendar-day__detailed-container-center')
    for i in range(len(pdata)):
        for j in range(len(pdata[i])):
            temp = pdata[i].contents[j].text + '\n'
            if j == 1:
                info += "Температура: "
            elif j == 3:
                info += "Давление: "
                temp = temp.replace('рт. ст.', 'рт. ст.\nВлажность: ')
                temp = temp.replace('%', '%\nВетер: ')
            elif j == 4:
                temp = temp.replace('Климатическая норма', 'Климатическая норма: ')

            info += temp
        array.append(info)
        info = ''

def search(array,day):
    for i in range(len(array)):
        if array[i].find(day) != -1:
            return array[i]
            break

def replay(bot, update):
    day = str(update.message.text)
    if day == '/events':
        update.message.reply_text('Формируется документ, подождите')
        parsing()
        doc = open('events.xls', 'rb')
        update.message.reply_document(doc)
    else:
        updateweather(array)
        search(array, day)
        update.message.reply_text(search(array, day))




answer = ''
array = []

updater = Updater(token=telegram_token)
updater.dispatcher.add_handler(MessageHandler(Filters.text, replay))


updater.start_polling()
updater.idle()



