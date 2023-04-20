import common_methods
import my_cfg
import psycopg2

conn = psycopg2.connect(my_cfg.pg_sql_con_string)
conn.autocommit = True
cur = conn.cursor()

#проверяет пользователя в бд, если есть-обновляет данные, если нет-добавляет данные
def check_user(data_from_message):

    chat_id = str(data_from_message.chat.id)
    first_name = data_from_message.from_user.first_name or ''
    username = data_from_message.from_user.username or ''
    last_name = data_from_message.from_user.last_name or ''
    language_code = data_from_message.from_user.language_code or ''
    is_premium = str(data_from_message.from_user.is_premium) or ''
    is_bot = str(data_from_message.from_user.is_bot) or ''

    cur.execute("""
    MERGE INTO users u
    USING (select """ + chat_id + """        as chat_id,
                 '""" + first_name + """'    as first_name,
                 '""" + username + """'      as username,
                 '""" + last_name + """'     as last_name,
                 '""" + language_code + """' as language_code,
                 '""" + is_premium + """'    as is_premium,
                 '""" + is_bot + """'        as is_bot) s
    ON u.chat_id = s.chat_id
    WHEN NOT MATCHED THEN
      INSERT (chat_id,first_name,username,last_name,language_code,is_premium,is_bot)
      VALUES (s.chat_id,s.first_name,s.username,s.last_name,s.language_code,s.is_premium,s.is_bot)
    WHEN MATCHED THEN
      UPDATE SET first_name    = s.first_name,
                 username      = s.username,
                 last_name     = s.last_name,
                 language_code = s.language_code,
                 is_premium    = s.is_premium,
                 is_bot        = s.is_bot;
    """)

#сохраняет прилетевшие данные в переписке с пользователем и ботом
def insert_user_story_in(data_from_message):

    chat_id = str(data_from_message.chat.id)
    message_id = str(data_from_message.message_id)
    username = data_from_message.from_user.username  or ''
    content_type = str(data_from_message.content_type)  or ''
    data_in = ''

    if (data_from_message.content_type =='text'):
        data_in = data_from_message.text
    elif (data_from_message.content_type =='location'):
        data_in = str(data_from_message.location.latitude)+';'+str(data_from_message.location.longitude)

    cur.execute("""
    insert into income ( chat_id,
                             message_id,
                             MESSAGE_TYPE,
                             MESSAGE_DATA
                           )
    values (  """ + chat_id + """,
              """ + message_id + """,
             '""" + content_type + """',
             '""" + data_in + """'
           );
    """)

#сохраняет улетевшие данные пользователю в переписке с ботом
def insert_user_story_out(content_type_out, clob_data_out, chat_id, message_id):

    chat_id = str(chat_id) or ''
    message_id =str(message_id) or ''
    content_type = str(content_type_out) or ''
    data_in = (str(clob_data_out)).replace("'","''") or ''

    cur.execute("""
    insert into outcome ( chat_id,
                          message_id,
                          message_type,
                          message_data
                        )
    select """ + chat_id + """,
           max(a.message_id) + 1,
           '""" + content_type + """',
           '""" + data_in + """'
    from (select message_id
            from income
           union all
          select message_id
            from outcome
         ) as a
    """)

#добавляет новую версию сообщения отредактированного пользователем
def insert_edited_msg_by_user(data_from_message):

    msg_text = str(data_from_message[0])
    chat_id = str(data_from_message[1])
    message_id = str(data_from_message[2])

    cur.execute("""
    insert into income( dt_ins
                          , dt_upd
                          , chat_id
                          , message_id
                          , MESSAGE_TYPE
                          , MESSAGE_DATA
                          , MESSAGE_VERSION)
                     select a.dt_ins
                          , current_timestamp
                          , a.chat_id
                          , a.message_id
                          , a.MESSAGE_TYPE
                          , '""" + msg_text + """'
                          , a.MESSAGE_VERSION + 1
                       from (select *
                               from income
                              where chat_id = """ + chat_id + """
                                and message_id = """ + message_id + """
                               order by MESSAGE_VERSION desc
                               limit 1) a
    """)

