--------------------------------------------------------
--  File created - Friday-March-24-2023
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table CEZAR
--------------------------------------------------------

CREATE TABLE CEZAR (ID SERIAL , DT_INS timestamp DEFAULT current_timestamp, chat_id bigint, LANG text, KEY bigint, METHOD text, MESSAAGE_IN text); 

COMMENT ON COLUMN CEZAR.ID IS 'ID строки';
COMMENT ON COLUMN CEZAR.DT_INS IS 'Дата вставки';
COMMENT ON COLUMN CEZAR.CHAT_ID IS 'ID чата';
COMMENT ON COLUMN CEZAR.LANG IS 'Язык';
COMMENT ON COLUMN CEZAR.KEY IS 'Ключ';
COMMENT ON COLUMN CEZAR.METHOD IS 'Метод обработки сообщения';
COMMENT ON COLUMN CEZAR.MESSAAGE_IN IS 'Сообщение';
COMMENT ON TABLE CEZAR  IS 'Данные для широфвания/дешифрования по Цезарю';
--------------------------------------------------------
--  DDL for Table COMPLIMENTS
--------------------------------------------------------

CREATE TABLE COMPLIMENTS (ID SERIAL , TEXT text); 

COMMENT ON COLUMN COMPLIMENTS.ID IS 'ID комплимента';
COMMENT ON COLUMN COMPLIMENTS.TEXT IS 'Текст комплимента';
COMMENT ON TABLE COMPLIMENTS  IS 'Комплименты';
--------------------------------------------------------
--  DDL for Table INLINE_MODE_DATA
--------------------------------------------------------

CREATE TABLE INLINE_MODE_DATA (ID SERIAL , DT_INS timestamp DEFAULT current_timestamp, QUERY_FROM bigint, QUERY_TEXT text); 

COMMENT ON COLUMN INLINE_MODE_DATA.ID IS 'ID строки';
COMMENT ON COLUMN INLINE_MODE_DATA.DT_INS IS 'Дата вставки';
COMMENT ON COLUMN INLINE_MODE_DATA.QUERY_FROM IS 'ID пользователя, делающего запрос';
COMMENT ON COLUMN INLINE_MODE_DATA.QUERY_TEXT IS 'Текст запроса';
COMMENT ON TABLE INLINE_MODE_DATA  IS 'Данные по отправке сообщений другому пользователю через бота';
--------------------------------------------------------
--  DDL for Table INTERNATIONAL_HOLIDAY
--------------------------------------------------------

CREATE TABLE INTERNATIONAL_HOLIDAY (ID SERIAL , TEXT_HOLIDAY TEXT, DATE_HOLIDAY timestamp); 

COMMENT ON COLUMN INTERNATIONAL_HOLIDAY.ID IS 'ID строки';
COMMENT ON COLUMN INTERNATIONAL_HOLIDAY.TEXT_HOLIDAY IS 'Текст праздник';
COMMENT ON COLUMN INTERNATIONAL_HOLIDAY.DATE_HOLIDAY IS 'Дата праздника';
COMMENT ON TABLE INTERNATIONAL_HOLIDAY  IS 'Словарь междунароных праздников';
--------------------------------------------------------
--  DDL for Table JAP_DICT
--------------------------------------------------------

CREATE TABLE JAP_DICT (ID SERIAL , JAP_WORD_WITHOUT_KANJI text, JAP_WORD_WITH_KANJI text, RUS_WORD text); 

COMMENT ON COLUMN JAP_DICT.ID IS 'ID строки';
COMMENT ON COLUMN JAP_DICT.JAP_WORD_WITHOUT_KANJI IS 'Написание на японском без кандзи';
COMMENT ON COLUMN JAP_DICT.JAP_WORD_WITH_KANJI IS 'Написание на японском с кандзи';
COMMENT ON COLUMN JAP_DICT.RUS_WORD IS 'Русский перевод';
COMMENT ON TABLE JAP_DICT  IS 'Японский словарь';
--------------------------------------------------------
--  DDL for Table JAP_KANJI
--------------------------------------------------------

CREATE TABLE JAP_KANJI (ID SERIAL , KANJI text, READING text, RUS_WORD text, EXAMPLES text); 

