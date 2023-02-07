from email import message
import telebot
import queries_to_bd
import answer_cases
import keyboards_buttons
import traceback

MypyBot = telebot.TeleBot('2024376867:AAEwo60MQbbuvTAFMxCC_orH1t7Xyduj5So', parse_mode = None)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


@MypyBot.edited_message_handler(content_types="text")
def catch_edit_msg(message):
    try:
        print(f"Пользователь {message.from_user.username} отредактировал сообщение.\n")

        #добавляет отредактированное сообщение
        queries_to_bd.queries_class.insert_edited_msg(message)

        #получает предпоследнеюю версию сообщения
        prev_msg = queries_to_bd.queries_class.get_last_ver_msg(message)
        
        #отправляет результат
        MypyBot.send_message(message.chat.id, "Ты думаешь я ничего не видел?\n" + r"|| '" + prev_msg + r"' ||", reply_to_message_id  = message.id, parse_mode='MarkdownV2')

    except Exception as e:
        print('Ошибочка в PyBot.edited_message_handler\nОписание: ' + "".join(traceback.format_exception_only(e)).strip())
        MypyBot.send_message(message.chat.id, "Ок, допустим кря\nДопустим, ты сделал ошибку в работе бота\nНо это только ДОПУСТИМ\nИ что дальше ты намерен делать?", reply_markup  = keyboards_buttons.keyboards_class.main_menu())


@MypyBot.message_handler(content_types=CONTENT_TYPES)
def start_message(message):

    try:
        print(f"Пришло сообщение от: {message.from_user.username}\nТип сообщения: {str(message.content_type)}\nТекст сообщения: {message.text}\n")

        #пересылает все прилетевшее боту - админу
        #resending_to_owner_motherfucker.resend(message)

        #проверяет пользователя в бд, если есть-обновляет данные, если нет-добавляет данные
        queries_to_bd.queries_class.check_user(message)

        #сохраняет прилетевшие данные в переписке с пользователем
        queries_to_bd.queries_class.insert_user_story_in(message)

        #получает последнее свое отправленное сообщение
        last_msg_bot = queries_to_bd.queries_class.get_last_bot_msg(message.chat.id)
        
        #кейсы на ответы пользователю - получение результатов ответа (получение типа контента, который отправляется пользователю, содержимое контента и реплай-контент)
        content_type, result, reply = answer_cases.cases_class.cases_trigger(message, last_msg_bot, MypyBot)
        
        #сохраняет улетевшие данные пользователю
        queries_to_bd.queries_class.insert_user_story_out(content_type, result, message.chat.id, message.message_id)

        #отправляет результат
        if content_type == "text":
            MypyBot.send_message(message.chat.id, result, reply_markup  = reply)
        elif content_type == "sticker":
            MypyBot.send_sticker(message.chat.id, result)
        elif content_type == "photo":
            caption_result = ""
            if message.text.lower() == "/pikcha":
                caption_result = "Ну ты и изврат"
            MypyBot.send_photo(message.chat.id, photo = open(result, 'rb'), caption = caption_result)
            
    except Exception as e:
        print('Ошибочка в PyBot.message_handler\nОписание: ' + "".join(traceback.format_exception_only(e)).strip())
        MypyBot.send_message(message.chat.id, "Ок, допустим кря\nДопустим, ты сделал ошибку в работе бота\nНо это только ДОПУСТИМ\nИ что дальше ты намерен делать?", reply_markup  = keyboards_buttons.keyboards_class.main_menu())

MypyBot.polling() 