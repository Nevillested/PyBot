import keyboards_buttons
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
import my_cfg
import time

MypyBot = telebot.TeleBot(my_cfg.telegram_token, parse_mode = None)

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
            print(f"Пользователь {edited_message.from_user.username} отредактировал сообщение.\n")
            
            #добавляет отредактированное сообщение
            queries_to_bd.insert_edited_msg(edited_message)
            
            #получает предпоследнеюю версию сообщения и обрамляет ее в результат
            result_prev_msg = "Ты думаешь я ничего не видел?\n" + r"|| '" + queries_to_bd.get_last_ver_msg(edited_message)+ r"' ||"
            
            #формирует текстовые данные
            cur_text_data = result_prev_msg, None, 'MarkdownV2', edited_message.id

            #отправляет и сохраняет
            sending.send_msg(bot             = MypyBot,
                             send_mode       = 'default_mode',
                             chat_id_out     = edited_message.chat.id,
                             type_data_out   = 'text',
                             text_data_out   = cur_text_data,
                             flg_counter_msg = 0)
                
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
            
            if message.via_bot != True:
                queries_to_bd.get_users_id()
                print(f"Пришло сообщение от: {message.from_user.username}\nТип сообщения: {str(message.content_type)}\nТекст сообщения: {message.text}\n")
                
                #проверяет пользователя в бд, если есть-обновляет данные, если нет-добавляет данные
                queries_to_bd.check_user(message)
                
                #сохраняет прилетевшие данные от пользователя
                queries_to_bd.insert_user_story_in(message)
                
                #получение результатов для ответа пользователю
                (bot, send_mode, chat_id, msg_id, type_data, text_data, poll_data, photo_data, sticker_data, audio_data, doc_data) = answer_cases.cases_trigger(MypyBot, message)
                
                #отправляет результат
                sending.send_msg(bot, send_mode, message, chat_id, msg_id, type_data, text_data, poll_data, photo_data, sticker_data, audio_data, doc_data)
                
        except Exception as e:
            print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))
    
    MypyBot.polling()
            

#Шедулер
def time_schedule_bot():
    while True:

        time.sleep(60)

        cur_date_time = datetime.datetime.now()

        if (cur_date_time.minute == 00):
            
            #отправка пикчи
            list_users_id = queries_to_bd.get_users_id_of_current_subscription('Пикча с Шинобу')
            for item in list_users_id:
                try:
                    cur_send_mode = 'default_mode'
                    cur_type_data = 'photo'
                    cur_photo_data = common_methods.get_pikcha(), None, 'Ежечасное солнышко\n' + "||Управление подписками:\n/managesubscriptions||" , 'MarkdownV2'
                    sending.send_msg(bot             = MypyBot,
                                     send_mode       = cur_send_mode,
                                     chat_id_out     = item,
                                     type_data_out   = cur_type_data,
                                     photo_data_out  = cur_photo_data,
                                     flg_counter_msg = 0)
                                         
                except Exception as e:
                    print('Не отправлено сообщение этому пользователю: ' +str(item)+'. Текст ошибки:\n'+str(e))

            #отправка комплимента
            list_users_id = queries_to_bd.get_users_id_of_current_subscription('Комплименты девушке')
            for item in list_users_id:
                try:
                    cur_type_data = 'text'
                    reply_markup_out = keyboards_buttons.create_inline_kb({"manage_subscriptions": "Управление подписками"})
                    cur_text_data = queries_to_bd.get_compliment(), reply_markup_out, None, None
                    sending.send_msg(bot             = MypyBot,
                                     send_mode       = cur_send_mode,
                                     chat_id_out     = item,
                                     type_data_out   = cur_type_data,
                                     text_data_out   = cur_text_data,
                                     flg_counter_msg = 0)
                                         
                except Exception as e:
                    print('Не отправлено сообщение этому пользователю: ' +str(item)+'. Текст ошибки:\n'+str(e))

            print('Отработка ежечасного шедулера')
        
        if (cur_date_time.hour == 22 and cur_date_time.minute == 00):
            
            #отправка праздника
            today_holiday = queries_to_bd.get_holiday()
            if len(today_holiday) > 0:
                list_users_id = queries_to_bd.get_users_id_of_current_subscription('Международные праздники')
                today_holiday = 'Сегодня ' + today_holiday.lower() + '🎉\nС праздничком:)'
                for item in list_users_id:
                    try:
                        cur_send_mode = 'default_mode'
                        cur_type_data = 'text'
                        reply_markup_out = keyboards_buttons.create_inline_kb({"manage_subscriptions": "Управление подписками"})
                        cur_text_data = today_holiday, reply_markup_out, None, None
                        sending.send_msg(bot             = MypyBot,
                                         send_mode       = cur_send_mode,
                                         chat_id_out     = item,
                                         type_data_out   = cur_type_data,
                                         text_data_out   = cur_text_data,
                                         flg_counter_msg = 0)

                    except Exception as e:
                        print('Не отправлено сообщение этому пользователю: ' +str(item)+'. Текст ошибки:\n'+str(e))
            print('Отработка ежедневного шедулера')


#создаем поток на основной держатель всех ивентов бота и на шедулер
thread_1 = threading.Thread(target=main_bot)
thread_2 = threading.Thread(target=time_schedule_bot)

#запускаем потоки
thread_1.start()
thread_2.start()
