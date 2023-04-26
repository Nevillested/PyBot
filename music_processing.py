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

def get_path_of_song(name_of_song):
    path_of_song = None
    #обновление словаря с файлами музыки
    dict_of_music = getDictofFiles('/home/duck/Documents/GitHub/PyBot/assets/music')
    for key, value in dict_of_music.items():
        result_of_compare = similar(key, name_of_song) *100
        print(key, ' : ', result_of_compare)
        if result_of_compare > 70:
            path_of_song = value
            break
    return path_of_song