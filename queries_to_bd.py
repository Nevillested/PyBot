import common_methods
import oracledb
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
    insert into users_data ( chat_id,
                             message_id,
                             username,
                             content_type_in,
                             message_data_clob_in
                           )
    values (  """ + chat_id + """,
              """ + message_id + """,
             '""" + username + """',
             '""" + content_type + """',
             '""" + data_in + """'
           );
    """)

#сохраняет улетевшие данные пользователю в переписке с ботом
def insert_user_story_out(content_type_out, clob_data_out, chat_id, message_id, flg_counter_msg):

    content_type_out = str(content_type_out) or ''
    clob_data_out = str(clob_data_out) or ''
    chat_id = str(chat_id) or ''
    message_id = str(message_id) or ''

    #flg_counter_msg - это флаг встречного сообщения
    #Если он равен 1, то улетающее сообщение - это ответ на сообщение пользователя
    #Если он равен 0, то улетающее сообщение - просто сообщение, как правило это рассылка
    if flg_counter_msg == 1:
        cur_string = """
        update users_data
           set content_type_out      = '""" + content_type_out + """',
               message_data_clob_out = '""" + clob_data_out.replace("'", "") + """'
         where chat_id = """ + chat_id + """
           and message_id = """ + message_id + """
        """
    elif flg_counter_msg == 0:
        cur_string = """
        insert into users_data (chat_id, content_type_out, message_data_clob_out)
        values (""" + chat_id + """, '""" + content_type_out + """', '""" + clob_data_out.replace("'","") + """')
        """

    cur.execute(cur_string)

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
    select a.message_data_clob_out
      from ( select message_data_clob_out
                  , row_number() OVER(ORDER BY dt_ins DESC) rn
               from users_data a
              where chat_id = """ + str(chat_id) + """
              order by dt_ins desc) as a
     where a.rn = 2""")
    result_tuple = cur.fetchone()
    result_string = ''

    if result_tuple != None:
        for item in result_tuple:
            result_string = result_string + str(item)

    return result_string

#получает предпоследнее сообщение пользователя
def get_prelast_user_msg(chat_id):

    cur.execute("""
    select a.message_data_clob_in
      from (select message_data_clob_in,
                   ROW_NUMBER () OVER (ORDER BY dt_ins desc) as rn
              from users_data a
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

#добавляет новую версию отредактированного сообщения и возвращает предыдущую
def insert_edited_msg(data_from_message):

    msg_text = str(data_from_message.text)
    chat_id = str(data_from_message.chat.id)
    message_id = str(data_from_message.message_id)

    cur.execute("""
    insert into users_data( dt_ins
                          , dt_upd
                          , chat_id
                          , message_id
                          , username
                          , content_type_in
                          , message_data_clob_in
                          , message_version_in)
                     select a.dt_ins
                          , current_timestamp
                          , a.chat_id
                          , a.message_id
                          , a.username
                          , a.content_type_in
                          , '""" + msg_text + """'
                          , a.message_version_in + 1
                       from (select *
                               from users_data
                              where chat_id = """ + chat_id + """
                                and message_id = """ + message_id + """
                               order by message_version_in desc
                               limit 1) a
    """)

#выдает последнюю версию отредактированного сообщения
def get_last_ver_msg(data_from_message):

    chat_id = str(data_from_message.chat.id)
    message_id = str(data_from_message.message_id)

    cur.execute("""
    select a.message_data_clob_in
      from ( select message_data_clob_in,
                    ROW_NUMBER () OVER (ORDER BY message_version_in desc) as rn
               from users_data
              where chat_id = """ + chat_id + """
                and message_id = """ + message_id + """
              order by message_version_in desc
           ) as a
     where a.rn = 2
    """)

    result_tuple = cur.fetchone()

    result_string = common_methods.convertTuple(result_tuple)

    return result_string

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


