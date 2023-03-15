import keyboards_buttons
import common_methods
import queries_to_bd
from datetime import datetime
import speech_to_text
import text_to_speech
import sending
import weather
import ChatGpt
import telebot
import random
import cezar
import quiz
import cfg
import os


def cases_trigger(cur_message, bot):
    
    correct_answer_id_out = ""
    content_type_out = ""
    answer_desc_out = ""
    parse_mode_out = None
    poll_type_out = ""
    resending_flg = 0
    caption_out = ""
    result_out = ""
    reply_out = telebot.types.ReplyKeyboardMarkup()
    
    #получает последнее свое отправленное сообщение
    last_msg_bot = queries_to_bd.get_last_bot_msg(cur_message.chat.id)
    last_msg_user = ""

    if cur_message.content_type == "text":
            last_msg_user = cur_message.text.lower()
    elif cur_message.content_type == "voice":
            last_msg_user = (speech_to_text.voice_processing(cur_message, bot, "ru" )).lower()

    if last_msg_user == "/start" or  last_msg_user == "/help":
            content_type_out = "text"
            admin = "/send_to_admin - отправка сообщения админу\n"
            s0 =  "Помощь немощу, сам же догадаться не можешь интуитивно да:\n"
            s1 =  "/stick - рандомный стикер с Шинобу\n"
            s2 =  "/pikcha - рандомная пикча с Шинобу\n"
            s3 =  "/maid - шикарные несколько артов горничных\n"
            s4 =  "/anekdot - рандомный анекдот из сборника, честно спизженного с просторов нашего необъятного\n"
            s5 =  "/rand - реши свою судьбу: да/нет\n"
            s6 =  "/encrypt - зашифруй данные по ключу\n"
            s7 =  "/decrypt - расшифруй данные по ключу\n"
            s8 =  "/delete_space - я не знаю зачем, но пусть будет - удаляет пробелы\n"
            s9 =  "/get_translate_jp - поиск слова в японском словаре\n"
            s10 = "/get_kanji - учим кандзи по хитрому файлу\n"
            s11 = "/speech_to_text - переведу войс в текст\n"
            s12 = "/text_to_speech - переведу текст в войс\n"
            s13 = "/get_quiz - викторина/тест по японским кандзи\n"
            s14 = "/get_weather - погода по текущей локации или указанному адресу\n"
            s15 = "/get_reactor_pikcha - получить рандомную пикчу по тегу с рекатора\n"
            s16 = "/get_qr_code - создать qr-код со своим текстом внутри\n"
            s17 = "/inline_mode - инлайн режимы\n"
            result_out = s0+s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+s11+s12+s13+s14+s15+s16+s17
            result_out += admin
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id) 
    elif (last_msg_user == "/main_menu"):
            content_type_out = "text"
            result_out = "Ну ок"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/stick":
            content_type_out = "sticker"
            stikers_dir = r"assets\\stickers"
            result_out = stikers_dir +"\\"+ random.choice(os.listdir(stikers_dir))
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/pikcha":
            content_type_out = "photo"
            result_out = common_methods.get_pikcha()
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
            caption_out = "Ну ты и изврат"
    elif last_msg_user == "/maid":
            content_type_out = "photo"
            maids_dir = r"assets\maids"
            result_out = maids_dir +"\\"+ random.choice(os.listdir(maids_dir))
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/anekdot":
            content_type_out = "text"
            result_out = queries_to_bd.get_joke()
            result_out = result_out.replace("it_is_new_row", "\n")
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/rand":
            content_type_out = "text"
            if random.randint(0,9) < 5:
                result_out = "Да!"
            else:
                result_out = "Нет!"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/encrypt" or last_msg_user == "/decrypt":
            content_type_out = "text"
            result_out = "Язык вводимого текста? en / ru"
            reply_out = keyboards_buttons.ru_en()
            queries_to_bd.create_session_cezar(cur_message)
    elif last_msg_bot == "Язык вводимого текста? en / ru":
            queries_to_bd.update_lang_session_cezar(cur_message)
            content_type_out = "text"
            if cur_message.text.lower() == "en":
                result_out = "Введи ключ в пределах от 0 до 26."
                reply_out = keyboards_buttons.en_key()
            elif cur_message.text.lower() == "ru":
                result_out = "Введи ключ в пределах от 0 до 32."
                reply_out = keyboards_buttons.ru_key()
            else:
                result_out = "Я для таких идиотов как ты даже кнопки сделал. ЛИБО EN, ЛИБО RU"
    elif last_msg_bot == "Введи ключ в пределах от 0 до 26." or last_msg_bot == "Введи ключ в пределах от 0 до 32.":
            content_type_out = "text"
            if last_msg_user.isnumeric() and ( (last_msg_bot == "Введи ключ в пределах от 0 до 26." and int(last_msg_user)>=0 and int(last_msg_user)<26) or (last_msg_bot == "Введи ключ в пределах от 0 до 32." and int(last_msg_user)>=0 and int(last_msg_user)<32)):
                queries_to_bd.update_key_session_cezar(cur_message)
                result_out = "Введи обрабатываемый текст"
            else:
               result_out = "Я для таких идиотов как ты даже кнопки сделал. Вводи число в соответствующем диапазоне."
            reply_out = telebot.types.ReplyKeyboardRemove()
    elif last_msg_bot == "Введи обрабатываемый текст":
            queries_to_bd.update_messaage_in_session_cezar(cur_message)
            lang, key, method, messaage_in = queries_to_bd.get_data_cezar(cur_message)
            content_type_out = "text"
            result_out = cezar.encrypt_decrypt(method, key, lang, messaage_in)
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/delete_space":
            content_type_out = "text"
            result_out = "Введи то, где надо удалить все пробелы:"
            reply_out = telebot.types.ReplyKeyboardRemove()
    elif last_msg_bot == "Введи то, где надо удалить все пробелы:":
            content_type_out = "text"
            result_out = last_msg_user.replace(" ", "")
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user.__contains__("лучшая девочка") or last_msg_user.__contains__("шинобу"):
            sentences = ["Шинобу лучшая девочка, товарищ старший лейтенант!", "Шинобу.", "Однозначно Шинобу!", "Лучшая девочка-та, ради кого я создан, это Шинобу!", "Шинобу", "Солышко мое Шинобу", "А я уже кидал пикчу с Шинобу?", "А я уже кидал стикос с Шинобу?"]
            value = random.randint(0,len(sentences))
            content_type_out = "text"
            result_out = sentences[value]
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user =="/speech_to_text":
            content_type_out = "text"
            result_out = "Выбери язык распознавания текста"
            reply_out = keyboards_buttons.ru_en()
    elif last_msg_bot == "Выбери язык распознавания текста":
            content_type_out = "text"
            if cur_message.text.lower() == "en" or cur_message.text.lower() == "ru":
                queries_to_bd.create_session_voice(cur_message)
                result_out = "Присылай войс для распознавания"
                reply_out = telebot.types.ReplyKeyboardRemove()
            else:
                result_out = "Я для таких идиотов как ты даже кнопки сделал. ЛИБО EN, ЛИБО RU"
                reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_bot =="Присылай войс для распознавания":
            content_type_out = "text"
            if cur_message.content_type == "voice":
                lang = (queries_to_bd.get_lang_voice(cur_message)).lower()
                result_out = r"'" + speech_to_text.voice_processing(cur_message, bot, lang )+ r"'" #вызов функции конвертации
                queries_to_bd.insert_result_recognize_speech(cur_message, result_out)
            else:
                result_out = "Что-то не похоже на войс, попробуй еще разок"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user =="/text_to_speech":
            content_type_out = "text"
            result_out = "Выбери язык войса"
            reply_out = keyboards_buttons.ru_en()
    elif last_msg_bot == "Выбери язык войса":
            content_type_out = "text"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
            if last_msg_user == "ru":
                result_out = "А теперь напиши текст на русском языке, который будет переведен в войс"
            elif last_msg_user == "en":
                result_out = "А теперь напиши текст на английском языке, который будет переведен в войс"
            else:
                result_out = "Я для таких идиотов как ты даже кнопки сделал. ЛИБО EN, ЛИБО RU"
    elif last_msg_bot == "А теперь напиши текст на русском языке, который будет переведен в войс":
            if cur_message.content_type == "text":
                if common_methods.check_ru_char_in_string(last_msg_user) == 0:
                    content_type_out = "audio"
                    result_out = text_to_speech.convert_text_to_speech(last_msg_user,"ru")
                else:
                    content_type_out = "text"
                    result_out = "Кажется, твой текст не весь состоит из русских букв.\nПопробуй снова. Допускаются только русские буквы."
            else:
                content_type_out = "text"
                result_out = "Ты тупой или да? Пиши ТЕКСТ"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_bot == "А теперь напиши текст на английском языке, который будет переведен в войс":
            if cur_message.content_type == "text":
                if common_methods.check_en_char_in_string(last_msg_user) == 0:
                    content_type_out = "audio"
                    result_out = text_to_speech.convert_text_to_speech(last_msg_user,"en")
                else:
                    content_type_out = "text"
                    result_out = "Кажется, твой текст не весь состоит из английских букв.\nПопробуй снова. Допускаются только английские буквы."
            else:
                content_type_out = "text"
                result_out = "Ты тупой или да? Пиши ТЕКСТ"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/get_translate_jp":
            content_type_out = "text"
            result_out = "Какое слово ищем в японском словаре?"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_bot == "Какое слово ищем в японском словаре?":
            content_type_out = "text"
            result_out = queries_to_bd.get_translate_jp(last_msg_user)
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
            #если в бд ничего не найдено, то спрашиваем у ChatGPT
            if result_out == 'Мы ничего не нашли':
                result_out = ChatGpt.get_result_from_chatgpt("Переведи с японского на русский язык: " + last_msg_user)
    elif last_msg_user == "/get_kanji":
            content_type_out = "text"
            result_out = "Пришлю десяток кандзи из словаря для изучения. Какой номер десятка?"
            reply_out = keyboards_buttons.kanji_num()
    elif last_msg_bot == "Пришлю десяток кандзи из словаря для изучения. Какой номер десятка?":
            content_type_out = "text"
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
            if last_msg_user.isnumeric():
                result_out = queries_to_bd.get_kanji(last_msg_user)
            else:
                result_out = "Введенное тобой что-то не похоже на число."
    elif last_msg_user == "/get_quiz":
            content_type_out = "text"
            result_out = "Квиз по всем имеющимся кандзи или по номеру определенного десятка?"
            reply_out = keyboards_buttons.kanji_quiz()
    elif last_msg_bot == "Квиз по всем имеющимся кандзи или по номеру определенного десятка?" and last_msg_user == "по всем имеющимся кандзи!":
            answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out = quiz.get_all_kanji_quiz()
            poll_type_out = "quiz"
    elif last_msg_bot == "Квиз по всем имеющимся кандзи или по номеру определенного десятка?" and last_msg_user == "по номеру десятка!":
            content_type_out = "text"
            result_out = "По какому номеру десятка кандзи будем гонять?"
            reply_out = keyboards_buttons.kanji_num()
    elif last_msg_bot == "По какому номеру десятка кандзи будем гонять?":
            if last_msg_user.isnumeric():
                poll_type_out = "quiz"
                answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out = quiz.get_decade_kanji_quiz(last_msg_user)
            else:
                content_type_out = "text"
                result_out = "Введенное тобой что-то не похоже на число."
    elif last_msg_bot == "квиз по всем имеющимся кандзи" and last_msg_user == "еще":
            answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out = quiz.get_all_kanji_quiz()
            poll_type_out = "quiz"
    elif last_msg_bot == "квиз по по номеру десятка кандзи" and last_msg_user == "еще":
            pre_last_msg_user = queries_to_bd.get_pre_last_user_msg(cur_message.chat.id)
            answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out = quiz.get_decade_kanji_quiz(pre_last_msg_user)
            poll_type_out = "quiz"
    elif last_msg_user == "/send_to_admin":
            content_type_out = "text"
            result_out = "Что хотите отправить? Принимаются текст, фото, видео, войсы, видео заметки."
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_bot == "Что хотите отправить? Принимаются текст, фото, видео, войсы, видео заметки.":
            resending_flg = 1
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/adminka":
            if cur_message.chat.id == cfg.id_owner:
                content_type_out = "text"
                result_out = "Здравствуйте, мой господин"
                reply_out = keyboards_buttons.admin_panel()
            else:
                content_type_out = "text"
                result_out = "Что-то не похоже, чтобы ты был админом."
                reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/get_users":
            if cur_message.chat.id == cfg.id_owner:
                content_type_out = "text"
                result_out = queries_to_bd.get_users()
                reply_out = keyboards_buttons.admin_panel()
                parse_mode_out = 'MarkdownV2'
            else:
                content_type_out = "text"
                result_out = "Что-то не похоже, чтобы ты был админом."
                reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/send_to_user":
            if cur_message.chat.id == cfg.id_owner:
                content_type_out = "text"
                result_out = 'Блок отправки сообщений пользователю.\nКому отправляем? (chat_id)'
                reply_out = keyboards_buttons.admin_panel()
            else:
                content_type_out = "text"
                result_out = "Что-то не похоже, чтобы ты был админом."
                reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_bot.__contains__("Блок отправки сообщений пользователю."):
            if last_msg_bot.__contains__("Кому отправляем? (chat_id)"):
                if cur_message.chat.id == cfg.id_owner:
                    content_type_out = "text"
                    result_out = 'Блок отправки сообщений пользователю.\nЧто отправляем?'
                    reply_out = keyboards_buttons.admin_panel()
                else:
                    content_type_out = "text"
                    result_out = "Что-то не похоже, чтобы ты был админом."
                    reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
            elif last_msg_bot.__contains__("Что отправляем?"):
                if cur_message.chat.id == cfg.id_owner:
                    resending_flg = 1
                    reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
                else:
                    content_type_out = "text"
                    result_out = "Что-то не похоже, чтобы ты был админом."
                    reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/get_weather":
            content_type_out = "text"
            result_out = "В какой области будем смотреть прогноз погоды? (Можешь отправить текущую локацию или написать адрес текстом.)"
            reply_out = keyboards_buttons.weather_place()
    elif last_msg_bot == "В какой области будем смотреть прогноз погоды? (Можешь отправить текущую локацию или написать адрес текстом.)":
            content_type_out = "text"
            if cur_message.content_type == 'text' or cur_message.content_type == 'location':
                result_out = weather.current_weather(cur_message)
                reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
            else:
                result_out = "Адрес нужен в виде текста или локации."
    elif last_msg_user == "/get_reactor_pikcha":
            content_type_out = "text"
            result_out = "Какую рандомную пикчу ищем на реакторе?"
            reply_out = telebot.types.ReplyKeyboardRemove()
    elif last_msg_bot == "Какую рандомную пикчу ищем на реакторе?":
            content_type_out = "photo"
            parse_mode_out, caption_out, result_out = common_methods.get_random_pikcha_by_teg(last_msg_user)
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/get_qr_code":
            content_type_out = "text"
            result_out = "Введи текст, который будет помещен в qr-код."
            reply_out = telebot.types.ReplyKeyboardRemove()
    elif last_msg_bot == "Введи текст, который будет помещен в qr-код.":
            content_type_out = "document"
            result_out = common_methods.create_qr_code(last_msg_user)
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
    elif last_msg_user == "/inline_mode":
            content_type_out = "text"
            result_out = "Значит, объясняю, что это такое и как пользоваться:\n\nИнлайн режим - это когда ты в чате с другим пользователем пишешь никнейм этого бота, а затем то, что хочешь найти. Например:\n@ArarararagiBot pic Шинобу Ошино\n\nи он тебе выдаст пикчи Ошино Шинобу\nСейчас пока работает только с пикчами - pic, чуть позже добавлю видео, ссылки, стикеры и еще что-нибудь\nнаслаждайся."
            reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
            
    elif last_msg_user == "/get_inline_kb":
            content_type_out = "text"
            result_out = "Это инлайн клавиатура"
            reply_out = keyboards_buttons.inline_kb()
    else:
        content_type_out = "text"
        result_out = ChatGpt.get_result_from_chatgpt(last_msg_user)
        #result_out = queries_to_bd.get_other_answer(last_msg_user)
        reply_out = keyboards_buttons.main_menu(cur_message.chat.id)
        
    return resending_flg, poll_type_out, parse_mode_out, answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out, caption_out