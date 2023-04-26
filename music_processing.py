import os
from difflib import SequenceMatcher

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def getDictofFiles(dirName):
    #получение списка с путями всех файлов в текущей директории
    list_of_files = getListOfFiles(dirName)
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

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_data_of_song(name_of_song):
    result_out = None
    content_type_out = None
    #обновление словаря с файлами музыки
    dict_of_music = getDictofFiles('/home/duck/Documents/GitHub/PyBot/assets/music')
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