#добавляет новую версию сообщения отредактированного ботом
def insert_edited_msg_by_bot(data_from_message):

    msg_text = str(data_from_message[0])
    chat_id = str(data_from_message[1])
    message_id = str(data_from_message[2])

    cur.execute("""
    insert into outcome( dt_ins
                          , dt_upd
                          , chat_id
                          , message_id
                          , MESSAGE_TYPE
                          , MESSAGE_DATA
                          , MESSAGE_VERSION)
                     select a.dt_ins
                          , current_timestamp
                          , a.chat_id
                          , a.message_id
                          , a.MESSAGE_TYPE
                          , '""" + msg_text + """'
                          , a.MESSAGE_VERSION + 1
                       from (select *
                               from outcome
                              where chat_id = """ + chat_id + """
                                and message_id = """ + message_id + """
                               order by MESSAGE_VERSION desc
                               limit 1) a
    """)

#выдает последнюю версию отредактированного сообщения пользователем
def get_last_ver_msg(data_from_message):

    chat_id = str(data_from_message[0])
    message_id = str(data_from_message[1])

    cur.execute("""
    select a.MESSAGE_DATA
      from ( select MESSAGE_DATA,
                    ROW_NUMBER () OVER (ORDER BY MESSAGE_VERSION desc) as rn
               from income
              where chat_id = """ + chat_id + """
                and message_id = """ + message_id + """
              order by MESSAGE_VERSION desc
           ) as a
     where a.rn = 2
    """)

    result_tuple = cur.fetchone()

    result_string = common_methods.convertTuple(result_tuple)

    return result_string

#сохраняет данные при переписке между пользователями
def save_resending_data(id_from, id_to, data_type, data_send):

    cur.execute("""
    insert into resending_data (send_from, send_to, type_data, send_data)
    values (""" + str(id_from) + """, """ + str(id_to) + """, '""" + str(data_type) + """', '""" + str(data_send) + """')
    """)

#сохраняет данные inline mode
def save_inline_data(id_from, text_query):

    cur.execute("""
    insert into inline_mode_data (query_from, query_text)
    values (""" + str(id_from) + """, '""" + str(text_query) + """')
    """)

#получает последнее свое отправленное сообщение
def get_last_bot_msg(chat_id):

    cur.execute("""
    select a.MESSAGE_DATA
      from ( select MESSAGE_DATA
                  , row_number() OVER(ORDER BY dt_ins DESC) rn
               from outcome a
              where chat_id = """ + str(chat_id) + """
              order by dt_ins desc) as a
     where a.rn = 1""")
    result_tuple = cur.fetchone()
    result_string = ''

    if result_tuple != None:
        for item in result_tuple:
            result_string = result_string + str(item)

    return result_string

#получает предпоследнее сообщение пользователя
def get_prelast_user_msg(chat_id):

    cur.execute("""
    select a.MESSAGE_DATA
      from (select MESSAGE_DATA,
                   ROW_NUMBER () OVER (ORDER BY dt_ins desc) as rn
              from income a
             where chat_id = """ + str(chat_id) + """
           ) as a
     where a.rn = 2
    """)
    result_tuple = cur.fetchone()

    result_string = ''

    if result_tuple != None:
        result_string = common_methods.convertTuple(result_tuple)

    return result_string

#создает строку для наполнения данных для шифрования/дешифрования
def create_session_cezar(data_from_message):

    chat_id = str(data_from_message.chat.id) or ''
    method = str(data_from_message.text.replace("/", "")) or ''

    cur.execute("""
    insert into cezar (chat_id, method)
    values (""" + chat_id + """, '""" + method + """')
    """)

