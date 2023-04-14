import keyboards_buttons
import queries_to_bd

#квиз по всем имеющимся кандзи
def get_all_kanji_quiz():
    content_type_out = "poll"
    result_out = []
    reply_out = keyboards_buttons.retry_quiz()
    list_of_rows = queries_to_bd.get_all_kanji_quiz() #получаем строки с данными
    tuple_row_with_right_answer = list_of_rows[0] #забираем всю первую строку
    answer_desc_out = tuple_row_with_right_answer[0] #забираем вопрос из 1 строки, 1 столбца
    list_of_rows.pop(0) #удаляем первую строку, тк она больше не нужна
    correct_answer_id_out = list_of_rows.index(tuple_row_with_right_answer) #забираем индекс правильного ответа
    for item in list_of_rows:
        result_out.append(item[1])
    result_out.insert(0,"квиз по всем имеющимся кандзи")
    return answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out





    #content_type_out = "poll"
    #result_out = []
    #reply_out = keyboards_buttons.retry_quiz()
    #list_of_rows = queries_to_bd.get_all_kanji_quiz() #получаем строки с данными
    #tuple_row_with_right_answer = list_of_rows[0] #забираем всю первую строку
    #answer_desc_out = tuple_row_with_right_answer[0] #забираем вопрос из 1 строки, 1 столбца
   # correct_answer_id_out = tuple_row_with_right_answer[2] #забираем номер правильного ответа из 1 строки, 3 столбца
   # correct_answer_id_out = correct_answer_id_out - 1
   # list_of_rows.pop(0) #удаляем первувю строку, тк она больше не нужна
   # for item in list_of_rows:
   #     result_out.append(item[1])
   # result_out.insert(0,"квиз по всем имеющимся кандзи")
    #return answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out

#квиз по номеру десятка среди имеющихся кандзи
def get_decade_kanji_quiz(decade_num):
    content_type_out = "poll"
    result_out = []
    reply_out = keyboards_buttons.retry_quiz()
    list_of_rows = queries_to_bd.get_decade_kanji_quiz(decade_num) #получаем строки с данными
    tuple_row_with_right_answer = list_of_rows[0] #забираем всю первую строку
    answer_desc_out = tuple_row_with_right_answer[0] #забираем вопрос из 1 строки, 1 столбца
    list_of_rows.pop(0) #удаляем первую строку, тк она больше не нужна
    correct_answer_id_out = list_of_rows.index(tuple_row_with_right_answer) #забираем индекс правильного ответа
    for item in list_of_rows:
        result_out.append(item[1])
    result_out.insert(0,"квиз по по номеру десятка кандзи")
    return answer_desc_out, correct_answer_id_out, content_type_out, result_out, reply_out