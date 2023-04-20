import telebot
import my_cfg
import sending

def command_pay(message, PyBot, id_payment):

    #объявляем основные выходные параметры
    title_out = None
    description_out = None
    invoice_payload_out = 'Shut up and take my money!'
    currency_out = 'RUB'
    prices_out = None
    photo_url_out = None
    start_parameter_out = 'payment_start'
    max_tip_amount_out = None
    suggested_tip_amounts_out = None

    if id_payment == "payment_one_btn":
        title_out = 'owner = one love'
        description_out = 'Потому что я такой хорошенький'
        photo_url_out = None#'https://i.ibb.co/H7Zv0qp/1.jpg'
        prices_out = 10000
    elif id_payment == "payment_two_btn":
        title_out = 'Денег нет, но ты держись'
        description_out = 'Не помирай плз, держи 150р'
        photo_url_out = None#'https://i.ibb.co/DrR4mpk/2.jpg'
        prices_out = 15000
    elif id_payment == "payment_three_btn":
        title_out = 'Бот - это святое'
        description_out = 'Ты только представь свою жизнь без этого бота. Ага, и я о том же, расчехляй кошель'
        photo_url_out = None#'https://i.ibb.co/6v1DT1d/3.jpg'
        prices_out = 20000
    elif id_payment == "payment_shinobu":
        title_out = 'ka-ka'
        description_out = 'Шинобу - лучшая девочка, ты это понимаешь?\nПоэтому давай, расчехляй свой кошель и без лишних вопросов скидывайся на кошерные фигурки.\nВсе скидываются, и ты скидывайся, давай, не ломайся\n(тут могла быть ваша пассивно-агрессивная реклама)'
        photo_url_out = None#'https://i.ibb.co/3vqH491/ga4wtboduxm-0-Rf5-U-1-1.jpg'#'https://i.ibb.co/pbQLhks/123123-0-Rf5-U.jpg'
        prices_out = 100000
    else:
        print('Неизвестный id инвойса: ' + id_payment)
        return

    payment_data = (message.chat.id,
                    title_out,
                    description_out,
                    invoice_payload_out,
                    my_cfg.provider_token,
                    currency_out,
                    prices_out,
                    photo_url_out,
                    512,
                    512,
                    512,
                    False,
                    start_parameter_out,
                    max_tip_amount_out,
                    suggested_tip_amounts_out)


    #отправляет и сохраняет результаты
    sending.send_msg(bot              = PyBot,
                     send_mode        = 'payment_mode',
                     payment_data_out = payment_data)