#добавляет язык обработки данных для шифрования/дешифрования
def update_lang_session_cezar(data_from_message):

    chat_id = str(data_from_message.chat.id) or ''
    lang = str(data_from_message.text.lower()) or ''

    cur.execute("""
    UPDATE CEZAR
       SET LANG = '""" + lang + """'
     WHERE CHAT_ID = """ + chat_id + """
       AND ID = (SELECT A.ID
                   FROM (SELECT ID
                           FROM CEZAR
                          WHERE CHAT_ID = """ + chat_id + """
                          ORDER BY ID DESC
                        ) A
                  LIMIT 1
                )
    """)


#добавляет ключ для шифрования/дешифрования
def update_key_session_cezar(data_from_message):

    chat_id = str(data_from_message.chat.id) or ''
    key = str(data_from_message.text) or ''

    cur.execute("""
    UPDATE CEZAR
       SET KEY = '""" + key + """'
     WHERE CHAT_ID = """ + chat_id + """
       AND ID = (SELECT A.ID
                   FROM (SELECT ID
                           FROM CEZAR
                          WHERE CHAT_ID = """ + chat_id + """
                          ORDER BY ID DESC
                        ) A
                  LIMIT 1
                )
    """)

#добавляет текст для шифрования/дешифрования
def update_messaage_in_session_cezar(data_from_message):

    chat_id = str(data_from_message.chat.id) or ''
    messaage_in = str(data_from_message.text) or ''

    cur.execute("""
    UPDATE CEZAR
       SET messaage_in = '""" + messaage_in + """'
     WHERE CHAT_ID = """ + chat_id + """
       AND ID = (SELECT A.ID
                   FROM (SELECT ID
                           FROM CEZAR
                          WHERE CHAT_ID = """ + chat_id + """
                          ORDER BY ID DESC
                        ) A
                  LIMIT 1
                )
    """)

#выдает данные для шифрования
def get_data_cezar(data_from_message):

    chat_id = str(data_from_message.chat.id) or ''

    cur.execute("""
    select lang
         , key
         , method
         , messaage_in
      from cezar
     WHERE CHAT_ID = """ + chat_id + """
       AND ID = (SELECT A.ID
                   FROM (SELECT ID
                           FROM CEZAR
                          WHERE CHAT_ID = """ + chat_id + """
                          ORDER BY ID DESC
                        ) A
                  LIMIT 1
                )
    """)

    result_tuple = cur.fetchone()

    return result_tuple[0],result_tuple[1],result_tuple[2],result_tuple[3]

#получает список пользователей для админки в чаровском виде
def get_users():

    cur.execute("""
    select STRING_AGG('ID чата `' || chat_id ||'`, ник/имя ' || coalesce(case when username is not null then '@'||username end, first_name||' '||last_name), '\n')
    from users""")
    tuple_data = cur.fetchone()

    result = common_methods.convertTuple(tuple_data)
    result = result.replace("_", "\_")
    return result


#получает список пользователей - только айдишники в list для рассылки
def get_users_id():

    list_of_id = []
    cur.execute("""
    select chat_id
    from users
    """)

    rows = cur.fetchall()

    for item in rows:
        buffer = ''
        for char_one in str(item):
            for char_two in ('1234567890-'):
                if char_one == char_two:
                    buffer += char_one
        list_of_id.append(int(buffer))

    return list_of_id

#получает сегодняшний праздник
def get_holiday():

    cur.execute("""
    select text_holiday
    from international_holiday
    where date_trunc('day', date_holiday) = date_trunc('day', now())
    """)

    tuple_data = cur.fetchone()

    result = ''
    if tuple_data != None:
        result = common_methods.convertTuple(tuple_data)
    return result


#создает новую сессию распознавания текста, добавляет язык
def create_session_voice(data_from_message):

    chat_id = str(data_from_message.chat.id) or ''
    lang = str(data_from_message.text) or ''

    cur.execute("""
    insert into voices (chat_id, lang)
    values (""" + chat_id + """, '""" + lang + """')
    """)

