import datetime
import calendar
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

#метод для создания инлайн-клавиатуры. На вход получает словарь из пары "ид кнопки-название кнопки" и количество кнопок в строке, а на выходе отдает саму клавиатуру
def create_inline_kb(dict_of_buttons, cnt_object_in_row):
    reply_to = telebot.types.InlineKeyboardMarkup()
    row = []
    for i in dict_of_buttons:
        current_button = telebot.types.InlineKeyboardButton(text = dict_of_buttons[i], callback_data = i)
        row.append(current_button)
        if len(row) == cnt_object_in_row:
            reply_to.add(*row)
            row = []
    reply_to.add(*row)
    return reply_to

def get_kb_payments():
    cnt_object_in_row = 1
    reply_to = telebot.types.InlineKeyboardMarkup()
    keyboard_dict = {"id_2_payment_one_btn": "Потому что я такой хорошенький - 100р","id_2_payment_two_btn":"На тяжелую жизнь бездомного разработчика - 150р","id_2_payment_three_btn":"На развитие бота, чтобы он делал вашу жизнь лучше - 200р", "id_2_payment_shinobu":"На фигурки с лучшей девочкой ~~~р"}
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавитура для музыки - алфавитная клавиатура
def music_alphabet():
    abc_buttons = queries_to_bd.get_abc_dict()
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

#клавитура для музыки - список исполнителей
def music_group_list(call_data):
    dict_of_names_group = queries_to_bd.get_performer_dict(call_data)
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
    reply_to.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='id_3_mus_back_one_' + call_data))
    return reply_to

#клавитура для музыки - список альбомов
def albums_of_group_list(call_data):
    dict_of_names_albums = queries_to_bd.get_albums_dict(call_data)
    sorted_dict_of_names_albums = dict(sorted(dict_of_names_albums.items(), key=lambda item: item[1]))
    reply_to = telebot.types.InlineKeyboardMarkup(row_width=2)
    local_cnt = 1
    global_cnt = 0
    len_of_dict = len(sorted_dict_of_names_albums)
    for key, value in sorted_dict_of_names_albums.items():
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
    reply_to.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='id_3_mus_back_two_' + call_data))
    return reply_to

#клавитура для музыки - список песен
def songs_of_album_list(call_data):
    dict_of_names_songs = queries_to_bd.get_songs_dict(call_data)
    sorted_dict_of_names_songs = dict(sorted(dict_of_names_songs.items(), key=lambda item: item[1]))
    reply_to = telebot.types.InlineKeyboardMarkup(row_width=2)
    local_cnt = 1
    global_cnt = 0
    len_of_dict = len(sorted_dict_of_names_songs)
    for key, value in sorted_dict_of_names_songs.items():
        current_key = key
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
    reply_to.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='id_3_mus_back_three_' + call_data))
    return reply_to

#основная клавиатура напоминалок
def notif_common():
    cnt_object_in_row = 1
    keyboard_dict = {"id_4_notification_cur" : "Текущие напоминалки", "id_4_notification_new" : "Новая напоминалка", "id_4_notification_cancel" : "Отмена"}
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to