COMMENT ON COLUMN JAP_KANJI.ID IS 'ID строки';
COMMENT ON COLUMN JAP_KANJI.KANJI IS 'Иероглиф кандзи';
COMMENT ON COLUMN JAP_KANJI.READING IS 'Чтение';
COMMENT ON COLUMN JAP_KANJI.RUS_WORD IS 'Русский перевод';
COMMENT ON COLUMN JAP_KANJI.EXAMPLES IS 'Примеры';
COMMENT ON TABLE JAP_KANJI  IS 'Кандзи';
--------------------------------------------------------
--  DDL for Table JOKES
--------------------------------------------------------

CREATE TABLE JOKES (ID SERIAL , TEXT_JOKE text); 

COMMENT ON COLUMN JOKES.ID IS 'ID строки';
COMMENT ON COLUMN JOKES.TEXT_JOKE IS 'Текст анекдота';
COMMENT ON TABLE JOKES  IS 'Анекдоты';
--------------------------------------------------------
--  DDL for Table RESENDING_DATA
--------------------------------------------------------

CREATE TABLE RESENDING_DATA (ID SERIAL , DT_INS timestamp DEFAULT current_timestamp, SEND_FROM bigint, SEND_TO bigint, TYPE_DATA text, SEND_DATA text); 

COMMENT ON COLUMN RESENDING_DATA.ID IS 'ID строки';
COMMENT ON COLUMN RESENDING_DATA.DT_INS IS 'Дата вставки';
COMMENT ON COLUMN RESENDING_DATA.SEND_FROM IS 'ID пользователя, отправивишего сообщение';
COMMENT ON COLUMN RESENDING_DATA.SEND_TO IS 'ID пользователя, принимающего сообщение';
COMMENT ON COLUMN RESENDING_DATA.TYPE_DATA IS 'Тип данных';
COMMENT ON COLUMN RESENDING_DATA.SEND_DATA IS 'Данные в текстовом виде';
COMMENT ON TABLE RESENDING_DATA  IS 'Данные по отправке сообщений другому пользователю через бота';
--------------------------------------------------------
--  DDL for Table USERS
--------------------------------------------------------

CREATE TABLE USERS (ID SERIAL , DT_INS TIMESTAMP DEFAULT current_timestamp, chat_id bigint, FIRST_NAME text, USERNAME text, LAST_NAME text, LANGUAGE_CODE text, IS_PREMIUM text, IS_BOT text); 

COMMENT ON COLUMN USERS.ID IS 'ID строки';
COMMENT ON COLUMN USERS.DT_INS IS 'Дата вставки';
COMMENT ON COLUMN USERS.CHAT_ID IS 'ID чата';
COMMENT ON COLUMN USERS.FIRST_NAME IS 'Отображаемое имя';
COMMENT ON COLUMN USERS.USERNAME IS 'Никнейм';
COMMENT ON COLUMN USERS.LAST_NAME IS 'Отображаемая амилия';
COMMENT ON COLUMN USERS.LANGUAGE_CODE IS 'Языковой код';
COMMENT ON COLUMN USERS.IS_PREMIUM IS 'Премиум?';
COMMENT ON COLUMN USERS.IS_BOT IS 'Бот?';
COMMENT ON TABLE USERS  IS 'Пользователи';
--------------------------------------------------------
--  DDL for Table USERS_DATA
--------------------------------------------------------
select * from users_data
--where chat_id = 1275894304
order by dt_ins desc



create table income (ID SERIAL ,
					 DT_INS TIMESTAMP DEFAULT current_timestamp,
					 DT_UPD TIMESTAMP,
					 chat_id bigint,
					 MESSAGE_ID bigint,
					 MESSAGE_TYPE text,
					 MESSAGE_VERSION bigint DEFAULT 0,
					 MESSAGE_DATA text); 
					 
