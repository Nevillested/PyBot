#проверяет в строке наличие не русских букв. Если нашел-возвращает -1, если все ок и не нашел - возвращает 0
def check_ru_char_in_string(string_income):

    string_income_lower = string_income.lower()
    ru_char_array = 'абвгдежзийклмнопрстуфхцчшщъыьэюя '
    result_out = ""

    for c in string_income_lower:
        for r in ru_char_array:
            if c == r:
                result_out = result_out + c

    if string_income_lower == result_out:
        return 0
    else:
        return -1

#проверяет в строке наличие не английских букв. Если нашел-возвращает -1, если все ок и не нашел - возвращает 0
def check_en_char_in_string(string_income):

    string_income_lower = string_income.lower()
    en_char_array = 'abcdefghijklmnopqrstuvwxyz '
    result_out = ""

    for c in string_income_lower:
        for r in en_char_array:
            if c == r:
                result_out = result_out + c

    if string_income_lower == result_out:
        return 0
    else:
        return -1