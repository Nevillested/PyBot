import keyboards_buttons
import queries_to_bd
import payments
import sending
import telebot
import os
import music_processing
import threading

#def payments_buttons(call_data):

#def music_buttons(call_data):

#def subscriptions_buttons():

def call_processed(bot, call):
    # Если сообщение из чата с ботом
    if call.message:

        dict_of_user_subscriptions = queries_to_bd.get_subscriptions_user(call.message.chat.id)
        list_of_user_subscriptions = list(dict_of_user_subscriptions.keys())

        chat_id_out      = call.message.chat.id
        message_id_out   = call.message.message_id
        text_out         = None
        reply_markup_out = None
        btn_name_out     = call.data

        if call.data == "subs_back_1":
            text_out = "Управление подписками"
            reply_markup_out = keyboards_buttons.create_inline_kb({"see_subscriptions": "Смотреть подписки"})

        elif call.data == "see_subscriptions" or call.data == "subs_back_2":
            text_out = "Какая подписка интересует?"
            dict_of_user_subscriptions["subs_back_1"] = "Назад"
            reply_markup_out = keyboards_buttons.create_inline_kb(dict_of_user_subscriptions)

        elif call.data in list_of_user_subscriptions:
            status_of_subs = queries_to_bd.get_cur_subscription_status(call.data)
            dict_of_btn = {}
            if status_of_subs == '1':
                text_out = 'Подписка активна, отключить?'
                dict_of_btn = {'turn_off_subscribe' + '_' + call.data: 'Да, выключить', 'turn_cancel_subscribe': 'Отмена'}
            elif status_of_subs == '0':
                text_out = 'Подписка неактивна, включить?'
                dict_of_btn = {'turn_on_subscribe' + '_' + call.data: 'Да, включить', 'turn_cancel_subscribe': 'Отмена'}
            dict_of_btn["subs_back_2"] = "Назад"
            reply_markup_out = keyboards_buttons.create_inline_kb(dict_of_btn)

        elif call.data == 'turn_cancel_subscribe':
            text_out = 'Отменено.Управление подписками:\n/managesubscriptions'

        elif call.data in ['turn_on_subscribe' + '_' + item for item in list_of_user_subscriptions]:
            subs_id = (call.data).replace("turn_on_subscribe_", "")
            queries_to_bd.change_user_subscription_status(subs_id,1)
            text_out = 'Включено. Управление подписками:\n/managesubscriptions'

        elif call.data in ['turn_off_subscribe' + '_' + item for item in list_of_user_subscriptions]:
            subs_id = (call.data).replace("turn_off_subscribe_", "")
            queries_to_bd.change_user_subscription_status(subs_id,0)
            text_out = 'Отключено. Управление подписками:\n/managesubscriptions'

        elif call.data.__contains__("payment"):
            text_out = "Ура, транжирим!"
            payments.command_pay(call.message, bot, call.data)

        elif call.data.startswith("mus_back_one_"):
            text_out = "Выбери символ (букву или цифру), с которой начинается название исполняющей группы"
            reply_markup_out = keyboards_buttons.music_alphabet()

        elif call.data.startswith("mus_abc_") or call.data.startswith("mus_back_two_"):
            text_out = "Выбери исполняющую группу"
            call_data = ''
            if call.data.startswith("mus_abc_"):
                call_data = call.data
            else:
                call_data = (call.data).replace('mus_back_two_','')
                call_data = queries_to_bd.get_reverse_performer(call_data)
            reply_markup_out = keyboards_buttons.music_group_list(call_data)

        elif call.data.startswith("mus_per_") or call.data.startswith("mus_back_three_"):
            text_out = "Выбери альбом"
            call_data = ''
            if call.data.startswith("mus_per_"):
                call_data = call.data
            else:
                call_data = (call.data).replace('mus_back_three_','')
                call_data = queries_to_bd.get_reverse_album(call_data)
            reply_markup_out = keyboards_buttons.albums_of_group_list(call_data)

        elif call.data.startswith("mus_alb_"):
            text_out = "Выбери песню"
            reply_markup_out = keyboards_buttons.songs_of_album_list(call.data)

        elif call.data.startswith("mus_son_"):
            full_song_path = queries_to_bd.get_song_path(call.data)
            cur_send_mode = 'default_mode'
            file_size = (os.stat(full_song_path)).st_size / (1024 * 1024)
            if file_size < 50:
                text_out = "Держи"
                cur_type_data = 'audio'
                result_out = full_song_path
                audio_data = result_out, None
                send_audio_thread = threading.Thread(target=sending.send_msg(bot             = bot,
                                                                             send_mode       = cur_send_mode,
                                                                             chat_id_out     = chat_id_out,
                                                                             type_data_out   = cur_type_data,
                                                                             audio_data_out  = audio_data))
                send_audio_thread.start()
            else:
                text_out = "Соре, файл весит больше 50 мб, телега не позволяет ботам отправлять такие файлы."

        elif call.data == "save_shinobu" or call.data == "subs_back_2":
            text_out = "сохронил"

        else:
            text_out = "Нажата какая-то кнопка"

        #отправляем и сохраняем
        edit_msg_data = (chat_id_out, message_id_out, text_out, reply_markup_out, btn_name_out)
        sending.send_msg(bot, 'editing_msg', edit_msg_data_out = edit_msg_data)

    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")