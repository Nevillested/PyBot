import requests
import random
import urllib
from bs4 import BeautifulSoup

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
    img_name = 'get_pikcha.jpeg'
    if response.status_code:
        fp = open(img_name, 'wb')
        fp.write(response.content)
        fp.close()
    return img_name