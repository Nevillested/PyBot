import os
import keyboards_buttons
import sending
from difflib import SequenceMatcher
import my_cfg


music_path = '/home/duck/Documents/GitHub/PyBot/assets/music'
allFiles = list()

#получение списка с путями всех файлов в текущей директории
def getListOfPathFiles(current_path):
    listOfFile = os.listdir(current_path)
    for entry in listOfFile:
        fullPath = os.path.join(current_path, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfPathFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

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

#подготовка данных по музыке
def prepare_data(bot):
    None