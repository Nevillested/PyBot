from bs4 import BeautifulSoup
import googletrans
import queries_to_bd
import requests
import random
import urllib
import segno
import os
import re

#проверяет в строке наличие не русских букв. Если нашел-возвращает -1, если все ок и не нашел - возвращает 0
def check_ru_char_in_string(string_income):

    string_income_lower = string_income.lower()
    ru_char_array = 'абвгдежзийклмнопрстуфхцчшщъыьэюя !?.,\n'
    result_out = ""

    for c in string_income_lower:
        for r in ru_char_array:
            if c == r:
                result_out = result_out + c
                
    if string_income_lower == result_out:
        return 0
    else:
        return -1

#проверяет в строке наличие не английских букв. Если нашел-возвращает -1, если все ок и не нашел - возвращает 0
def check_en_char_in_string(string_income):

    string_income_lower = string_income.lower()
    en_char_array = 'abcdefghijklmnopqrstuvwxyz !?.,\n'
    result_out = ""

    for c in string_income_lower:
        for r in en_char_array:
            if c == r:
                result_out = result_out + c

    if string_income_lower == result_out:
        return 0
    else:
        return -1

#переводит Tuple в стрингу
def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

#получает рандомную пикчу Шинобу с реактора
def get_pikcha():
    page = "https://joyreactor.cc/search/oshino+shinobu/"+str(random.randint(1,100))
    html_page = urllib.request.urlopen(page)
    soup = BeautifulSoup(html_page, "lxml")
    images_url = []
    
    for img in soup.findAll('img'):
        if img.get('src').__contains__('post'):
            images_url.append('https:'+img.get('src'))
    
    url_of_result_image =  images_url[random.randint(1,len(images_url)-1)]
    
    response = requests.get(url_of_result_image)
    img_name = 'assets/temp/shinobu.jpeg'
    if response.status_code:
        fp = open(img_name, 'wb')
        fp.write(response.content)
        fp.close()
    return img_name

#переводчик из EN в RU
def translate_en_to_ru(input_string):
    translator = googletrans.Translator()
    
    translated_text = translator.translate(input_string, dest='ru')
    
    return str(translated_text.text)

#получает рандомную пикчу с реактора по запросу
def get_random_pikcha_by_teg(msg):
    tegs = msg.split()
    result_tegs = ''

    #собираем прилетевшие теги
    for item in tegs:
        result_tegs = result_tegs + '+' + str(item)
    #преобразовываем кириллицу в читабельный вид для http pfghjcf в адресной строке
    result_tegs = urllib.parse.quote(result_tegs)
    #немножко заменяем и обрезаем ненужное
    result_tegs = result_tegs.replace("%2B", "+")
    result_tegs = result_tegs[1:]
    #создаем итоговый вариант для загрузки страницы, чтобы посчитать, сколько всего страниц на рекаторе есть по текущим тегам
    page = "https://joyreactor.cc/search?q=" + result_tegs
    #открываем страницу
    html_page = urllib.request.urlopen(page)
    #скачиваем страницу
    soup = BeautifulSoup(html_page, "lxml")
    #переводим всю страницу в текстовый вариант длинного html-css-js кода
    code_page_string = str(soup)
    #максимальный номер страницы по текущему тегу есть в div блоке pagination_expande, поэтому уберем все лишнее вокруг него
    #"стартовое слово", откуда начинается нужный блок
    start = 'pagination_expanded'
    #"конечное слово", где заканчивается нужный блок
    end = '</div'
    #находим индекс стартового слова
    index_start = code_page_string.find(start)
    #обрезаем все, что было до нужного "стартового слова"
    remove_before = code_page_string[index_start:]
    #обрезаем все, что было до нужного "конечного слова"
    remove_after = remove_before.split(end, 1)[0]
    #чистим все, что находится в тегах (между знаками < и >) - оно нам не надо
    t = re.sub('<.*?>', ';', remove_after)
    #переводим в список оставшееся содержимое
    li = list(t.split(";"))
    #номер страницы находится во втором жлементе списка с конца, итого:
    max_page = li[len(li)-2]

    result_page = 0
    if max_page.isnumeric:
        result_page = random.randint(1, int(max_page))
    else:
        result_page = 1

    #создаем итоговый вариант ссылки на реактор
    page = "https://joyreactor.cc/search?q=" + result_tegs + "/" +str(result_page)
    #открываем страницу
    html_page = urllib.request.urlopen(page)
    #скачиваем страницу
    soup = BeautifulSoup(html_page, "lxml")
    #создаем список элементов изображений (ссылок на пикчи)
    images_url = []

    #находим все пикчи, принадлежащие постам и помещаем все ссылки в images_url
    for img in soup.findAll('img'):
        if img.get('src').__contains__('post'):
            images_url.append('https:'+img.get('src'))
    
    #создаем итоговый URL нашей рандомной пикчи с текущей страницы
    url_of_result_image =  images_url[random.randint(1,len(images_url)-1)]
    #делаем запрос на страницу
    response = requests.get(url_of_result_image)
    #даем пикче адрес и имя и сохраняем ее
    img_name = 'assets/temp/image_by_teg.jpeg'
    if response.status_code:
        fp = open(img_name, 'wb')
        fp.write(response.content)
        fp.close()
    #возвращаем адрес итоговой скачанной пикчи
    return img_name

#создает qr-код
def create_qr_code(text):
    qrcode = segno.make_qr(text)
    new_dir = 'assets/temp'
    os.chdir(new_dir)
    name = "qr_code.pdf"
    qrcode.save(name, border=1, scale=8)
    result = os.getcwd() + '\\' + name
    return result