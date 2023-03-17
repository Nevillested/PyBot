import queries_to_bd
import my_cfg

#метод отправки сообщений с различными типами данных
def send_msg(resending_flg, cur_message, bot, chat_id, content_type_out, result_out, reply_out, parse_mode_out, caption_out, poll_answer_desc_out, poll_options_out, poll_correct_option_id_out, poll_type_out):

    #если флаг отправки сообщения другому пользователю через бота равен 0: (от пользователя админу или от админа пользователю)
    if resending_flg == 0:
        if content_type_out == "text":
            bot.send_message(chat_id, result_out, parse_mode = parse_mode_out, reply_markup = reply_out)

        elif content_type_out == "sticker":
            bot.send_sticker(chat_id, sticker = open(result_out, "rb"), reply_markup = reply_out)

        elif content_type_out == "photo":
            bot.send_photo(chat_id, photo = open(result_out, 'rb'), caption = caption_out, parse_mode = parse_mode_out, reply_markup = reply_out)

        elif content_type_out == "audio":
            bot.send_audio(chat_id=chat_id, audio=open(result_out, 'rb'), reply_markup = reply_out)

        elif content_type_out == "poll":
            result_out = result_out[0]
            poll_options_out.pop(0)
            bot.send_poll(chat_id, 'Кандзи: ' + poll_answer_desc_out, options = poll_options_out, correct_option_id  = poll_correct_option_id_out, type = poll_type_out, reply_markup = reply_out)
        elif content_type_out == "document":
            bot.send_document(chat_id, document = open(result_out, 'rb'), reply_markup = reply_out)
            
    #если флаг отправки сообщения другому пользователю через бота равен 1: (от пользователя админу или от админа пользователю)
    elif resending_flg == 1:
        chat_id_to_send = None
        content_type_out = cur_message.content_type
        
        if content_type_out == "text":
            result_out = cur_message.text

        #получаем id чата, куда отправляем сообщение
        if cur_message.chat.id == my_cfg.id_owner:
            chat_id_to_send = queries_to_bd.get_prelast_user_msg(cur_message.chat.id)
        else:
            chat_id_to_send = my_cfg.id_owner
            
        bot.send_message(chat_id_to_send, 'Пришло сообщение от @' + cur_message.from_user.username +':') 

        if cur_message.content_type == "text":
            bot.send_message(chat_id_to_send, cur_message.text)

        elif cur_message.content_type == "sticker":
            bot.send_sticker(chat_id_to_send, cur_message.sticker.file_id)

        elif cur_message.content_type == "photo":
            file = cur_message.photo[-1]
            file = file.file_id
            bot.send_photo(chat_id_to_send, photo = file)

        elif cur_message.content_type == "voice":
            bot.send_voice(chat_id_to_send, cur_message.voice.file_id)

        elif cur_message.content_type == "video":
            bot.send_video(chat_id_to_send, cur_message.video.file_id)

        elif cur_message.content_type == "video_note":
            bot.send_video_note(chat_id_to_send, cur_message.video_note.file_id)

        elif cur_message.content_type == "document":
            bot.send_document(chat_id_to_send, cur_message.document.file_id)

        else:
            bot.send_message(cur_message.chat.id, 'Не удалось отправить ваше сообщение. Свяжитесь с админом и расскажите об ошибке плз\nТип сообщения: '+str(cur_message.content_type)) 
            
        bot.send_message(cur_message.chat.id, 'Отправлено') 

    return content_type_out, result_out