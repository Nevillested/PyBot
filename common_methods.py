from googletrans import Translator
from bs4 import BeautifulSoup
import queries_to_bd
import queries_to_bd
import requests
import random
import urllib

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

#метод пересылки сообщений
id_owner = 1275894304
def resend_data(message, bot):

    chat_id_to_send = None

    if message.chat.id == id_owner:
        chat_id_to_send = queries_to_bd.queries_class.get_prelast_user_msg(message.chat.id)
    else:
        chat_id_to_send = id_owner
        
    bot.send_message(chat_id_to_send, 'Пришло сообщение от @' + message.from_user.username +':') 

    if message.content_type == "text":
        bot.send_message(chat_id_to_send, message.text)
    elif message.content_type == "sticker":
        bot.send_sticker(chat_id_to_send, message.sticker.file_id)
    elif message.content_type == "photo":
        file = message.photo[-1]
        file = file.file_id
        bot.send_photo(chat_id_to_send, photo = file)
    elif message.content_type == "voice":
        bot.send_voice(chat_id_to_send, message.voice.file_id)
    elif message.content_type == "video":
        bot.send_video(chat_id_to_send, message.video.file_id)
    elif message.content_type == "video_note":
        bot.send_video_note(chat_id_to_send, message.video_note.file_id)
    elif message.content_type == "document":
        bot.send_document(chat_id_to_send, message.document.file_id)
    else:
        bot.send_message(chat_id_to_send, 'Не удалось переслать вам сообщение. Свяжитесь с админом и расскажите об ошибке плз\nТип сообщения: '+str(message.content_type)) 

#переводчик из EN в RU
def translate_en_to_ru(input_string):
    translator = Translator()
    
    translated_text = translator.translate(input_string, dest='ru')
    
    return str(translated_text.text)