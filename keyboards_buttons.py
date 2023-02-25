from datetime import timedelta, date
import telebot
import sending

#клавиатура основного меню
def main_menu(chat_id):
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        help = telebot.types.KeyboardButton(text="/help")
        stick = telebot.types.KeyboardButton(text="/stick")
        pikcha = telebot.types.KeyboardButton(text="/pikcha")
        maid = telebot.types.KeyboardButton(text="/maid")
        anekdot = telebot.types.KeyboardButton(text="/anekdot")
        rand = telebot.types.KeyboardButton(text="/rand")
        encrypt = telebot.types.KeyboardButton(text="/encrypt")
        decrypt = telebot.types.KeyboardButton(text="/decrypt")
        speech_to_text = telebot.types.KeyboardButton(text="/speech_to_text")
        text_to_speech = telebot.types.KeyboardButton(text="/text_to_speech")
        get_translate_jp = telebot.types.KeyboardButton(text="/get_translate_jp")
        get_kanji = telebot.types.KeyboardButton(text="/get_kanji")
        delete_space = telebot.types.KeyboardButton(text="/delete_space")
        get_quiz = telebot.types.KeyboardButton(text="/get_quiz")
        send_admin = telebot.types.KeyboardButton(text="/send_to_admin")
        get_weather = telebot.types.KeyboardButton(text="/get_weather")
        get_reactor_pikcha = telebot.types.KeyboardButton(text="/get_reactor_pikcha")
        get_qr_code = telebot.types.KeyboardButton(text="/get_qr_code")

        adminka = telebot.types.KeyboardButton(text="/adminka")
        
        if chat_id == sending.id_owner:
            reply_to.add(help, stick, pikcha, maid, anekdot, rand, encrypt, decrypt, speech_to_text, text_to_speech, get_translate_jp, get_kanji, delete_space, get_quiz, get_weather, get_reactor_pikcha, get_qr_code, adminka)
        else:
            reply_to.add(help, stick, pikcha, maid, anekdot, rand, encrypt, decrypt, speech_to_text, text_to_speech, get_translate_jp, get_kanji, delete_space, get_quiz, get_weather, get_reactor_pikcha, get_qr_code, send_admin)

        return reply_to

#клавиатура для шифрования - выбор языка
def ru_en():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        EN = telebot.types.KeyboardButton(text="EN")
        RU = telebot.types.KeyboardButton(text="RU")
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(EN, RU, main_menu)
        return reply_to

#клавиатура для шифрования - русские ключи
def ru_key():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True, one_time_keyboard=True)
        zero = telebot.types.KeyboardButton(text="0")
        one = telebot.types.KeyboardButton(text="1")
        two = telebot.types.KeyboardButton(text="2")
        three = telebot.types.KeyboardButton(text="3")
        four = telebot.types.KeyboardButton(text="4")
        five = telebot.types.KeyboardButton(text="5")
        six = telebot.types.KeyboardButton(text="6")
        seven = telebot.types.KeyboardButton(text="7")
        eight = telebot.types.KeyboardButton(text="8")
        nine = telebot.types.KeyboardButton(text="9")
        ten = telebot.types.KeyboardButton(text="10")
        eleven = telebot.types.KeyboardButton(text="11")
        twelve = telebot.types.KeyboardButton(text="12")
        thirteen = telebot.types.KeyboardButton(text="13")
        fourteen = telebot.types.KeyboardButton(text="14")
        fifteen = telebot.types.KeyboardButton(text="15")
        sixteen = telebot.types.KeyboardButton(text="16")
        seventeen = telebot.types.KeyboardButton(text="17")
        eighteen = telebot.types.KeyboardButton(text="18")
        nineteen = telebot.types.KeyboardButton(text="19")
        twenty = telebot.types.KeyboardButton(text="20")
        twenty_one = telebot.types.KeyboardButton(text="21")
        twenty_two = telebot.types.KeyboardButton(text="22")
        twenty_three = telebot.types.KeyboardButton(text="23")
        twenty_four = telebot.types.KeyboardButton(text="24")
        twenty_five = telebot.types.KeyboardButton(text="25")
        twenty_six = telebot.types.KeyboardButton(text="26")
        twenty_seven = telebot.types.KeyboardButton(text="27")
        twenty_eight = telebot.types.KeyboardButton(text="28")
        twenty_nine = telebot.types.KeyboardButton(text="29")
        thirty = telebot.types.KeyboardButton(text="30")
        thirty_one = telebot.types.KeyboardButton(text="31")
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty, twenty_one, twenty_two, twenty_three, twenty_four, twenty_five, twenty_six, twenty_seven, twenty_eight, twenty_nine, thirty, thirty_one, main_menu)
        return reply_to

