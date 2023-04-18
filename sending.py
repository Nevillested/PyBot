import queries_to_bd
import my_cfg

#метод отправки сообщений с различными типами данных


def send_msg(bot, send_mode, cur_msg=None, chat_id_out=None, msg_id_out=None, type_data_out=None, text_data_out=None, poll_data_out=None, photo_data_out=None, sticker_data_out=None, audio_data_out=None, doc_data_out=None, inline_data_out=None, flg_counter_msg=1):
    
    #простой режим отправки сообщений
    if send_mode == 'default_mode':
        if type_data_out == "text":
            result_out =  text_data_out[0]
            reply_markup_out = text_data_out[1]
            parse_mode_out =  text_data_out[2]
            reply_message_out =  text_data_out[3]
            bot.send_message(chat_id_out, result_out, reply_markup = reply_markup_out, parse_mode = parse_mode_out, reply_to_message_id = reply_message_out)

        elif type_data_out == "sticker":
            result_out = sticker_data_out[0]
            reply_markup_out = sticker_data_out[1]
            bot.send_sticker(chat_id_out, sticker = open(result_out, "rb"), reply_markup = reply_markup_out)

        elif type_data_out == "photo":
            result_out = photo_data_out[0]
            reply_markup_out = photo_data_out[1]
            caption_out = photo_data_out[2]
            parse_mode_out = photo_data_out[3]
            bot.send_photo(chat_id_out, photo = open(result_out, 'rb'), reply_markup = reply_markup_out, caption = caption_out, parse_mode = parse_mode_out)

        elif type_data_out == "audio":
            result_out = audio_data_out[0]
            reply_markup_out = audio_data_out[1]
            bot.send_audio(chat_id_out, audio=open(result_out, 'rb'), reply_markup = reply_markup_out)

        elif type_data_out == "poll":
            result_out = (poll_data_out[0]).pop(0)
            poll_options_out = poll_data_out[0]
            type_out = poll_data_out[1]
            correct_option_id_out = poll_data_out[2]
            result = 'Кандзи: ' + poll_data_out[3]
            reply_markup_out = poll_data_out[4]
            bot.send_poll(chat_id_out, result, options = poll_options_out, correct_option_id  = correct_option_id_out, type = type_out, reply_markup = reply_markup_out)

        elif type_data_out == "document":
            result_out = doc_data_out[0]
            reply_out = doc_data_out[1]
            bot.send_document(chat_id_out, document = open(result_out, 'rb'), reply_markup = reply_out)

        #сохраняет улетевшие данные пользователю
        queries_to_bd.insert_user_story_out(type_data_out, result_out, chat_id_out, msg_id_out, flg_counter_msg)
            
            
    #режим отправки соообщений другому пользователю
    elif send_mode == 'resending_mode':

        type_data_out = cur_msg.content_type
        content_type_out = cur_msg.content_type
        from_send = cur_msg
        chat_id_to_send = None
        result = None
        
        #если сообщение прилетело не от админа, то оно направляется админу. 
        if cur_msg.chat.id != my_cfg.id_owner:
            chat_id_to_send = my_cfg.id_owner
        #В противном случае это сообщение от админа и id чата, куда должно уйти сообщение находится в предпоследнем сообщении от админа боту
        else:
            chat_id_to_send = queries_to_bd.get_prelast_user_msg(my_cfg.id_owner)

        #Отправляем предварительное уведомление
        bot.send_message(chat_id_to_send, 'Пришло сообщение от @' + from_send.from_user.username +':') 
        
        #раскейсовка и отправка сообщений, который отправляет юзер
        status = 'Отправлено'
        if content_type_out == "text":
            result = from_send.text
            bot.send_message(chat_id_to_send, result)

        elif content_type_out == "sticker":
            result = from_send.sticker.file_id
            bot.send_sticker(chat_id_to_send, result)

        elif content_type_out == "photo":
            file = from_send.photo[-1]
            result = file.file_id
            bot.send_photo(chat_id_to_send, photo = result)

        elif content_type_out == "voice":
            result = from_send.voice.file_id
            bot.send_voice(chat_id_to_send, result)

        elif content_type_out == "video":
            result = from_send.video.file_id
            bot.send_video(chat_id_to_send, result)

        elif content_type_out == "video_note":
            result = from_send.video_note.file_id
            bot.send_video_note(chat_id_to_send, result)

        elif content_type_out == "document":
            result = from_send.document.file_id
            bot.send_document(chat_id_to_send, result)

        else:
            status = 'Не удалось отправить ваше сообщение. Свяжитесь с админом и расскажите об ошибке плз\nТип сообщения: '+str(content_type_out)
        
        #уведомляет отправляющего пользователя о статусе сообщения
        bot.send_message(from_send.chat.id, status) 

        #сохраняет данные, теоретически улетевшие пользователю
        queries_to_bd.save_resending_data(from_send.chat.id, chat_id_to_send, content_type_out, result)
    
    #инлайн режим
    elif send_mode == 'inline_mode':

        query_data_out = inline_data_out[0]
        results_out = inline_data_out[1]
        cache_time_out = inline_data_out[2]
        query_id_out = query_data_out.id
        query_from = query_data_out.from_user.id
        query_text = query_data_out.query

        #отправляет результаты запроса
        bot.answer_inline_query(query_id_out, results_out, cache_time = cache_time_out)
        
        #сохраняет запрос
        queries_to_bd.save_inline_data(query_from, query_text)
        
    
    #платежный режим
    #elif send_mode == 'payment_mode':