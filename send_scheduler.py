import keyboards_buttons
import common_methods
import queries_to_bd
import datetime
import sending
import time

#Метод для шедулера - это будет дочерний поток
def time_schedule_bot(MypyBot):
        cur_date_time = datetime.datetime.now()

        #if (cur_date_time.second % 2 == 0):
        #
        #    #отправка рандомного сердечка
        #    try:
        #        cur_send_mode = 'default_mode'
        #        cur_type_data = 'text'
        #        heart_string = '❤️🤍💗💚💙💕💝💘💖💞🤎❣️🖤💓♥️🧡❤️'
        #        cur_text_data = random.choice(heart_string), None, None, None
        #        sending.send_msg(bot             = MypyBot,
        #                         send_mode       = cur_send_mode,
        #                         chat_id         = 83729683,
        #                         type_data       = cur_type_data,
        #                         text_data       = cur_text_data)

        #        cur_text_data = random.choice(heart_string), None, None, None
        #        sending.send_msg(bot             = MypyBot,
        #                         send_mode       = cur_send_mode,
        #                         chat_id         = my_cfg.id_owner,
        #                         type_data       = cur_type_data,
        #                         text_data       = cur_text_data)
        #    except Exception as e:
        #        print('Heart is not sending')

        #    print('Отработка ежесекундного шедулера')

        if (cur_date_time.minute == 00 and cur_date_time.second == 00):
            #отправка пикчи
            list_users_id = queries_to_bd.get_users_id_of_current_subscription('Пикча с Шинобу')
            for item in list_users_id:
                try:
                    cur_send_mode = 'default_mode'
                    cur_type_data = 'photo'
                    cur_spoiler   = True
                    reply_markup  = None
                    cur_photo_data = common_methods.get_pikcha(), reply_markup, 'Ежечасное солнышко\n' + "||Управление подписками:\n/managesubscriptions||" , 'MarkdownV2', cur_spoiler
                    sending.send_msg(bot             = MypyBot,
                                     send_mode       = cur_send_mode,
                                     chat_id         = item,
                                     type_data       = cur_type_data,
                                     photo_data      = cur_photo_data)

                except Exception as e:
                    print('Не отправлено сообщение этому пользователю: ' +str(item)+'. Текст ошибки:\n'+str(e))

            #отправка комплимента
            list_users_id = queries_to_bd.get_users_id_of_current_subscription('Комплименты девушке')
            for item in list_users_id:
                try:
                    cur_type_data = 'text'
                    reply_markup_out = keyboards_buttons.create_inline_kb({"see_subscriptions": "Смотреть подписки"}, 1)
                    cur_text_data = queries_to_bd.get_compliment(), reply_markup_out, None, None
                    sending.send_msg(bot             = MypyBot,
                                     send_mode       = cur_send_mode,
                                     chat_id         = item,
                                     type_data       = cur_type_data,
                                     text_data       = cur_text_data)

                except Exception as e:
                    print('Не отправлено сообщение этому пользователю: ' +str(item)+'. Текст ошибки:\n'+str(e))

            print('Отработка ежечасного шедулера')

        if (cur_date_time.hour == 22 and cur_date_time.minute == 00 and cur_date_time.second == 00):

            #отправка праздника
            today_holiday = queries_to_bd.get_holiday()
            if len(today_holiday) > 0:
                list_users_id = queries_to_bd.get_users_id_of_current_subscription('Международные праздники')
                today_holiday = 'Сегодня ' + today_holiday.lower() + '🎉\nС праздничком:)'
                for item in list_users_id:
                    try:
                        cur_send_mode = 'default_mode'
                        cur_type_data = 'text'
                        reply_markup_out = keyboards_buttons.create_inline_kb({"see_subscriptions": "Смотреть подписки"}, 1)
                        cur_text_data = today_holiday, reply_markup_out, None, None
                        sending.send_msg(bot             = MypyBot,
                                         send_mode       = cur_send_mode,
                                         chat_id         = item,
                                         type_data       = cur_type_data,
                                         text_data       = cur_text_data)

                    except Exception as e:
                        print('Не отправлено сообщение этому пользователю: ' +str(item)+'. Текст ошибки:\n'+str(e))
            print('Отработка ежедневного шедулера')

