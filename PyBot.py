import keyboards_buttons
import music_processing
import common_methods
import callback_data
import queries_to_bd
import answer_cases
import inline_mode
import threading
import send_scheduler
import inspect
import telebot
import sending
import my_cfg
import random
import datetime
import time

music_processing.prepare_data()

MypyBot = telebot.TeleBot(my_cfg.telegram_token, parse_mode = None)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

#хэндлер успешных платежей
@MypyBot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    try:
        print(f"Донат от: {message.from_user.username}!")
        MypyBot.send_message(message.chat.id,
                             'Атлы, все прошло успешно. Сейчас мы обработаем платеж `{} {}` настолько быстро насколько это вообще в принципе возможно.\nОставайтесь с нами и спасибо за покупку!'.format(
                                 message.successful_payment.total_amount / 100, message.successful_payment.currency),
                             parse_mode='Markdown')
                             
        queries_to_bd.upd_data_for_payment(message)  

    except Exception as e:
        print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))

#хэнделер ошибок оплаты
@MypyBot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    try:
        MypyBot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                          error_message="Ты не поверишь, пришельцы пытались украсть твой CVV-код, но я отбился. Сейчас я отдохну пару мин, а ты затем попробуй еще разок.")

    except Exception as e:
        print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))


#хэндер ивентов редактирования сообщения пользователем
@MypyBot.edited_message_handler(content_types="text")
def catch_edit_msg(edited_message):
    try:
        print(f"Пользователь {edited_message.from_user.username} отредактировал сообщение.\n")
        
        #добавляет отредактированное сообщение
        cur_data = (str(edited_message.text), str(edited_message.chat.id), str(edited_message.message_id))
        queries_to_bd.insert_edited_msg_by_user(cur_data)
        
        #получает предпоследнеюю версию сообщения и обрамляет ее в результат
        cur_data = (str(edited_message.chat.id), str(edited_message.message_id))
        result_prev_msg = "Ты думаешь я ничего не видел?\n" + r"|| '" + queries_to_bd.get_last_ver_msg(cur_data)+ r"' ||"
        
        #формирует текстовые данные
        cur_text_data = result_prev_msg, None, 'MarkdownV2', edited_message.id

        #отправляет и сохраняет
        sending.send_msg(bot             = MypyBot,
                         send_mode       = 'default_mode',
                         chat_id_out     = edited_message.chat.id,
                         msg_id_out      = edited_message.message_id + 1,
                         type_data_out   = 'text',
                         text_data_out   = cur_text_data)
            
    except Exception as e:
        print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))

#хэндер ивентов инлайн-запросов
@MypyBot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    try:
        print(f"{query.from_user.username} сделал inline запрос: {query.query}.\n")

        #метод обработки всех инлайн запросов
        inline_mode.inline_mode_processed(MypyBot, query)

    except Exception as e:
        print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))
    
#хэндер ивентов колбэкдаты инлайн кнопок
@MypyBot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        print(f"{call.from_user.username} нажал кнопку {call.data}.\n")
        
        #метод обработки всех инлайн кнопок
        callback_data.call_processed(MypyBot, call) 

    except Exception as e:
        print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))

#хэндер простых сообщений   
@MypyBot.message_handler(content_types=CONTENT_TYPES)
def start_message(message):
    try:
        #if message.via_bot != True:
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

#шедулер
def scheduler():
    while True:
        try:
            send_scheduler.time_schedule_bot(MypyBot)
            time.sleep(1)            
        except Exception as e:
            print(f'В {str(inspect.stack()[0][3])} произошла ошибка: \n' + str(e))


child_thread = threading.Thread(target=scheduler)
child_thread.start()
MypyBot.polling(none_stop=True)