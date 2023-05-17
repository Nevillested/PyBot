import os
import keyboards_buttons
import sending
from difflib import SequenceMatcher
import my_cfg

music_path = '/home/duck/Documents/GitHub/PyBot/assets/music'
list_data_of_music_files = list()

#получение списка с путями всех файлов в текущей директории
def getListOfPathFiles(current_path):
    allFiles = list()
    listOfFile = os.listdir(current_path)
    for entry in listOfFile:
        fullPath = os.path.join(current_path, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfPathFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

#убирает все знаки, которые не подходят для создания call_back_data button
def replace_invalid_telegram_chr(current_string):
    new_string = ''
    number_dict = {"1":"one","2":"two","3":"three","4":"four","5":"five","6":"six","7":"seven","8":"eight","9":"nine","0":"zero",}
    for char_cs in current_string:
        for char_rp in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_1234567890':
            if char_cs == char_rp:
                if char_cs in number_dict:
                    new_string += number_dict.get(char_cs)
                else:
                    new_string += char_cs
    return new_string

#выдает индекс н-ного вхождение подстроки в строке
def find_nth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)

#подготовка данных по музыке
def prepare_data():
    #создаем список с путями всех файлов в текущей директориим
    list_of_full_path_all_files = getListOfPathFiles(music_path)

    #а теперь наполняем новый список (list_data_of_music_files) кортежами, каждый из которых состоит из 8 элементов, где:
    #item_zero   0 элемент списка - буква, с которой начинается название группы
    #item_one    1 элемент списка - название группы
    #item_two    2 элемент списка - название альбома
    #item_three  3 элемент списка - название песни

    #item_four   4 элемент списка - очищенная буква, с которой начинается название группы - необходимо для корректного call back data id
    #item_five   5 элемент списка - очищенное название группы  - необходимо для корректного call back data id
    #item_six    6 элемент списка - очищенное название альбома - необходимо для корректного call back data id
    #item_seven  7 элемент списка - очищенное название песни - необходимо для корректного call back data id
    for path_of_file in list_of_full_path_all_files:
        unique_item = path_of_file.replace(r'/home/duck/Documents/GitHub/PyBot/assets/music/','')

        item_zero  = (unique_item[0]).upper()
        item_one   = unique_item[0:find_nth(unique_item,r'/',1)]
        item_two   = unique_item[find_nth(unique_item,r'/',1)+1:find_nth(unique_item,r'/',2)]
        item_three = unique_item[find_nth(unique_item,r'/',2)+1:unique_item.rindex('.')]

        item_four  = (replace_invalid_telegram_chr(item_zero)).upper()
        item_five  = (item_four + r'/' + replace_invalid_telegram_chr(item_one)).upper()
        item_six   = (item_five + r'/' + replace_invalid_telegram_chr(item_two)).upper()
        item_seven = ((item_six + r'/' + replace_invalid_telegram_chr(item_three)).upper())

        while True:
            if len(item_seven.encode('utf-8'))+12 > 64:
                item_seven = item_seven[0:len(item_seven)-1]
            else:
                break
        list_data_of_music_files.append([item_zero, item_one, item_two, item_three, item_four, item_five, item_six, item_seven])