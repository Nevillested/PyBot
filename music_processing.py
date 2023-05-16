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
"""
#получение словаря, в котором ключ = имя файла, значение = путь к нему
def getDictofFiles():
    list_of_files = getListOfPathFiles(music_path)
    dict = {}

    for item in list_of_files:
        idx_from = ''
        idx_to = len(item)
        for idx, char in enumerate(item):
            if char == "/":
                idx_from = idx
        cur_file_name = ((item[idx_from+1:idx_to]).lower()).replace("'","")
        dict[cur_file_name] = item

    return dict

#сравнение двух строк
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#получение данных по имени файла
def get_data_of_song(name_of_song):
    result_out = None
    content_type_out = None
    dict_of_music = getDictofFiles()
    for key, value in dict_of_music.items():
        result_of_compare = similar(name_of_song, key) * 100
        if result_of_compare > 70:
            result_out = value
            content_type_out = "audio"
            break

    if result_out is not None:
        file_stats = os.stat(result_out)
        if file_stats.st_size / (1024 * 1024) > 50:
            result_out = "Соре, этот файл весит больше 50 мб, телега не позволяет отправлять такие файлы"
            content_type_out = "text"
    else:
        result_out = "Мы ничего не нашли, соре"
        content_type_out = "text"

    return result_out, content_type_out

def getListOfMusicFiles():
    list_of_files = getListOfPathFiles(music_path)
    files_names = list()

    for item in list_of_files:
        idx_from = ''
        idx_to = len(item)
        for idx, char in enumerate(item):
            if char == "/":
                idx_from = idx
        cur_file_name = ((item[idx_from+1:idx_to]).lower()).replace("'","")
        files_names.append(cur_file_name)

    return files_names






#создает отсортированный словарь с названиями групп, которые начинаются с буквы, которую выбрал пользователь
def getDictOfSortedAbcMusicButtons(first_char):

    dict_of_names_group = {}
    folders = os.listdir(music_path)
    for music_group in folders:
        if (music_group[0]).upper() == first_char.upper():
            clean_music_group = replace_invalid_telegram_chr(music_group)
            dict_of_names_group['_music_group_' + clean_music_group] = music_group
    sort_dict_of_names_group = dict(sorted(dict_of_names_group.items(), key=lambda item: item[1]))
    for item in dict_of_names_group:
        print(item)
    return sort_dict_of_names_group
"""

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

        item_zero = (unique_item[0]).upper()
        item_one = unique_item[0:find_nth(unique_item,r'/',1)]
        item_two = unique_item[find_nth(unique_item,r'/',1)+1:find_nth(unique_item,r'/',2)]
        item_three = unique_item[find_nth(unique_item,r'/',2)+1:unique_item.rindex('.')]

        item_four = replace_invalid_telegram_chr(item_zero)
        item_five = replace_invalid_telegram_chr(item_one)
        item_six = replace_invalid_telegram_chr(item_two)
        item_seven = replace_invalid_telegram_chr(item_three)

        list_data_of_music_files.append([item_zero, item_one, item_two, item_three, item_four, item_five, item_six, item_seven])