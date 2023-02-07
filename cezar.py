class cezar_class(Exception):

    def encrypt_decrypt(chifr, n, l, fraza):
        eng_lower_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        eng_upper_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        rus_lower_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        rus_upper_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        symbol = [" ", ",", ".", "!", "?"]
        if l.lower() == 'ru':
            moch = 32
        if l.lower() == 'en':
            moch = 26
        if chifr == 'encrypt':
            n = n
        elif chifr == 'decrypt':
            n = -n
        else:
            n = 0
        result = ''
        
        for i in range(len(fraza)):
            if fraza[i].isalpha():
                if fraza[i] == fraza[i].upper():
                    for j in range (moch):
                        if moch == 32:
                            if fraza[i] == rus_upper_alphabet[j]:
                                result = result + rus_upper_alphabet[(j+n)%moch]
                                break
                        if moch == 26:
                            if fraza[i] == eng_upper_alphabet[j]:
                                result = result + eng_upper_alphabet[(j+n)%moch]
                                break
                elif fraza[i] ==fraza[i].lower():
                    for j in range (moch):
                        if moch == 32:
                            if fraza[i] == rus_lower_alphabet[j]:
                               result = result + rus_lower_alphabet[(j+n)%moch]
                               break
                        if moch == 26:
                            if fraza[i] == eng_lower_alphabet[j]:
                               result = result + eng_lower_alphabet[(j+n)%moch]
                               break
            else:
                result = result + fraza[i]
        return result