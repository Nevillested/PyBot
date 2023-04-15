import keyboards_buttons
import queries_to_bd

def call_processed(bot,call):
    # Если сообщение из чата с ботом
    if call.message:
        dict_of_user_subscriptions = queries_to_bd.get_subscriptions_user(call.message.chat.id)

        list_of_user_subscriptions = []
        for key, value in dict_of_user_subscriptions.items():
            list_of_user_subscriptions.append(key)

        list_of_user_subscriptions_turn_off = []
        for item in list_of_user_subscriptions:
            list_of_user_subscriptions_turn_off.append('turn_off_subscribe' + '_' + item)

        list_of_user_subscriptions_turn_on = []
        for item in list_of_user_subscriptions:
            list_of_user_subscriptions_turn_on.append('turn_on_subscribe' + '_' + item)

        if call.data == "inline_kb_1bt":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата первая кнопка!")
        elif call.data == "inline_kb_2bt":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата вторая кнопка!")
        elif call.data == "inline_kb_3bt":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата третья кнопка!")
        elif call.data == "manage_subscriptions":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какая подписка интересует?", reply_markup = keyboards_buttons.create_inline_kb(dict_of_user_subscriptions))
        elif call.data in list_of_user_subscriptions:
            status_of_subs = queries_to_bd.get_cur_subscription_status(call.data)
            text_result_out = ''
            dict_of_btn = {}
            if status_of_subs == '1':
                text_result_out = 'Подписка активна, отключить?'
                dict_of_btn = {'turn_off_subscribe' + '_' + call.data: 'Да, выключить', 'turn_cancel_subscribe': 'Отмена'}
            elif status_of_subs == '0':
                text_result_out = 'Подписка неактивна, включить?'
                dict_of_btn = {'turn_on_subscribe' + '_' + call.data: 'Да, включить', 'turn_cancel_subscribe': 'Отмена'}
            else:
                text_result_out = 'С подпиской что-то непонятное..'
            reply_markup_out = keyboards_buttons.create_inline_kb(dict_of_btn)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text_result_out, reply_markup = reply_markup_out)
        elif call.data == 'turn_cancel_subscribe':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Отменено.Управление подписками:\n/manage_subscriptions')
        elif call.data in list_of_user_subscriptions_turn_on:
            subs_id = (call.data).replace("turn_on_subscribe_", "")
            queries_to_bd.change_user_subscription_status(subs_id,1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Включено. Управление подписками:\n/manage_subscriptions')
        elif call.data in list_of_user_subscriptions_turn_off:
            subs_id = (call.data).replace("turn_off_subscribe_", "")
            queries_to_bd.change_user_subscription_status(subs_id,0)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Отключено. Управление подписками:\n/manage_subscriptions')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата какая-то кнопка")
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")