#клавиатура для шифрования - английские ключи
def en_key():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True, one_time_keyboard=True)
        zero = telebot.types.KeyboardButton(text="0")
        one = telebot.types.KeyboardButton(text="1")
        two = telebot.types.KeyboardButton(text="2")
        three = telebot.types.KeyboardButton(text="3")
        four = telebot.types.KeyboardButton(text="4")
        five = telebot.types.KeyboardButton(text="5")
        six = telebot.types.KeyboardButton(text="6")
        seven = telebot.types.KeyboardButton(text="7")
        eight = telebot.types.KeyboardButton(text="8")
        nine = telebot.types.KeyboardButton(text="9")
        ten = telebot.types.KeyboardButton(text="10")
        eleven = telebot.types.KeyboardButton(text="11")
        twelve = telebot.types.KeyboardButton(text="12")
        thirteen = telebot.types.KeyboardButton(text="13")
        fourteen = telebot.types.KeyboardButton(text="14")
        fifteen = telebot.types.KeyboardButton(text="15")
        sixteen = telebot.types.KeyboardButton(text="16")
        seventeen = telebot.types.KeyboardButton(text="17")
        eighteen = telebot.types.KeyboardButton(text="18")
        nineteen = telebot.types.KeyboardButton(text="19")
        twenty = telebot.types.KeyboardButton(text="20")
        twenty_one = telebot.types.KeyboardButton(text="21")
        twenty_two = telebot.types.KeyboardButton(text="22")
        twenty_three = telebot.types.KeyboardButton(text="23")
        twenty_four = telebot.types.KeyboardButton(text="24")
        twenty_five = telebot.types.KeyboardButton(text="25")
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty, twenty_one, twenty_two, twenty_three, twenty_four, twenty_five, main_menu)
        return reply_to

#клавиатура для поиска номера десятка. Должна быть редактирована в зависимости от увеличения/уменьшения кол-ва кандзи в словаре
def kanji_num():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True, one_time_keyboard=True)
        one = telebot.types.KeyboardButton(text="1")
        two = telebot.types.KeyboardButton(text="2")
        three = telebot.types.KeyboardButton(text="3")
        four = telebot.types.KeyboardButton(text="4")
        five = telebot.types.KeyboardButton(text="5")
        six = telebot.types.KeyboardButton(text="6")
        seven = telebot.types.KeyboardButton(text="7")
        eight = telebot.types.KeyboardButton(text="8")
        nine = telebot.types.KeyboardButton(text="9")
        ten = telebot.types.KeyboardButton(text="10")
        eleven = telebot.types.KeyboardButton(text="11")
        twelve = telebot.types.KeyboardButton(text="12")
        thirteen = telebot.types.KeyboardButton(text="13")
        fourteen = telebot.types.KeyboardButton(text="14")
        fifteen = telebot.types.KeyboardButton(text="15")
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, main_menu)
        return reply_to

#клавиатура для выбора квиза
def kanji_quiz():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        all_kanji = telebot.types.KeyboardButton(text="по всем имеющимся кандзи!")
        decade_kanji = telebot.types.KeyboardButton(text="по номеру десятка!")
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(all_kanji, decade_kanji, main_menu)
        return reply_to

#клавиатура для повторного вызова квиза
def retry_quiz():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        yes = telebot.types.KeyboardButton(text="Еще")
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(yes, main_menu)
        return reply_to

#клавиатура админки
def admin_panel():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        get_users = telebot.types.KeyboardButton(text="/get_users")
        send_to_user = telebot.types.KeyboardButton(text="/send_to_user")
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(get_users, send_to_user, main_menu)
        return reply_to

#клавиатура адреса погоды
def weather_place():
        reply_to = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        current_place = telebot.types.KeyboardButton(text="Отправить свою локацию", request_location=True)
        main_menu = telebot.types.KeyboardButton(text="/main_menu")
        reply_to.add(current_place, main_menu)
        return reply_to

#клавиатура по циклу - тестовый вариант, нигде пока не используется
def weather_days():
        reply_to = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        iteration_var = 0
        while iteration_var <= 31:
            buffer_day = date.today() + timedelta(days=iteration_var)
            buffer_day = buffer_day.strftime('%d-%m-%Y')
            reply_to.add(telebot.types.KeyboardButton(text=str(buffer_day)))
            iteration_var += 1
        return reply_to

#тестовая inline клавиатура - команда /get_inline
def inline_keyboard():
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(telebot.types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
                                   telebot.types.InlineKeyboardButton("No", callback_data="cb_no"))
        return markup