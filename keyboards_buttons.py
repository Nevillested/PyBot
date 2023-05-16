from datetime import timedelta, date
import music_processing
import queries_to_bd
import telebot
import sending
import my_cfg
import os

#клавиатура основного меню
def main_menu(chat_id):
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    last_item = ''
    if chat_id == my_cfg.id_owner:
        last_item = "/adminka"
    else:
        last_item = "/send_to_admin"
    reply_to.add("/help", "/stick", "/pikcha", "/maid", "/anekdot", "/rand", "/encrypt", "/decrypt", "/speech_to_text", "/text_to_speech","/get_translate_jp",
    "/get_kanji", "/delete_space", "/get_quiz", "/get_weather", "/get_reactor_pikcha", "/get_qr_code", "/inline_mode", "/managesubscriptions", "/prices", "/music", last_item)
    return reply_to

#клавиатура для шифрования - выбор языка
def ru_en():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    reply_to.add("EN", "RU", "/main_menu")
    return reply_to

#клавиатура для шифрования - русские ключи
def ru_key():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True, one_time_keyboard=True)
    reply_to.add("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "/main_menu")
    return reply_to

#клавиатура для шифрования - английские ключи
def en_key():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True, one_time_keyboard=True)
    reply_to.add("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "/main_menu")
    return reply_to

#клавиатура для поиска номера десятка. Должна быть редактирована в зависимости от увеличения/уменьшения кол-ва кандзи в словаре
def kanji_num():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True, one_time_keyboard=True)
    reply_to.add("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "/main_menu")
    return reply_to

#клавиатура для выбора квиза
def kanji_quiz():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    reply_to.add("по всем имеющимся кандзи!","по номеру десятка!","/main_menu")
    return reply_to

#клавиатура для повторного вызова квиза
def retry_quiz():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    reply_to.add("Еще","/main_menu")
    return reply_to

#клавиатура админки
def admin_panel():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    reply_to.add("/get_users", "/send_to_user", "/main_menu")
    return reply_to

#клавиатура адреса погоды
def weather_place():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    current_place = telebot.types.KeyboardButton(text="Отправить свою локацию", request_location=True)
    reply_to.add(current_place, "/main_menu")
    return reply_to

#клавитура для выбора частоты получения подписки - в тесте
def subscription_frequency():
    reply_to = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    reply_to.add("Каждый час","Каждый день","Каждую неделю","Каждый месяц","Каждый год")
    return reply_to

#метод для создания инлайн-клавиатуры. На вход получает словарь из пары "ид кнопки-название кнопки", а на выходе отдает саму клавиатуру
def create_inline_kb(dict_of_buttons):
    reply_to = telebot.types.InlineKeyboardMarkup()
    for key, value in dict_of_buttons.items():
        reply_to.add(telebot.types.InlineKeyboardButton(text=value, callback_data=key))
    return reply_to

#клавитура для музыки - алфавитная клавиатура
def music_alphabet():
    abc_buttons = {}

    #создаем словарь с уникальными ключ-значение, где ключ - ID кнопки, а значение - текст кнопки
    for item in music_processing.list_data_of_music_files:
        if (item[0]).upper() not in abc_buttons:
            abc_buttons['_music_abc_group_' + (item[4]).upper()] = item[0]
    sorted_abc_buttons = dict(sorted(abc_buttons.items(), key=lambda item: item[1]))

    reply_to = telebot.types.InlineKeyboardMarkup(row_width=5)
    local_cnt = 1
    global_cnt = 0
    len_of_dict = len(sorted_abc_buttons)

    for key, value in sorted_abc_buttons.items():

        if local_cnt == 1:
            tmp_btn_1 = telebot.types.InlineKeyboardButton(text=value, callback_data=key)

        elif local_cnt == 2:
            tmp_btn_2 = telebot.types.InlineKeyboardButton(text=value, callback_data=key)

        elif local_cnt == 3:
            tmp_btn_3 = telebot.types.InlineKeyboardButton(text=value, callback_data=key)

        elif local_cnt == 4:
            tmp_btn_4 = telebot.types.InlineKeyboardButton(text=value, callback_data=key)

        elif local_cnt == 5:
            tmp_btn_5 = telebot.types.InlineKeyboardButton(text=value, callback_data=key)
            reply_to.add(tmp_btn_1, tmp_btn_2, tmp_btn_3, tmp_btn_4, tmp_btn_5)
            tmp_btn_1 = None
            tmp_btn_2 = None
            tmp_btn_3 = None
            tmp_btn_4 = None
            tmp_btn_5 = None
            local_cnt = 0


        global_cnt = global_cnt + 1

        if str(global_cnt) == str(len_of_dict):
            if local_cnt == 1:
                reply_to.add(tmp_btn_1)
            elif local_cnt == 2:
                reply_to.add(tmp_btn_1, tmp_btn_2)
            elif local_cnt == 3:
                reply_to.add(tmp_btn_1, tmp_btn_2, tmp_btn_3)
            elif local_cnt == 4:
                reply_to.add(tmp_btn_1, tmp_btn_2, tmp_btn_3, tmp_btn_4)
            elif local_cnt == 5:
                reply_to.add(tmp_btn_1, tmp_btn_2, tmp_btn_3, tmp_btn_4, tmp_btn_5)
        local_cnt = local_cnt + 1
    return reply_to

#клавитура для музыки - список исполнителей сгруппированных по общему первому знаку
def music_group_list(call_data):
    first_char = call_data.replace('_music_abc_group_','')

    #создаем словарь с уникальными ключ-значение, где ключ - ID кнопки, а значение - текст кнопки
    dict_of_names_group = {}
    for item in music_processing.list_data_of_music_files:
        if ((item[4])).upper() == first_char.upper() and (item[4]) not in dict_of_names_group:
            dict_of_names_group['_music_group_' + (item[5])] = item[1]
    sorted_dict_of_names_group = dict(sorted(dict_of_names_group.items(), key=lambda item: item[1]))

    reply_to = telebot.types.InlineKeyboardMarkup(row_width=2)
    local_cnt = 1
    global_cnt = 0
    len_of_dict = len(sorted_dict_of_names_group)

    for key, value in sorted_dict_of_names_group.items():
        if local_cnt == 1:
            tmp_btn_1 = telebot.types.InlineKeyboardButton(text=value, callback_data=key)
        elif local_cnt == 2:
            tmp_btn_2 = telebot.types.InlineKeyboardButton(text=value, callback_data=key)
            reply_to.add(tmp_btn_1, tmp_btn_2)
            tmp_btn_1 = None
            tmp_btn_2 = None
            local_cnt = 0

        global_cnt = global_cnt + 1

        if str(global_cnt) == str(len_of_dict):
            if local_cnt == 1:
                reply_to.add(tmp_btn_1)
        local_cnt = local_cnt + 1
    reply_to.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='_music_menu_one_'))
    return reply_to

