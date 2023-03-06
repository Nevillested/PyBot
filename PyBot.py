from logging import exception
import keyboards_buttons
import common_methods
import queries_to_bd
import answer_cases
import threading
import traceback
import telebot
import sending

MypyBot = telebot.TeleBot('2024376867:AAEwo60MQbbuvTAFMxCC_orH1t7Xyduj5So', parse_mode = None)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

#основной держатель всех ивентов бота
def main_bot():
    
    @MypyBot.edited_message_handler(content_types="text")
    def catch_edit_msg(message):
        try:
            print(f"Пользователь {message.from_user.username} отредактировал сообщение.\n")
    
            #добавляет отредактированное сообщение
            queries_to_bd.insert_edited_msg(message)
    
            #получает предпоследнеюю версию сообщения и обрамляет ее в результат
            result_prev_msg = "Ты думаешь я ничего не видел?\n" + r"|| '" + queries_to_bd.get_last_ver_msg(message)+ r"' ||"
    
            #отправляет результат
            MypyBot.send_message(message.chat.id, result_prev_msg , reply_to_message_id = message.id, parse_mode='MarkdownV2')
            
            #сохраняет улетевшие данные пользователю
            queries_to_bd.insert_user_story_out("text", result_prev_msg, message.chat.id, message.message_id)
    
        except Exception as e:
            print('Ошибочка в PyBot.edited_message_handler\nОписание: ' + "".join(traceback.format_exception_only(e)).strip())
            MypyBot.send_message(message.chat.id, "Ок, допустим кря\nДопустим, ты сделал ошибку в работе бота\nНо это только ДОПУСТИМ\nИ что дальше ты намерен делать?", reply_markup = keyboards_buttons.main_menu(message.chat.id))
            
    
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
            print('Ошибочка в PyBot.message_handler\nОписание: ' + "".join(traceback.format_exception_only(e)).strip())
            MypyBot.send_message(message.chat.id, "Ок, допустим кря\nДопустим, ты сделал ошибку в работе бота\nНо это только ДОПУСТИМ\nИ что дальше ты намерен делать?", reply_markup = keyboards_buttons.main_menu(message.chat.id))
    
    
    MypyBot.polling() 

#отправщик пикч по времени. Короче говоря - шедулер
def time_schedule_bot():

    def send_time_pikcha():
        try:
            threading.Timer(3600.0, send_time_pikcha).start()
            content_type_out = 'photo'
            result_out = common_methods.get_pikcha()
            content_type_out, result_out = sending.send_msg( 0,
                                                             None,
                                                             MypyBot,
                                                             sending.id_owner,
                                                             content_type_out,
                                                             result_out,
                                                             None,
                                                             None,
                                                             None,
                                                             None,
                                                             None,
                                                             None,
                                                             None)
            print('Отправка ежечасной пикчи!')
        except Exception as e:
            print('При отправке ежечасной пикчи произошла ошибка: \n' + e)

    send_time_pikcha()
    
thread_main_bot = threading.Thread(target=main_bot)
thread_time_schedule_bot = threading.Thread(target=time_schedule_bot)

thread_main_bot.start()
thread_time_schedule_bot.start()