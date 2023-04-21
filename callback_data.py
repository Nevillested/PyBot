import keyboards_buttons
import queries_to_bd
import payments
import sending

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
            reply_markup_out = keyboards_buttons.create_inline_kb({"manage_subscriptions": "Смотреть подписки"})

        elif call.data == "manage_subscriptions" or call.data == "subs_back_2":
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

        else:
            text_out = "Нажата какая-то кнопка"

        #отправляем и сохраняем
        edit_msg_data = (chat_id_out, message_id_out, text_out, reply_markup_out, btn_name_out)
        sending.send_msg(bot, 'editing_msg', edit_msg_data_out = edit_msg_data)

    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")