COMMENT ON COLUMN income.id is 'ID строки';
COMMENT ON COLUMN income.DT_INS is 'Дата вставки сообщения';
COMMENT ON COLUMN income.DT_UPD is 'Дата обновления сообщения';
COMMENT ON COLUMN income.chat_id is 'ID чата';
COMMENT ON COLUMN income.MESSAGE_ID is 'ID сообщения в чате';
COMMENT ON COLUMN income.MESSAGE_TYPE is 'Тип данных';
COMMENT ON COLUMN income.MESSAGE_VERSION is 'Версия сообщения';
COMMENT ON COLUMN income.MESSAGE_DATA is 'Текстовые данные';
COMMENT ON TABLE income IS 'Входящие данные';


create table outcome (ID SERIAL ,
					 DT_INS TIMESTAMP DEFAULT current_timestamp,
					 DT_UPD TIMESTAMP,
					 chat_id bigint,
					 MESSAGE_ID bigint,
					 MESSAGE_TYPE text,
					 MESSAGE_VERSION bigint DEFAULT 0,
					 MESSAGE_DATA text); 
					 
COMMENT ON COLUMN outcome.id is 'ID строки';
COMMENT ON COLUMN outcome.DT_INS is 'Дата вставки сообщения';
COMMENT ON COLUMN outcome.DT_UPD is 'Дата обновления сообщения';
COMMENT ON COLUMN outcome.chat_id is 'ID чата';
COMMENT ON COLUMN outcome.MESSAGE_ID is 'ID сообщения в чате';
COMMENT ON COLUMN outcome.MESSAGE_TYPE is 'Тип данных';
COMMENT ON COLUMN outcome.MESSAGE_VERSION is 'Версия сообщения';
COMMENT ON COLUMN outcome.MESSAGE_DATA is 'Текстовые данные';
COMMENT ON TABLE outcome IS 'Исходящие данные';
--------------------------------------------------------
--  DDL for Table VOICES
--------------------------------------------------------

CREATE TABLE VOICES (ID SERIAL , DT_INS timestamp DEFAULT current_timestamp, chat_id bigint, LANG TEXT, RESULT_TEXT text);

COMMENT ON COLUMN VOICES.ID IS 'ID строки';
COMMENT ON COLUMN VOICES.DT_INS IS 'Дата вставки';
COMMENT ON COLUMN VOICES.CHAT_ID IS 'ID чата';
COMMENT ON COLUMN VOICES.LANG IS 'Язык распознавания';
COMMENT ON COLUMN VOICES.RESULT_TEXT IS 'Текстовый результат';
COMMENT ON TABLE VOICES  IS 'Распознавание голоса';
--------------------------------------------------------
--  DDL for Table payments
--------------------------------------------------------
CREATE TABLE payments(id serial,
                      dt_ins timestamp DEFAULT current_timestamp, 
                      chat_id bigint,
                      title text,
                      descr text,
                      currency text,
                      total_amount int,
                      telegram_payment_charge_id text,
                      provider_payment_charge_id text
                     );
                          
COMMENT ON COLUMN payments.ID IS 'ID строки';
COMMENT ON COLUMN payments.DT_INS IS 'Дата вставки';
COMMENT ON COLUMN payments.chat_id IS 'ID часа с юзером, запросивший данные';
COMMENT ON COLUMN payments.title IS 'Заголовок платежа';
COMMENT ON COLUMN payments.descr IS 'Описание платежа';
COMMENT ON COLUMN payments.currency IS 'Валюта платежа';
COMMENT ON COLUMN payments.total_amount IS 'Сумма платежа';
COMMENT ON COLUMN payments.telegram_payment_charge_id IS 'ID платежа телеги';
COMMENT ON COLUMN payments.provider_payment_charge_id IS 'ID платежа платежной системы';
COMMENT ON TABLE payments  IS 'Данные платежей';
--------------------------------------------------------
--  DDL for Table music_files
--------------------------------------------------------
CREATE TABLE music_files(ID SERIAL,
			 FIRST_CHAR_PERFORMER_DISPLAY_NAME text,
                         FIRST_CHAR_PERFORMER_ID text,
                         PERFORMER_DISPLAY_NAME text,
                         PERFORMER_DISPLAY_ID text,
                         ALBUM_DISPLAY_NAME text,
                         ALBUM_DISPLAY_ID text,
                         SONG_DISPLAY_NAME text,
                         SONG_DISPLAY_ID text,
			 PATH_TO_FILE text
                        );
                          
