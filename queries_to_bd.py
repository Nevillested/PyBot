import oracledb
import common_methods

class queries_class(Exception):

    #проверяет пользователя в бд, если есть-обновляет данные, если нет-добавляет данные
    def check_user(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()

        chat_id = data_from_message.chat.id
        first_name = data_from_message.from_user.first_name
        username = data_from_message.from_user.username
        last_name = data_from_message.from_user.last_name
        language_code = data_from_message.from_user.language_code
        is_premium = str(data_from_message.from_user.is_premium)
        is_bot = str(data_from_message.from_user.is_bot)

        rows = [ (chat_id, first_name, username, last_name, language_code, is_premium, is_bot) ]
        cursor.executemany("""merge into john.users a
                              using (select :1 as chat_id
                                          , :2 as first_name
                                          , :3 as username
                                          , :4 as last_name
                                          , :5 as language_code
                                          , :6 as is_premium
                                          , :7 as is_bot
                                       from dual) b
                                 on (a.chat_id = b.chat_id)
                               when matched
                                 then update set
                                     a.first_name = b.first_name
                                   , a.username = b.username
                                   , a.last_name = b.last_name
                                   , a.language_code = b.language_code
                                   , a.is_premium = b.is_premium
                                   , a.is_bot = b.is_bot
                               when not matched
                                 then insert (  a.chat_id
                                              , a.first_name
                                              , a.username
                                              , a.last_name
                                              , a.language_code
                                              , a.is_premium
                                              , a.is_bot)
                                      values (  b.chat_id
                                              , b.first_name
                                              , b.username
                                              , b.last_name
                                              , b.language_code
                                              , b.is_premium
                                              , b.is_bot)""", rows)
        connection.commit()
    
    #сохраняет прилетевшие данные в переписке с пользователем
    def insert_user_story_in(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()

        chat_id = data_from_message.chat.id
        message_id = data_from_message.message_id
        username = data_from_message.from_user.username
        content_type = str(data_from_message.content_type)
        clob_data = data_from_message.text

        rows = [ (chat_id, message_id, username, content_type, clob_data) ]
        cursor.executemany("""insert into john.users_data (chat_id, message_id, username, content_type_in, message_data_clob_in)
                              values (:1, :2, :3, :4, :5 )""", rows)
        connection.commit()

    #добавляет новую версию отредактированного сообщения и возвращает предыдущую
    def insert_edited_msg(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        msg_text = data_from_message.text
        chat_id = data_from_message.chat.id
        message_id = data_from_message.message_id
        
        rows_in = [ (msg_text, chat_id, message_id) ]
        cursor.executemany("""insert into john.users_data( dt_ins
                                                         , dt_upd
                                                         , chat_id
                                                         , message_id
                                                         , username
                                                         , content_type_in
                                                         , message_data_clob_in
                                                         , message_version_in)
                                                    select dt_ins
                                                         , current_timestamp
                                                         , chat_id
                                                         , message_id
                                                         , username
                                                         , content_type_in
                                                         , :1
                                                         , message_version_in + 1
                                                      from (select *
                                                              from john.users_data 
                                                             where chat_id = :2
                                                               and message_id = :3
                                                              order by message_version_in desc)
                                                     where rownum = 1""", rows_in)
        connection.commit()

    #выдает последнюю версию отредактированного сообщения
    def get_last_ver_msg(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        chat_id = data_from_message.chat.id
        message_id = data_from_message.message_id
        
        cursor.execute("""select message_data_clob_in
                            from ( select message_data_clob_in
                                        , rownum as rn
                                     from (select *
                                             from john.users_data 
                                            where chat_id = :cur_chat_id
                                              and message_id = :cur_message_id
                                             order by message_version_in desc)
                                 )
                           where rn = 2""", cur_chat_id = chat_id, cur_message_id = message_id)
        result_tuple = cursor.fetchone()
        connection.commit()
        result_string = ''
        
        for item in result_tuple:
            result_string = result_string + str(item)
        
        return result_string
        
    #сохраняет улетевшие данные пользователю
    def insert_user_story_out(content_type_out, clob_data_out, chat_id, message_id):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        rows = [ (content_type_out, clob_data_out, chat_id, message_id) ]
        cursor.executemany("""update john.users_data set content_type_out = :1, message_data_out = :2 where chat_id = :3 and message_id = :4""", rows)
        connection.commit()

    #получает последнее свое отправленное сообщение
    def get_last_bot_msg(chat_id):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        cursor.execute("""select message_data_out
                            from ( select message_data_out
                                        , row_number() OVER(ORDER BY dt_ins DESC) rn
                                     from john.users_data a
                                    where chat_id = :cur_chat_id
                                    order by dt_ins desc)
                           where rn = 2""", cur_chat_id = chat_id)
        result_tuple = cursor.fetchone()
        connection.commit()
        result_string = ''

        if result_tuple != None:
            for item in result_tuple:
                result_string = result_string + str(item)

        return result_string

    #получает последний номер десятка кандзи
    def get_pre_last_user_msg(chat_id):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        cursor.execute("""select to_char(message_data_clob_in)
                            from ( select a.*
                                        , row_number() OVER(ORDER BY dt_ins DESC) rn
                                     from john.users_data a
                                    where chat_id = :cur_chat_id
                                      and message_data_out = 'квиз по по номеру десятка кандзи'
                                      and case when REGEXP_LIKE(message_data_clob_in, '^[[:digit:]]+$') then 1 else 0 end = 1
                                    order by dt_ins desc)
                           where rn = 1
                           """, cur_chat_id = chat_id)
        result_tuple = cursor.fetchone()
        connection.commit()
        result_string = ''

        if result_tuple != None:
            result_string = common_methods.convertTuple(result_tuple)

        return result_string

    #получает анекдот
    def get_joke():
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        cursor.execute("""select to_char(text_joke)
                            from (select *
                                    from jokes
                                   order by dbms_random.value)
                           where rownum = 1""")
        tuple_data = cursor.fetchone()
        connection.commit()
        anekdot =''
        for item in tuple_data:
            anekdot = anekdot + item
        return anekdot

    #создает строку для наполнения данных для шифрования/дешифрования
    def create_session_cezar(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()

        chat_id = data_from_message.chat.id
        method = data_from_message.text.replace("/", "")

        rows = [ (chat_id, method) ]
        cursor.executemany("""insert into john.cezar (chat_id, method)
                              values (:1, :2)""", rows)
        connection.commit()
    
    #добавляет язык обработки данных для шифрования/дешифрования
    def update_lang_session_cezar(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()

        chat_id = data_from_message.chat.id
        lang = data_from_message.text.lower()
        
        rows = [ (chat_id, lang) ]
        cursor.executemany("""merge into cezar a
                              using (select id
                                          , :1 as chat_id
                                          , :2 as lang
                                       from (select *
                                               from cezar
                                              order by dt_ins desc)
                                      where rownum = 1) b
                                 on (a.id = b.id and a.chat_id = b.chat_id)
                               when matched then update set a.lang = b.lang""", rows)
        connection.commit()
    
    #добавляет ключ для шифрования/дешифрования
    def update_key_session_cezar(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        chat_id = data_from_message.chat.id
        key = data_from_message.text
        
        rows = [ (chat_id, key) ]
        cursor.executemany("""merge into cezar a
                              using (select id
                                          , :1 as chat_id
                                          , :2 as key
                                       from (select *
                                               from cezar
                                              order by dt_ins desc)
                                      where rownum = 1) b
                                 on (a.id = b.id and a.chat_id = b.chat_id)
                               when matched then update set a.key = b.key""", rows)
        connection.commit()

    #добавляет текст для шифрования/дешифрования
    def update_messaage_in_session_cezar(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        chat_id = data_from_message.chat.id
        messaage_in = data_from_message.text
        
        rows = [ (chat_id, messaage_in) ]
        cursor.executemany("""merge into cezar a
                              using (select id
                                          , :1 as chat_id
                                          , :2 as messaage_in
                                       from (select *
                                               from cezar
                                              order by dt_ins desc)
                                      where rownum = 1) b
                                 on (a.id = b.id and a.chat_id = b.chat_id)
                               when matched then update set a.messaage_in = b.messaage_in""", rows)
        connection.commit()

    #выдает данные для шифрования
    def get_data_cezar(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        chat_id = data_from_message.chat.id
        
        rows = [ (chat_id) ]
        for row in cursor.execute("""select lang
                                          , key
                                          , method
                                          , to_char(messaage_in) as messaage_in
                                       from (select *
                                               from cezar
                                              where chat_id = :1
                                              order by dt_ins desc)
                                      where rownum = 1""", rows):
            val = row
        connection.commit()
        return val[0],val[1],val[2],val[3]

    #выдает какой-нибудь ответ, который у него есть в вопрос-ответнике
    def get_other_answer(user_text):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        rows = [ (user_text) ]
        for row in cursor.execute("""with
                                     t1 as ( select outcome 
                                               from (select outcome, 
                                                            UTL_MATCH.edit_distance_similarity(lower(income), lower(:var)) as match_procent 
                                                       from other_answers 
                                                      order by dbms_random.value ) 
                                              where match_procent >= 85 
                                                and rownum = 1 
                                           ) 
                                     select case 
                                              when EXISTS(select outcome from t1) 
                                                then (select outcome from t1) 
                                              else 'моя твоя не понимать, сори' 
                                            end as answer_to_client 
                                       from dual""", rows):
            val = row
        connection.commit()
        return val[0]
    
    #создает новую сессию распознавания текста, добавляет язык
    def create_session_voice(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        rows = [ (data_from_message.chat.id, data_from_message.text) ]
        cursor.executemany("""insert into john.voices (chat_id, lang) values (:1, :2)""", rows)
        connection.commit()

    #выдает язык распознавания текста
    def get_lang_voice(data_from_message):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        rows = [ (data_from_message.chat.id) ]
        for row in cursor.execute("""select lang
                                       from ( select lang
                                                   , rownum as rn
                                                from ( select *
                                                         from john.voices
                                                        where chat_id = :chat_id
                                                        order by dt_ins desc
                                                     )
                                            )
                                      where rn = 1""", rows):
            val = row
        connection.commit()
        return val[0]

    #сохраняет распознанный текст
    def insert_result_recognize_speech(data_from_message, result_recog):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        rows = [ (result_recog, data_from_message.chat.id) ]
        cursor.executemany("""update john.voices
                                 set result_text = :1
                               where id = (select id
                                             from (select id
                                                        , rownum as rn
                                                     from ( select *
                                                             from john.voices
                                                            where chat_id = :2
                                                            order by dt_ins desc
                                                          )
                                                   )
                                            where rn = 1
                                          )""", rows)
        connection.commit()

    #возвращает перевод слова из "новые слова"
    def get_translate_jp(user_word):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()

        for row in cursor.execute(""" select coalesce(
                                                        LISTAGG('С кандзи: '||coalesce(t1.jap_word_with_kanji,'-')||'\nБез кандзи: '||coalesce(t1.jap_word_without_kanji,'-')||'\nПеревод: '||coalesce(t1.rus_word,'-')||'' ,'\n\n')
                                                      , 'Мы ничего не нашли'
                                                     ) as result_output 
                                        from (select jap_word_with_kanji
                                                   , jap_word_without_kanji
                                                   , rus_word
                                                   , '1' as rn
                                                from jap_dict
                                             ) t1
                                       inner
                                        join (select :cur_user_word as user_word
                                                   , '1' as rn
                                                from dual
                                             ) t2
                                          on t1.rn = t2.rn
                                       where lower(t1.rus_word) like '%'||lower(t2.user_word)||'%'""", cur_user_word = user_word):
            val = row
        connection.commit()
        result = common_methods.convertTuple(val)
        return result

    #возвращает список кандзи по номеру десятка
    def get_kanji(user_value):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()

        for row in cursor.execute("""with t1 as (select :cur_value as value from dual)
                                       select coalesce((listagg(('Кандзи: '||kanji||'\nПеревод: '||RUS_WORD||'\nЧтения: '||reading||'\nПримеры:\n '||examples),'\n\n')),'Мы ничего не нашли, попробуй изменить номер десятка.')
                                       from JOHN.JAP_KANJI
                                      where id < (select (value)*10 from t1)
                                        and id >= (select (value-1)*10 from t1)""", cur_value = user_value):
            val = row
        connection.commit()
        result = common_methods.convertTuple(val)
        return result

    #возвращает данные для квиза но номеру десятка
    def get_decade_kanji_quiz(num_decade):
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        list_of_rows = []

        for row in cursor.execute("""with
                                     all_vars as (
                                       select a.kanji
                                            , a.reading
                                            , a.rus_word
                                            , rownum as rn
                                         from (select a.*
                                                    , rownum as rn
                                                 from ( select *
                                                          from john.jap_kanji
                                                         where id >=10 * ( :var - 1 )
                                                           and id < 10 * :var
                                                         order by dbms_random.value
                                                      ) a
                                              ) a
                                        where rn <= 4
                                       ),
                                       
                                       rand_val as(
                                         select round(dbms_random.value(1,4)) as rand
                                           from dual
                                       )
                                       /*берем правильный ответ*/
                                       select kanji, 'Чтение '||reading||'. Перевод '||rus_word,rn from all_vars where rn = (select rand from rand_val)
                                       /*объединяем со всеми, которые имеются*/
                                       union all
                                       select kanji, 'Чтение '||reading||'. Перевод '||rus_word,rn from all_vars """, var = num_decade):
            list_of_rows.append(row)
            
        connection.commit()

        return list_of_rows

    #возвращает данные для квиза по всем имеющимся кадзи
    def get_all_kanji_quiz():
        connection = oracledb.connect(user="john", password="ipiheb60", dsn="localhost:1521/xe")
        cursor = connection.cursor()
        
        list_of_rows = []

        for row in cursor.execute("""with
                                     all_vars as (
                                       select a.kanji
                                            , a.reading
                                            , a.rus_word
                                            , rownum as rn
                                         from (select a.*
                                                    , rownum as rn
                                                 from ( select *
                                                          from john.jap_kanji
                                                         order by dbms_random.value
                                                      ) a
                                              ) a
                                        where rn <= 4
                                       ),
                                       
                                       rand_val as(
                                         select round(dbms_random.value(1,4)) as rand
                                           from dual
                                       )
                                       /*берем правильный ответ*/
                                       select kanji, 'Чтение '||reading||'. Перевод '||rus_word,rn from all_vars where rn = (select rand from rand_val)
                                       /*объединяем со всеми, которые имеются*/
                                       union all
                                       select kanji, 'Чтение '||reading||'. Перевод '||rus_word,rn from all_vars """):
            list_of_rows.append(row)
            
        connection.commit()

        return list_of_rows