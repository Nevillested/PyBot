from bs4 import BeautifulSoup
import transliterate
import googletrans
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
    #str = ''
    #for item in tup:
        #str = str + item
    str_val = "".join(map(str,tup))
    return str_val

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
    img_name = '/home/duck/Documents/GitHub/PyBot/assets/temp/shinobu.jpeg'
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

#переводит в транслит
def translit(ru_text):
    result_eng = transliterate.translit(ru_text, language_code='ru', reversed=True)
    return result_eng

#получает рандомную пикчу с реактора
def get_random_pikcha_by_teg(msg):
    try:
        tegs = msg.split()
        result_tegs = ''
        parse_mode = 'HTML'
        #собираем прилетевшие теги
        for item in tegs:
            result_tegs = result_tegs + '+' + str(item)
        #преобразовываем кириллицу в читабельный вид для http запроса в адресной строке
        result_tegs = urllib.parse.quote(result_tegs)
        #немножко заменяем и обрезаем ненужное
        result_tegs = result_tegs.replace("%2B", "+")
        result_tegs = result_tegs[1:]
        #создаем итоговый вариант для загрузки страницы, чтобы посчитать, сколько всего страниц на рекаторе есть по текущим тегам
        page = 'https://joyreactor.cc/search/' + result_tegs
        #открываем страницу
        html_page = urllib.request.urlopen(page)
        #скачиваем страницу
        soup = BeautifulSoup(html_page, "lxml")
        #переводим всю страницу в текстовый вариант длинного html-css-js кода и удаляем определенный кусок кода, тк его тег-дублируется, а мы по тегу ищем нужное.
        code_page_string = str(soup)
        #максимальный номер страницы по текущему тегу есть в div блоке pagination_expande, поэтому уберем все лишнее вокруг него
        #"стартовое слово", откуда начинается нужный блок
        start = f'<div class="pagination_expanded">'
        #"конечное слово", где заканчивается нужный блок
        end = f'</div>'
        #находим индекс стартового слова
        index_start = code_page_string.find(start)
        #обрезаем все, что было до нужного "стартового слова"
        remove_before = code_page_string[index_start+len(start):]
        #обрезаем все, что было до нужного "конечного слова"
        remove_after = remove_before.split(end, 1)[0]
        #чистим все, что находится в тегах (между знаками < и >) - оно нам не надо
        clean_page = re.sub('<.*?>', ';', remove_after)
        #помещаем весь список страниц в...список
        pages = list(clean_page.split(";"))
        #достаем искомое число страниц по текущему тегу
        max_page = pages[-2]
        #генерим номер рандомной странице в найденном диапазоне страниц
        result_page = 0
        if max_page.isnumeric:
            result_page = random.randint(1, int(max_page))
        else:
            result_page = 1
        #создаем итоговый вариант ссылки на реактор
        page = 'https://joyreactor.cc/search/' + result_tegs + "/" + str(result_page)
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
        url_of_result_image =  images_url[random.randint(0,len(images_url)-1)]
        #делаем запрос на пикчу
        response = requests.get(url_of_result_image)
        #даем пикче адрес и имя и сохраняем ее
        img_name = '/home/duck/Documents/GitHub/PyBot/assets/temp/image_by_teg.jpeg'
        if response.status_code:
            fp = open(img_name, 'wb')
            fp.write(response.content)
            fp.close()
        caption = '<a href="'+url_of_result_image+'">Ссылка на пикчу</a>\n<a href="'+page+'">Ссылка на страницу с постом пикчи</a>'
        #возвращаем адрес итоговой скачанной пикчи
        return parse_mode, caption, img_name
    except:
        img_name = '/home/duck/Documents/GitHub/PyBot/assets/not_found.png'
        parse_mode = None
        caption = "Мы либо ничего не нашли, либо произошла какая-то абсолютно неведомая херня, соре\nПопробуй написать теги транслитом"
        return parse_mode, caption, img_name

#создает qr-код
def create_qr_code(text):
    qrcode = segno.make_qr(text)
    new_dir = '/home/duck/Documents/GitHub/PyBot/assets/temp/'
    os.chdir(new_dir)
    name = "qr_code.pdf"
    qrcode.save(name, border=1, scale=8)
    result =  new_dir + name
    return result

#парсит html страницу с <тегами> и переводит в словарь
def html_string_to_dict(html_string):
    result_dict = {}
    idx_first_open_char_teg = -1
    idx_second_open_char_teg = -1
    current_key = ''
    current_value = ''
    for idx, char in enumerate(html_string):
        current_teg = ''

        if char == '<':
            idx_first_open_char_teg = idx
            if idx_second_open_char_teg != -1:
                current_value = html_string[idx_second_open_char_teg+1:idx_first_open_char_teg]
                idx_second_open_char_teg = -1
        if char == '>':
            idx_second_open_char_teg = idx

        if idx_first_open_char_teg != -1 and idx_second_open_char_teg != -1:

            current_teg = html_string[idx_first_open_char_teg+1:idx_second_open_char_teg]
            current_key = current_teg
            idx_first_open_char_teg = -1

        if len(current_key) != 0 and len(current_value) != 0:
            result_dict[current_key] = current_value
            current_key = ''
            current_value = ''

    return result_dict

#возвращает список с уникальными значениями
def unique_list_from_list(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
