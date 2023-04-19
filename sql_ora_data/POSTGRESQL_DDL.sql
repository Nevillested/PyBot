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

CREATE TABLE USERS_DATA (ID SERIAL , DT_INS TIMESTAMP DEFAULT current_timestamp, DT_UPD TIMESTAMP, chat_id bigint, MESSAGE_ID bigint, USERNAME text, CONTENT_TYPE_IN text, MESSAGE_DATA_CLOB_IN text, MESSAGE_VERSION_IN bigint DEFAULT 0, CONTENT_TYPE_OUT text, MESSAGE_DATA_CLOB_OUT text); 

COMMENT ON COLUMN USERS_DATA.ID IS 'ID строки';
COMMENT ON COLUMN USERS_DATA.DT_INS IS 'Дата вставки сообщения';
COMMENT ON COLUMN USERS_DATA.DT_UPD IS 'Дата обновления сообщения';
COMMENT ON COLUMN USERS_DATA.CHAT_ID IS 'ID сообщения в чате';
COMMENT ON COLUMN USERS_DATA.MESSAGE_ID IS 'ID сообщения';
COMMENT ON COLUMN USERS_DATA.USERNAME IS 'Никнейм пользователя';
COMMENT ON COLUMN USERS_DATA.CONTENT_TYPE_IN IS 'Тип входящих данных в сообщении';
COMMENT ON COLUMN USERS_DATA.MESSAGE_DATA_CLOB_IN IS 'Входящие данные в сообщении в text';
COMMENT ON COLUMN USERS_DATA.MESSAGE_VERSION_IN IS 'Версия входящего сообщения';
COMMENT ON COLUMN USERS_DATA.CONTENT_TYPE_OUT IS 'Тип исходящих данных в сообщении';
COMMENT ON COLUMN USERS_DATA.MESSAGE_DATA_CLOB_OUT IS 'Исходящие данные в текстовом виде';
COMMENT ON TABLE USERS_DATA  IS 'Переписка с пользователями';
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
