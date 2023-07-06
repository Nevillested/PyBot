import queries_to_bd
from telebot.types import LabeledPrice
import my_cfg

#метод отправки сообщений с различными режимами
def send_msg(bot, send_mode, cur_msg=None, chat_id_out=None, msg_id_out=None, type_data_out=None, text_data_out=None, poll_data_out=None, photo_data_out=None, sticker_data_out=None, audio_data_out=None, doc_data_out=None, inline_data_out=None, payment_data_out=None, edit_msg_data_out=None):
    
    #простой режим отправки сообщений
    result_out = ''
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
            has_spoiler_out = photo_data_out[4]
            bot.send_photo(chat_id_out, photo = open(result_out, 'rb'), reply_markup = reply_markup_out, caption = caption_out, parse_mode = parse_mode_out, has_spoiler = has_spoiler_out)

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
        queries_to_bd.insert_user_story_out(type_data_out, result_out, chat_id_out)
            
            
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
            status = 'Не удалось отправить ваше сообщение. Свяжитесь с админом напрямую @g1ts0 и расскажите об ошибке плз\nТип сообщения: '+str(content_type_out)
        
        #уведомляет отправляющего пользователя о статусе сообщения
        bot.send_message(from_send.chat.id, status) 

        #сохраняет данные, теоретически улетевшие пользователю
        queries_to_bd.insert_user_story_out(content_type_out, status, from_send.chat.id)
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
    elif send_mode == 'payment_mode':

        chat_id_out = payment_data_out[0]
        title_out = payment_data_out[1]
        description_out = payment_data_out[2]
        invoice_payload_out = payment_data_out[3]
        provider_token_out = payment_data_out[4]
        currency_out = payment_data_out[5]
        prices_out = [LabeledPrice(label='Выворачивай карманы, к оплате: ', amount=payment_data_out[6])]
        photo_url_out = payment_data_out[7]
        photo_height_out = payment_data_out[8]
        photo_width_out = payment_data_out[9]
        photo_size_out = payment_data_out[10]
        is_flexible_out = payment_data_out[11]
        start_parameter_out = payment_data_out[12]
        max_tip_amount_out = payment_data_out[13]
        suggested_tip_amounts_out = payment_data_out[14]
        provider_data_out = '''{
  "receipt": {
    "customer": {
        "email": "ararararagi.payments@gmail.com"
    },     
    "items": [
      {
             "description": "'''+description_out+'''",
             "quantity": "1",
             "amount": {
                 "value": "'''+str(payment_data_out[6]/100)+'''",
                 "currency": "'''+currency_out+'''"
             },
             "vat_code": "1"
        }
    ]
  }
}'''

        #отправляет данные для платежа
        bot.send_invoice(chat_id               = chat_id_out,
                         title                 = title_out,
                         description           = description_out,
                         invoice_payload       = invoice_payload_out,
                         provider_token        = provider_token_out,
                         currency              = currency_out,
                         prices                = prices_out,
                         photo_url             = photo_url_out,
                         photo_height          = photo_height_out,
                         photo_width           = photo_width_out,
                         photo_size            = photo_size_out,
                         is_flexible           = is_flexible_out,
                         start_parameter       = start_parameter_out,
                         max_tip_amount        = max_tip_amount_out,
                         suggested_tip_amounts = suggested_tip_amounts_out,
                         need_email            = True,
                         send_email_to_provider= True,
                         provider_data         = provider_data_out
                        )
        
        #сохраняет данные для платежа
        queries_to_bd.save_data_for_payment(payment_data_out)
    
    #режим редактирования сообщений
    elif send_mode == 'editing_msg':
        
        chat_id_out      = edit_msg_data_out[0]
        message_id_out   = edit_msg_data_out[1]
        text_out         = edit_msg_data_out[2]
        reply_markup_out = edit_msg_data_out[3]
        btn_name_out     = edit_msg_data_out[4]
        
        bot.edit_message_text(chat_id=chat_id_out, message_id=message_id_out, text=text_out, reply_markup = reply_markup_out)

        #Сохраняет в бд
        edited_message = (text_out + ': ' + btn_name_out, chat_id_out, message_id_out)
        queries_to_bd.insert_edited_msg_by_bot(edited_message)