#выдает язык распознавания текста
def get_lang_voice(data_from_message):

    cur.execute("""
    select lang
    from voices
    where chat_id = """ + str(data_from_message.chat.id) + """
    order by dt_ins desc
    limit 1
    """)
    tuple_data = cur.fetchone()

    return tuple_data[0]

#сохраняет распознанный текст
def insert_result_recognize_speech(data_from_message, result_recog):

    cur.execute("""
    update voices
       set result_text = """ + result_recog + """
     where id = ( select id
                    from voices
                    where chat_id = """ + str(data_from_message.chat.id) + """
                    order by dt_ins desc
                    limit 1
                )
    """)

#получает анекдот
def get_joke():

    cur.execute("""
    select 'Анекдотов пока нет, соре'
    """)
    tuple_data = cur.fetchone()

    anekdot = common_methods.convertTuple(tuple_data)
    return anekdot

#получает комплимент
def get_compliment():

    cur.execute("""
    select text
    from compliments
    order by random()
    limit 1
    """)
    tuple_data = cur.fetchone()

    compliment = common_methods.convertTuple(tuple_data)
    return compliment

#выдает перевод найденного слова
def get_translate_jp(user_text):

    cur.execute("""
    select coalesce(
                    ( select STRING_AGG ('Без кандзи: '||jap_word_without_kanji||
                                         '\nС Кандзи: '||coalesce(jap_word_with_kanji,'отсутствует')||
                                         '\nПеревод: '||rus_word, '\n\n') res
                        from jap_dict
                       where lower(rus_word) like '%""" + user_text.lower() +"""%'
                    ), 'Мы ничего не нашли'
                   )
    """)

    result_tuple = cur.fetchone()

    result_string = common_methods.convertTuple(result_tuple)

    return result_string

#выдает кандзи
def get_kanji(user_number):

    cur.execute("""
    select STRING_AGG ('Кандзи: '||kanji||
                       '\nЧтения: '||reading||
                       '\nПеревод: '||rus_word, '\n\n') res
      from jap_kanji
     where id <= 10 * """+user_number+"""
       and id > 10 * """+user_number+""" - 10
    """)

    result_tuple = cur.fetchone()

    result_string = common_methods.convertTuple(result_tuple)

    return result_string

#получает последний "номер десятка", полученный от пользователя для квиза по "номеру десятка"
def get_last_num_decade_kanji(chat_id):

    cur.execute("""
    select lag_msg
      from ( select LAG(message_data,1) OVER ( ORDER BY id desc ) lag_msg,
                    message_data,
                    chat_id
               from income
           ) as a
     where lower(a.message_data) = 'по номеру десятка!'
       and a.chat_id = """ + str(chat_id) + """
    """)
    result_tuple = cur.fetchone()

    result_string = ''

    if result_tuple != None:
        result_string = common_methods.convertTuple(result_tuple)
    print(result_string)
    return result_string

#возвращает данные для квиза но номеру десятка
def get_decade_kanji_quiz(num_decade):

    list_of_rows = []

    cur.execute("""with
                     all_vars as (
                       select a.kanji
                            , a.reading
                            , a.rus_word
                            , a.rn
                         from (select a.*
                                    , ROW_NUMBER () OVER (ORDER BY random()) as rn
                                 from jap_kanji a
                                where a.id <= 10 * """+num_decade+"""
                                  and a.id > 10 * """+num_decade+""" -10
                                order by random()
                              ) a
                        where rn <= 4
                       ),
                       rand_true_val as(
                         select *
                           from all_vars
                          where rn = 1
                       )
                       /*берем правильный ответ*/
                       select kanji, 'Чтение: '||reading||'. Перевод: '||rus_word,rn from rand_true_val
                       /*объединяем со всеми, которые имеются*/
                       union all
                       select a.kanji, 'Чтение: '||a.reading||'. Перевод: '||a.rus_word,rn from (select *
                                                                                                 from all_vars
                                                                                                order by random()
                                                                                              ) as a
    """)
    list_of_rows = cur.fetchall()
    return list_of_rows

