import keyboards_buttons
import queries_to_bd
import payments
import sending
import telebot
import os
import music_processing
import threading

def call_processed(bot, call):
    # Если сообщение из чата с ботом
    if call.message:

        chat_id_out      = call.message.chat.id
        message_id_out   = call.message.message_id
        text_out         = None
        reply_markup_out = None
        btn_name_out     = call.data

        #Меню с подписками ID = 1.
        #Меню с платежками ID = 2.
        #Меню с музыкой ID = 3.
        #Меню с напоминалками ID = 4.

        #Меню кнопок с подписками ID = 1
        if call.data.startswith("id_1_"):

            dict_of_user_subscriptions = queries_to_bd.get_subscriptions_user(call.message.chat.id)
            list_of_user_subscriptions = list(dict_of_user_subscriptions.keys())

            #выдает основное меню управления подписками (с 1 кнопкой)
            if call.data == "id_1_back_1":
                text_out = "Управление подписками"
                reply_markup_out = keyboards_buttons.create_inline_kb({"id_1_see_subscriptions": "Смотреть подписки"},1)

            #выдает меню в с имеющимися у пользователя подписками
            elif call.data == "id_1_see_subscriptions" or call.data == "id_1_back_2":
                text_out = "Какая подписка интересует?"
                dict_of_user_subscriptions["id_1_back_1"] = "Назад"
                reply_markup_out = keyboards_buttons.create_inline_kb(dict_of_user_subscriptions, 1)

            #выдает меню со включением или отключением подписки
            elif call.data in list_of_user_subscriptions:
                status_of_subs = queries_to_bd.get_cur_subscription_status(call.data)
                dict_of_btn = {}
                if status_of_subs == '1':
                    text_out = 'Подписка активна, отключить?'
                    dict_of_btn = {'id_1_turn_off_subscribe' + '_' + call.data: 'Да, выключить', 'id_1_turn_cancel_subscribe': 'Отмена'}
                elif status_of_subs == '0':
                    text_out = 'Подписка неактивна, включить?'
                    dict_of_btn = {'id_1_turn_on_subscribe' + '_' + call.data: 'Да, включить', 'id_1_turn_cancel_subscribe': 'Отмена'}
                dict_of_btn["id_1_back_2"] = "Назад"
                reply_markup_out = keyboards_buttons.create_inline_kb(dict_of_btn, 1)

            elif call.data == 'id_1_turn_cancel_subscribe':
                text_out = 'Отменено.Управление подписками:\n/managesubscriptions'

            elif call.data in ['id_1_turn_on_subscribe' + '_' + item for item in list_of_user_subscriptions]:
                subs_id = (call.data).replace("id_1_turn_on_subscribe_id_1_", "")
                queries_to_bd.change_user_subscription_status(subs_id,1)
                text_out = 'Включено. Управление подписками:\n/managesubscriptions'

            elif call.data in ['id_1_turn_off_subscribe' + '_' + item for item in list_of_user_subscriptions]:
                subs_id = (call.data).replace("id_1_turn_off_subscribe_id_1_", "")
                queries_to_bd.change_user_subscription_status(subs_id,0)
                text_out = 'Отключено. Управление подписками:\n/managesubscriptions'

        #Меню с платежками. ID = 2
        elif call.data.startswith("id_2_"):
            text_out = "Ура, транжирим!"
            payments.command_pay(call.message, bot, call.data)

        #Меню с музыкой. ID = 3
        elif call.data.startswith("id_3_"):

            if call.data.startswith("id_3_mus_back_one_"):
                text_out = "Выбери символ (букву или цифру), с которой начинается название исполняющей группы"
                reply_markup_out = keyboards_buttons.music_alphabet()

            elif call.data.startswith("id_3_mus_abc_") or call.data.startswith("id_3_mus_back_two_"):
                text_out = "Выбери исполняющую группу"
                call_data = ''
                if call.data.startswith("id_3_mus_abc_"):
                    call_data = call.data
                else:
                    call_data = (call.data).replace('id_3_mus_back_two_','')
                    call_data = queries_to_bd.get_reverse_performer(call_data)
                reply_markup_out = keyboards_buttons.music_group_list(call_data)

            elif call.data.startswith("id_3_mus_per_") or call.data.startswith("id_3_mus_back_three_"):
                text_out = "Выбери альбом"
                call_data = ''
                if call.data.startswith("id_3_mus_per_"):
                    call_data = call.data
                else:
                    call_data = (call.data).replace('id_3_mus_back_three_','')
                    call_data = queries_to_bd.get_reverse_album(call_data)
                reply_markup_out = keyboards_buttons.albums_of_group_list(call_data)

            elif call.data.startswith("id_3_mus_alb_"):
                text_out = "Выбери песню"
                reply_markup_out = keyboards_buttons.songs_of_album_list(call.data)

            elif call.data.startswith("id_3_mus_son_"):
                full_song_path = queries_to_bd.get_song_path(call.data)
                cur_send_mode = 'default_mode'
                file_size = (os.stat(full_song_path)).st_size / (1024 * 1024)
                if file_size < 50:
                    text_out = "Держи"
                    cur_type_data = 'audio'
                    result_out = full_song_path
                    audio_data = result_out, None
                    send_audio_thread = threading.Thread(target=sending.send_msg(bot       = bot,
                                                                                send_mode  = cur_send_mode,
                                                                                chat_id    = chat_id_out,
                                                                                type_data  = cur_type_data,
                                                                                audio_data = audio_data))
                    send_audio_thread.start()
                else:
                    text_out = "Соре, файл весит больше 50 мб, телега не позволяет ботам отправлять такие файлы."

        #elif call.data == "save_shinobu":
        #    text_out = "сохронил"

        #Меню с напоминалками. ID = 4
        elif call.data.startswith("id_4_"):

            if call.data == "id_4_notification_cur":
                text_out = "Текущие напоминалки"
                reply_markup_out = keyboards_buttons.get_kb_user_notifications(chat_id_out)

            #меню просмотра определенной напоминалки
            elif call.data.startswith("id_4_notif_id_"):
                notification_id = (call.data).replace("id_4_notif_id_", "")
                text_out = queries_to_bd.get_data_by_not_id(notification_id)
                reply_markup_out = keyboards_buttons.get_kb_change_notification(notification_id)

            #меню редактирования
            elif call.data.startswith("id_4_edit_"):

                value_of_edit = (call.data).replace("id_4_edit_", "")

                if value_of_edit.startswith("name_"):
                    notif_id = (call.data).replace("id_4_edit_name_", "")
                    text_out = "Как назовём?"
                    reply_markup_out = keyboards_buttons.create_inline_kb({"id_4_notif_id_" + str(notif_id) :"Назад"}, 1)

                #elif value_of_edit.startswith("act_"):

                #elif value_of_edit.startswith("repeat_flg_"):

                #elif value_of_edit.startswith("repeat_intv_"):

                #elif value_of_edit.startswith("year_"):

                #elif value_of_edit.startswith("month_"):

                #elif value_of_edit.startswith("day_"):

                #elif value_of_edit.startswith("hour_"):

                #elif value_of_edit.startswith("min_"):









            #первое меню новой напоминалки
            if call.data == "id_4_notification_new":
                text_out = "Что напомнить? (пиши в чат)"
                reply_markup_out = keyboards_buttons.create_inline_kb({"id_4_not_back_1":"Назад"}, 1)



        #выход из основного меню напоминалок
        elif call.data == "notification_cancel":
            text_out = "Отменено"

        #возвращение в основное меню напоминалок
        elif call.data == "not_back_1":
            text_out = "Напоминалки"
            reply_markup_out = keyboards_buttons.notif_common(chat_id_out)

        #возврат в название создаваемой напоминалки
        elif call.data == "not_back_2":
            text_out = "Что напомнить? (пиши в чат)"
            reply_markup_out = keyboards_buttons.create_inline_kb({"not_back_1":"Назад"}, 1)

        #возврат к году создаваемой напоминалки
        elif call.data == "not_back_3":
            text_out = "В каком году?"
            reply_markup_out = keyboards_buttons.notif_year()

        #возврат к месяцу создаваемой напоминалки
        elif call.data == "not_back_4":
            year = queries_to_bd.get_year_of_edit_not(chat_id_out)
            text_out = "В каком месяце?"
            reply_markup_out = keyboards_buttons.notif_month(year)

        #возврат к дню создаваемой напоминалки
        elif call.data == "not_back_5":
            month = queries_to_bd.get_month_of_edit_not(chat_id_out)
            text_out = "В какой день?"
            reply_markup_out = keyboards_buttons.notif_day(month,chat_id_out)

        #возврат к часу создаваемой напоминалки
        elif call.data == "not_back_6":
            day = queries_to_bd.get_day_of_edit_not(chat_id_out)
            text_out = "В котором часу?"
            reply_markup_out = keyboards_buttons.notif_hour(day,chat_id_out)

        #возврат к минутам создаваемой напоминалки
        elif call.data == "not_back_7":
            hour = queries_to_bd.get_hour_of_edit_not(chat_id_out)
            text_out = "В какую минуту?"
            reply_markup_out = keyboards_buttons.notif_minute(hour,chat_id_out)

        #возврат периодичности повторения создаваемой напоминалки
        elif call.data == "not_back_8":
            text_out = "Повторять нужно?"
            reply_markup_out = keyboards_buttons.notif_repeat()

        #меню выбора месяца напоминалки
        elif call.data.startswith("not_year_"):
            year = (call.data).replace("not_year_", "")
            queries_to_bd.update_notification(chat_id = chat_id_out, year_num = year)
            text_out = "В каком месяце?"
            reply_markup_out = keyboards_buttons.notif_month(year)

        #меню выбора дня напоминалки
        elif call.data.startswith("not_month_"):
            month = (call.data).replace("not_month_", "")
            queries_to_bd.update_notification(chat_id = chat_id_out, month_num = month)
            text_out = "В какой день?"
            reply_markup_out = keyboards_buttons.notif_day(month, chat_id_out)

        #меню выбора часа напоминалки
        elif call.data.startswith("not_day_"):
            day = (call.data).replace("not_day_", "")
            queries_to_bd.update_notification(chat_id = chat_id_out, day_num = day)
            text_out = "В котором часу?"
            reply_markup_out = keyboards_buttons.notif_hour(day, chat_id_out)

        #меню выбора минуты напоминалки
        elif call.data.startswith("not_hour_"):
            hour = (call.data).replace("not_hour_", "")
            queries_to_bd.update_notification(chat_id = chat_id_out, hour_num = hour)
            text_out = "В какую минуту?"
            reply_markup_out = keyboards_buttons.notif_minute(hour, chat_id_out)

        #меню выбора интервала повторения напоминалки
        elif call.data.startswith("not_minute_"):
            minute = (call.data).replace("not_minute_", "")
            queries_to_bd.update_notification(chat_id = chat_id_out, minute_num = minute)
            text_out = "Повторять нужно?"
            reply_markup_out = keyboards_buttons.notif_repeat()

        #меню подтверждения информации по напоминалке
        elif call.data.startswith("not_repeat_"):
            cur_repeat_value = (call.data).replace("not_repeat_", "")
            if cur_repeat_value == "none":
                queries_to_bd.update_notification(chat_id = chat_id_out, repeat_flg = 0)
            else:
                queries_to_bd.update_notification(chat_id = chat_id_out, repeat_flg = 1, repeat_value = cur_repeat_value)
            text_out = queries_to_bd.check_correct_not(chat_id_out)
            #после получения сгенерированной строки в бд, заменяем символ доллара на новую строку, чтобы нормально отображалось в сообщении
            text_out = text_out.replace("$", "\n")
            reply_markup_out = keyboards_buttons.create_inline_kb({"notif_complete": "Да, все верно","not_back_8":"Назад"}, 1)

       #последнее меню создаваемой напоминалки
        elif call.data == "notif_complete":
            queries_to_bd.update_notification(chat_id = chat_id_out,  activity_flg = '1')
            text_out = "Я все запомнил. Я все напомню."




        else:
            text_out = "Нажата какая-то кнопка"

        #отправляем и сохраняем
        edit_msg_data_out = (chat_id_out, message_id_out, text_out, reply_markup_out, btn_name_out)
        sending.send_msg(bot, 'editing_msg', edit_msg_data = edit_msg_data_out)

    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")