COMMENT ON COLUMN music_files.ID is 'ID строки';
COMMENT ON COLUMN music_files.FIRST_CHAR_PERFORMER_DISPLAY_NAME is 'Первая буква названия исполнителя';
COMMENT ON COLUMN music_files.FIRST_CHAR_PERFORMER_ID is 'ID первой буквы названия исполнителя';
COMMENT ON COLUMN music_files.PERFORMER_DISPLAY_NAME is 'Название исполнителя';
COMMENT ON COLUMN music_files.PERFORMER_DISPLAY_ID is 'ID исполнителя';
COMMENT ON COLUMN music_files.ALBUM_DISPLAY_NAME is 'Название альбома';
COMMENT ON COLUMN music_files.ALBUM_DISPLAY_ID is 'ID альбома';
COMMENT ON COLUMN music_files.SONG_DISPLAY_NAME is 'Название песни';
COMMENT ON COLUMN music_files.SONG_DISPLAY_ID IS 'ID песни';
COMMENT ON COLUMN music_files.PATH_TO_FILE is 'Путь к песне';
COMMENT ON TABLE music_files IS 'Данные музыки';
--------------------------------------------------------
--  DDL for Table notifications
--------------------------------------------------------
CREATE TABLE PUBLIC.NOTIFICATIONS (ID SERIAL, CHAT_ID bigint, NOTIF_NAME text, ACTIVITY_FLG int default 0, DT_CREATED timestamp DEFAULT current_timestamp, DT_UPDATED timestamp, repeat_flg int, EVERY_YEAR_FLG int, EVERY_MONTH_FLG int, EVERY_WEEK_FLG int, EVERY_DAY_FLG int, EVERY_HOUR_FLG int, EVERY_MINUTE_FLG int, YEAR_NUM int, MONTH_NUM int,  DAY_NUM int, HOUR_NUM int, MINUTE_NUM int);

COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.ID IS 'ID строки';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.CHAT_ID IS 'ID чата';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.NOTIF_NAME IS 'Название';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.ACTIVITY_FLG IS 'Флаг активности напоминалки';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.DT_CREATED IS 'Дата создания';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.DT_UPDATED IS 'Дата обновления';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.REPEAT_FLG IS 'Дата обновления';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.EVERY_YEAR_FLG IS 'Флаг повторения каждый год';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.EVERY_MONTH_FLG IS 'Флаг повторения каждый месяц';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.EVERY_WEEK_FLG IS 'Флаг повторения каждую неделю';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.EVERY_DAY_FLG IS 'Флаг повтороения каждый день';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.EVERY_HOUR_FLG IS 'Флаг повтороения каждый час';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.EVERY_MINUTE_FLG IS 'Флаг повтороения каждую минуту';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.YEAR_NUM IS 'Номер года';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.MONTH_NUM IS 'Номер месяца';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.DAY_NUM IS 'Номер дня месяца';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.HOUR_NUM IS 'Номер часа';
COMMENT ON COLUMN PUBLIC.NOTIFICATIONS.MINUTE_NUM IS 'Номер минуты';
COMMENT ON TABLE PUBLIC.NOTIFICATIONS IS 'Напоминалки юзеров';
--------------------------------------------------------
--  DDL for procedure new_notification
--------------------------------------------------------
CREATE OR REPLACE procedure new_notification(IN chat_id BIGINT, IN notif_name text)
language plpgsql
as $$
declare
begin
  insert into public.notifications (chat_id, notif_name)
  values (chat_id, notif_name);

  commit;
end;
$$;
--------------------------------------------------------
--  DDL for procedure reset_repeat_not
--------------------------------------------------------
CREATE OR REPLACE procedure reset_repeat_not(IN p_chat_id BIGINT)
language plpgsql
as $$
declare
begin
    -- subtracting the amount from the sender's account 
    update notifications 
    set repeat_flg = Null, EVERY_YEAR_FLG = Null, EVERY_MONTH_FLG = Null, EVERY_WEEK_FLG = Null, EVERY_DAY_FLG = Null, EVERY_HOUR_FLG = Null, EVERY_MINUTE_FLG= Null
    where id = (select id
from notifications
  where chat_id = p_chat_id
    and activity_flg = 0
  order by id desc
  limit  1);

    commit;