#клавитура для выбора года напоминания
def notif_year():
    cnt_object_in_row = 3
    current_year = datetime.datetime.now().year
    keyboard_dict = {}
    for i in range(10):
        dict_key = 'id_4_not_year_' + str(current_year + i)
        dict_value = str(current_year + i)
        keyboard_dict[dict_key] = dict_value
    keyboard_dict["id_4_not_back_2"] = "Назад"
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавитура для выбора месяца напоминания
def notif_month(need_year):
    cnt_object_in_row = 3
    current_year = str(datetime.datetime.now().year)
    current_month = datetime.datetime.now().month
    keyboard_dict = {}
    month_dict = {1 : "Январь", 2 : "Февраль", 3 : "Март", 4 : "Апрель", 5 : "Май", 6 : "Июнь", 7 : "Июль", 8 : "Август", 9 : "Сентярь", 10 : "Октябрь", 11 : "Ноябрь", 12 : "Декабрь",}
    month_start = 1
    if current_year == need_year:
        month_start = current_month
    for i in range(month_start, 13):
        dict_key = 'not_month_' + str(i)
        dict_value = month_dict[i]
        keyboard_dict[dict_key] = dict_value
    keyboard_dict["not_back_3"] = "Назад"
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавитура для выбора дня напоминания
def notif_day(need_month, chat_id):
    cnt_object_in_row = 3
    keyboard_dict = {}
    need_year = queries_to_bd.get_year_of_edit_not(chat_id)
    day_start = 1

    if need_year == str(datetime.datetime.now().year) and need_month == str(datetime.datetime.now().month):
        day_start = str(datetime.datetime.now().day)
    day_end = calendar.monthrange(int(need_year), int(need_month))[1]
    for i in range(int(day_start), int(day_end) + 1):
        dict_key = 'not_day_' + str(i)
        dict_value = str(i)
        keyboard_dict[dict_key] = dict_value
    keyboard_dict["not_back_4"] = "Назад"
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавиатура для выбора часа напоминания
def notif_hour(need_day, chat_id):
    cnt_object_in_row = 3
    keyboard_dict = {}
    need_year = queries_to_bd.get_year_of_edit_not(chat_id)
    need_month = queries_to_bd.get_month_of_edit_not(chat_id)
    hour_start = 0
    if need_year == str(datetime.datetime.now().year) and need_month == str(datetime.datetime.now().month) and need_day == str(datetime.datetime.now().day):
        hour_start = str(datetime.datetime.now().hour)
    hour_end = 24
    for i in range(int(hour_start),int(hour_end)):
        dict_key = 'not_hour_' + str(i)
        dict_value = str(i)
        keyboard_dict[dict_key] = dict_value
    keyboard_dict["not_back_5"] = "Назад"
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавиатура для выбора часа напоминания
def notif_minute(need_hour, chat_id):
    cnt_object_in_row = 3
    keyboard_dict = {}
    need_year = queries_to_bd.get_year_of_edit_not(chat_id)
    need_month = queries_to_bd.get_month_of_edit_not(chat_id)
    need_day = queries_to_bd.get_day_of_edit_not(chat_id)
    minute_start = 0
    if need_year == str(datetime.datetime.now().year) and need_month == str(datetime.datetime.now().month) and need_day == str(datetime.datetime.now().day) and need_hour == str(datetime.datetime.now().hour):
        minute_start = str(datetime.datetime.now().minute)
    minute_end = 60
    for i in range(int(minute_start),int(minute_end)):
        if i < 10:
            dict_key = 'not_minute_0' + str(i)
            dict_value = '0' + str(i)
        else:
            dict_key = 'not_minute_' + str(i)
            dict_value = str(i)
        keyboard_dict[dict_key] = dict_value
    keyboard_dict["not_back_6"] = "Назад"
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавиатура для выбора повторения напоминалки
def notif_repeat():
    cnt_object_in_row = 2
    keyboard_dict = {"not_repeat_minute" : "Каждую минуту", "not_repeat_hour" : "Каждый час", "not_repeat_day" : "Каждый день", "not_repeat_week" : "Каждую неделю", "not_repeat_month" : "Каждый месяц", "not_repeat_year" : "Каждый год", "not_repeat_none" : "Не повторять", "not_back_7" : "Назад"}
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавиатура с имеющимися у пользователя напоминалками
def get_kb_user_notifications(chat_id):
    cnt_object_in_row = 1
    keyboard_dict = {}
    user_data_notif = queries_to_bd.get_user_notifications(chat_id)
    for current_row in user_data_notif:
        dict_key = "id_4_notif_id_" + str(current_row[0])
        dict_value = current_row[1]
        keyboard_dict[dict_key] = dict_value
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to

#клавиатура для изменения текущей напоминалки
def get_kb_change_notification(not_id):
    cnt_object_in_row = 2
    keyboard_dict = {"id_4_edit_name_" + str(not_id) : "Изменить название",
                     "id_4_edit_act_" + str(not_id) : "Изменить активность",
                     "id_4_edit_repeat_flg_" + str(not_id) : "Изменить повторность",
                     "id_4_edit_repeat_intv_" + str(not_id) : "Изменить интервал повторения",
                     "id_4_edit_year_" + str(not_id) : "Изменить год",
                     "id_4_edit_month_" + str(not_id) : "Изменить месяц",
                     "id_4_edit_day_" + str(not_id) : "Изменить день",
                     "id_4_edit_hour_" + str(not_id) : "Изменить час",
                     "id_4_edit_min_" + str(not_id) : "Изменить минуты",
                     "id_4_notification_cur" : "Назад"
                    }
    reply_to = create_inline_kb(keyboard_dict, cnt_object_in_row)
    return reply_to