#возвращает данные для квиза по всем имеющимся кадзи
def get_all_kanji_quiz():
    list_of_rows = []

    cur.execute("""with
                     all_vars as (
                       select a.kanji
                            , a.reading
                            , a.rus_word
                            , a.id
                            , ROW_NUMBER () OVER (ORDER BY random()) as rn
                         from jap_kanji as a order by RANDOM() limit 4
                       )
                       /*берем правильный ответ*/
                       select kanji, 'Чтение: '||reading||'. Перевод: '||rus_word,rn from all_vars where rn = 1
                       /*объединяем со всеми, которые имеются*/
                       union all
                       select a.kanji, 'Чтение: '||a.reading||'. Перевод: '||a.rus_word, rn from (select *
                                                                                                  from all_vars
                                                                                                 order by random()
                                                                                               ) as a
    """)
    list_of_rows = cur.fetchall()
    return list_of_rows

#возвращает словарь с подписками пользователей
def get_subscriptions_user(chat_id):
    list_of_rows = []
    dict_of_subscriptions_user = {}
    cur.execute("""
    select chat_id ||'_' ||id as  btn_id
         , subscription_name
      from subscriptions
     where chat_id = """ + str(chat_id) + """
    """)
    list_of_rows = cur.fetchall()
    for item in list_of_rows:
        dict_of_subscriptions_user[item[0]] = item[1]

    return dict_of_subscriptions_user

#возвращает статус подписки пользователя
def get_cur_subscription_status(id_subscription):
    cur.execute("""
    select a.active_flg
      from (select a.*
                 , a.chat_id ||'_' ||a.id as btn_id
              from subscriptions as a
           ) as a
     where a.btn_id = '""" + id_subscription + """'
    """)
    result_tuple = cur.fetchone()

    result_string = ''

    if result_tuple != None:
        result_string = common_methods.convertTuple(result_tuple)

    return result_string

#изменяет статус подписки
def change_user_subscription_status(id_subscription, status):
    cur.execute("""
    update subscriptions
       set active_flg = """+ str(status) + """
     where chat_id ||'_' ||id = '""" + id_subscription + """'
    """)

#выдает список пользователей для активной подписки
def get_users_id_of_current_subscription(name_of_subscription):

    list_of_id = []
    cur.execute("""
    select chat_id
      from subscriptions
     where subscription_name = '""" + name_of_subscription + """'
       and active_flg = 1
    """)

    rows = cur.fetchall()

    for item in rows:
        buffer = ''
        for char_one in str(item):
            for char_two in ('1234567890-'):
                if char_one == char_two:
                    buffer += char_one
        list_of_id.append(int(buffer))

    return list_of_id

#сохраняет данные для платежа
def save_data_for_payment(payment_data_out):

    cur.execute("""
    insert into payments (chat_id,
                          title,
                          descr)
    values (""" + str(payment_data_out[0]) + """,
            '""" + str(payment_data_out[1]) + """',
            '""" + str(payment_data_out[2]) + """')
    """)

#обновляет данные платежа
def upd_data_for_payment(payment_data_in):

    cur.execute("""
    update payments
    set currency                   = '""" +str(payment_data_in.successful_payment.currency)+ """',
        total_amount               = """ +str(payment_data_in.successful_payment.total_amount)+ """,
        telegram_payment_charge_id = '""" +str(payment_data_in.successful_payment.telegram_payment_charge_id)+ """',
        provider_payment_charge_id = '""" +str(payment_data_in.successful_payment.provider_payment_charge_id)+ """'
        where id = (select id
                      from payments
                     where chat_id = """+str(payment_data_in.chat.id)+"""
                     order by dt_ins desc
                     limit 1
                   )
    """)