end;
$$;
--------------------------------------------------------
--  DDL for procedure set_music_id
--------------------------------------------------------
CREATE OR REPLACE procedure set_music_id()
language plpgsql
as $$
declare
rec                                 record;
l_first_char_performer_id           text;
l_first_char_performer_display_name text := '';
l_performer_display_id              text;
l_performer_display_name            text := '';
l_album_display_id                  text;
l_album_display_name                text := ''; 
begin
  execute 'ALTER SEQUENCE music_files_id_seq RESTART WITH 1';
  update music_files set first_char_performer_id = null, performer_display_id = null, album_display_id = null, song_display_id = null;
  for rec in (select id,
			         first_char_performer_display_name,
                     first_char_performer_id,
                     performer_display_name,
                     performer_display_id,
                     album_display_name,
                     album_display_id,
                     song_display_name,
                     song_display_id,
				     path_to_file
                from music_files
               order by path_to_file asc)
  loop
	if l_first_char_performer_display_name is null or 
	   l_performer_display_name is null or
	   l_album_display_name is null
      then
        l_first_char_performer_display_name := rec.first_char_performer_display_name;
	    l_performer_display_name            := rec.performer_display_name;
	    l_album_display_name                := rec.album_display_name;
		l_first_char_performer_id           := make_uid('first_char_performer_id');
		l_performer_display_id              := make_uid('performer_display_id');
		l_album_display_id                  := make_uid('album_display_id');
	end if;
	
    if rec.first_char_performer_display_name = l_first_char_performer_display_name
	  then 
	    update music_files set first_char_performer_id = l_first_char_performer_id where id = rec.id;
	  else
	    l_first_char_performer_display_name := rec.first_char_performer_display_name;
		l_first_char_performer_id           := make_uid('first_char_performer_id');
	    update music_files set first_char_performer_id = l_first_char_performer_id where id = rec.id;
	end if;
	
    if rec.performer_display_name = l_performer_display_name
	  then 
	    update music_files set performer_display_id = l_performer_display_id where id = rec.id;
	  else
	    l_performer_display_name := rec.performer_display_name;
		l_performer_display_id   := make_uid('performer_display_id');
	    update music_files set performer_display_id = l_performer_display_id where id = rec.id;
	end if;
	
	if rec.album_display_name = l_album_display_name
	  then
	    update music_files set album_display_id = l_album_display_id where id = rec.id;
	  else
	    l_album_display_name := rec.album_display_name;
		l_album_display_id   := make_uid('album_display_id');
	    update music_files set album_display_id = l_album_display_id where id = rec.id;
	end if;
	
	update music_files set song_display_id = make_uid('song_display_id') where id = rec.id;
	
  end loop;
end;
$$;
--------------------------------------------------------
--  DDL for FUNCTION make_uid
--------------------------------------------------------
CREATE OR REPLACE FUNCTION make_uid(p_column_name text)
RETURNS text
language plpgsql
as
$$
declare
  result   text;
  done     bool;
  chars    text[] := '{A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}';
  length   integer := 10;
  i        integer := 0;
  cnt      integer;
  sql_stmt text := 'select count(*) from music_files where '||p_column_name||'=';
BEGIN

  done := false;
  IF p_column_name = 'first_char_performer_id'
    THEN result := 'mus_abc_';
  ELSIF p_column_name = 'performer_display_id'
    THEN RESULT := 'mus_per_';
  ELSIF p_column_name = 'album_display_id'
    THEN RESULT := 'mus_alb_';
  ELSIF p_column_name = 'song_display_id'
    THEN RESULT := 'mus_son_';
  END IF;
	
  WHILE NOT done LOOP
    for i in 1..length loop
      result := result || chars[1+random()*(array_length(chars, 1)-1)];
    end loop;

    sql_stmt := sql_stmt ||''''||result||'''';
    execute sql_stmt into cnt;
    if cnt = 0
      then done := true;
    end if;

  END LOOP;
  RETURN result;
END;
$$;
