import common_methods
import callback_data
import queries_to_bd
import answer_cases
import inline_mode
import threading
import inspect
import telebot
import sending
import datetime
import cfg

MypyBot = telebot.TeleBot(cfg.telegram_token, parse_mode = None)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

#основной держатель всех ивентов бота
def main_bot():
    #хэндер ивентов редактирования сообщения пользователем
    @MypyBot.edited_message_handler(content_types="text")
    def catch_edit_msg(edited_message):
        try:
            if edited_message.via_bot.username != 'ArarararagiBot' and edited_message.via_bot.is_bot != True:
                print(f"Пользователь {edited_message.from_user.username} отредактировал сообщение.\n")
                
                #добавляет отредактированное сообщение
                queries_to_bd.insert_edited_msg(edited_message)
                
                #получает предпоследнеюю версию сообщения и обрамляет ее в результат
                result_prev_msg = "Ты думаешь я ничего не видел?\n" + r"|| '" + queries_to_bd.get_last_ver_msg(edited_message)+ r"' ||"
                
                #отправляет результат
                MypyBot.send_message(edited_message.chat.id, result_prev_msg , reply_to_message_id = edited_message.id, parse_mode='MarkdownV2')
                
                #сохраняет улетевшие данные пользователю
                queries_to_bd.insert_user_story_out("text", result_prev_msg, edited_message.chat.id, edited_message.message_id)
        except Exception as e:
            print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))

    #хэндер ивентов инлайн-запросов
    @MypyBot.inline_handler(lambda query: len(query.query) > 0)
    def query_text(query):
        try:
            print(f"{query.from_user.username} сделал inline запрос: {query.query}.\n")

            inline_mode.inline_mode_processed(MypyBot, query)

        except Exception as e:
            print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))
        
    #хэндер ивентов колбэкдаты инлайн кнопок
    @MypyBot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            print(f"{call.from_user.username} нажал кнопку {call.data}.\n")

            callback_data.call_processed(MypyBot, call)

        except Exception as e:
            print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))

    #хэндер простых сообщений
    @MypyBot.message_handler(content_types=CONTENT_TYPES)
    def start_message(message):
        try:
            if message.via_bot.username != 'ArarararagiBot' and message.via_bot.is_bot != True:
                print(f"Пришло сообщение от: {message.from_user.username}\nТип сообщения: {str(message.content_type)}\nТекст сообщения: {message.text}\n")
                
                #проверяет пользователя в бд, если есть-обновляет данные, если нет-добавляет данные
                queries_to_bd.check_user(message)
                
                #сохраняет прилетевшие данные от пользователя
                queries_to_bd.insert_user_story_in(message)
                
                #получение результатов для ответа пользователю
                (resending_flg,
                     poll_type_out,
                     parse_mode_out,
                     answer_desc_out,
                     correct_answer_id_out,
                     content_type_out,
                     result_out,
                     reply_out,
                     caption_out) = answer_cases.cases_trigger(message, MypyBot)
                
                #отправляет результат
                content_type_out, result_out = sending.send_msg( resending_flg,
                                                                     message,
                                                                     MypyBot,
                                                                     message.chat.id,
                                                                     content_type_out,
                                                                     result_out,
                                                                     reply_out,
                                                                     parse_mode_out,
                                                                     caption_out,
                                                                     answer_desc_out,
                                                                     result_out,
                                                                     correct_answer_id_out,
                                                                     poll_type_out)
                
                #сохраняет улетевшие данные пользователю
                queries_to_bd.insert_user_story_out(content_type_out, result_out, message.chat.id, message.message_id)
        except Exception as e:
            print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))

    MypyBot.polling()
            

#Шедулер
def time_schedule_bot():
    def send_time_pikcha():
        try:
            threading.Timer(60.0, send_time_pikcha).start()
            if (datetime.datetime.now().minute == 00):
                #отправка пикчи
                content_type_out, result_out = sending.send_msg( 0,
                                                                 None,
                                                                 MypyBot,
                                                                 cfg.id_owner,
                                                                 'photo',
                                                                 common_methods.get_pikcha(),
                                                                 None,
                                                                 None,
                                                                 'Ежечасное солнышко',
                                                                 None,
                                                                 None,
                                                                 None,
                                                                 None)
                #отправка комплимента
                #content_type_out, result_out = sending.send_msg( 0,
                #                                                 None,
                #                                                 MypyBot,
                #                                                 83729683,
                #                                                 'text',
                #                                                 queries_to_bd.get_compliment(),
                #                                                 None,
                #                                                 None,
                #                                                 'Ежечасное солнышко',
                #                                                 None,
                #                                                 None,
                #                                                 None,
                #                                                 None)
                print('Отработка ежечасного шедулера')

        except Exception as e:
            print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))

    send_time_pikcha()

#создаем поток на основной держатель всех ивентов бота и на шедулер
thread_main_bot = threading.Thread(target=main_bot)
thread_time_schedule_bot = threading.Thread(target=time_schedule_bot)

#запускаем потоки
thread_main_bot.start()
thread_time_schedule_bot.start()