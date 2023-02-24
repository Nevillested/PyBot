from email import message
import queries_to_bd
import answer_cases
import traceback
import telebot

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
        queries_to_bd.insert_edited_msg(message)

        #получает предпоследнеюю версию сообщения и обрамляет ее в результат
        result_prev_msg = "Ты думаешь я ничего не видел?\n" + r"|| '" + queries_to_bd.get_last_ver_msg(message)+ r"' ||"
        
        #сохраняет улетевшие данные пользователю
        queries_to_bd.insert_user_story_out("text", result_prev_msg, message.chat.id, message.message_id)

        #отправляет результат
        MypyBot.send_message(message.chat.id, result_prev_msg , reply_to_message_id = message.id, parse_mode='MarkdownV2')

    except Exception as e:
        print('Ошибочка в PyBot.edited_message_handler\nОписание: ' + "".join(traceback.format_exception_only(e)).strip())
        MypyBot.send_message(message.chat.id, "Ок, допустим кря\nДопустим, ты сделал ошибку в работе бота\nНо это только ДОПУСТИМ\nИ что дальше ты намерен делать?")
        

#callback_query_handler пока в тесте
@MypyBot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        MypyBot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        MypyBot.answer_callback_query(call.id, "Answer is No")


@MypyBot.message_handler(content_types=CONTENT_TYPES)
def start_message(message):
    try:
        print(f"Пришло сообщение от: {message.from_user.username}\nТип сообщения: {str(message.content_type)}\nТекст сообщения: {message.text}\n")

        #проверяет пользователя в бд, если есть-обновляет данные, если нет-добавляет данные
        queries_to_bd.check_user(message)

        #сохраняет прилетевшие данные в переписке с пользователем
        queries_to_bd.insert_user_story_in(message)

        #получает последнее свое отправленное сообщение
        last_msg_bot = queries_to_bd.get_last_bot_msg(message.chat.id)
        
        #кейсы на ответы пользователю - получение результатов ответа (получение типа контента, который отправляется пользователю, содержимое контента и реплай-контент)
        parse_mode_out, answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out = answer_cases.cases_class.cases_trigger(message, last_msg_bot, MypyBot)
        
        #если результат - список, то возьмем первую строку из списка. Эта строка - название исходящих данных
        result_array_out = result_out
        if str(type(result_array_out)) == '<class \'list\'>':
            result_out = result_out[0]
            result_array_out.pop(0)

        #сохраняет улетевшие данные пользователю
        queries_to_bd.insert_user_story_out(content_type_out, result_out, message.chat.id, message.message_id)

        #отправляет результат
        if content_type_out == "text":
            MypyBot.send_message(message.chat.id, result_out, reply_markup = reply_out, parse_mode = parse_mode_out)
        elif content_type_out == "sticker":
            MypyBot.send_sticker(message.chat.id, result_out, reply_markup = reply_out)
        elif content_type_out == "photo":
            caption_result = ""
            if message.text.lower() == "/pikcha":
                caption_result = "Ну ты и изврат"
            MypyBot.send_photo(message.chat.id, photo = open(result_out, 'rb'), caption = caption_result, reply_markup = reply_out)
        elif content_type_out == "audio":
            #MypyBot.send_voice(message.chat.id, result_out) #метод send_voice не работает по непонятным причинам апи телеги
            MypyBot.send_audio(chat_id=message.chat.id, audio=open(result_out, 'rb'), reply_markup = reply_out)
        elif content_type_out == "poll":
            MypyBot.send_poll(message.chat.id, 'Кандзи: ' + answer_desc_out, options = result_array_out, correct_option_id  = correct_answer_id_out, type = 'quiz', reply_markup = reply_out)
        elif content_type_out == "document":
            document = open(result_out, 'rb')
            MypyBot.send_document(message.chat.id, document, reply_markup = reply_out)
            
    except Exception as e:
        print('Ошибочка в PyBot.message_handler\nОписание: ' + "".join(traceback.format_exception_only(e)).strip())
        MypyBot.send_message(message.chat.id, "Ок, допустим кря\nДопустим, ты сделал ошибку в работе бота\nНо это только ДОПУСТИМ\nИ что дальше ты намерен делать?")

MypyBot.polling() 