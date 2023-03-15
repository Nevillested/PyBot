def call_processed(bot,call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "inline_kb_1bt":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата первая кнопка!")
        elif call.data == "inline_kb_2bt":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата вторая кнопка!")
        elif call.data == "inline_kb_3bt":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата третья кнопка!")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нажата какая-то кнопка")
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")