#клавитура для музыки - список альбомов определенного исполнителя
def albums_of_group_list(call_data):
    group_name = call_data.replace('_music_group_','')

    albums_name_buttons = {}
    musical_group_path = music_processing.music_path + r'/' + group_name
    folders = os.listdir(musical_group_path)
    for album_name in folders:
        albums_name_buttons['_music_album_' + group_name + r'/' + album_name] = album_name
    sorted_abc_buttons = dict(sorted(albums_name_buttons.items(), key=lambda item: item[1]))

    reply_to = create_inline_kb(sorted_abc_buttons)
    return reply_to

#клавитура для музыки - список песен определенного альбома и исполнителя
def songs_of_album_list(call_data):
    group_album_name = call_data.replace('_music_album_','')
    songs_name_buttons = {}
    songs_path = music_processing.music_path + r'/' + group_album_name

    folder = os.listdir(songs_path)

    for song_name in folder:
        idx_of_LAST_TOCHKA = song_name.rindex('.')
        cur_song_name = song_name[0:idx_of_LAST_TOCHKA]
        for char in cur_song_name:
            for num in '1234567890 ':
                if cur_song_name.__contains__(num):
                    cur_song_name = cur_song_name.replace(num,'')
        songs_name_buttons['_music_song_' + group_album_name + r'/' + cur_song_name ] = song_name

    sorted_abc_buttons = dict(sorted(songs_name_buttons.items(), key=lambda item: item[1]))

    reply_to = create_inline_kb(sorted_abc_buttons)
    return reply_to