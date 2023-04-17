import telebot
import my_cfg
import PyBot

from telebot.types import LabeledPrice, ShippingOption

def command_pay(message, id_payment):

    #объявляем основные выходные параметры
    title_out = None
    description_out = None
    invoice_payload_out = 'Shut up and take my money!'
    currency_out = 'RUB'
    prices_out = [LabeledPrice(label='Начальная ставка!', amount=9900)]
    photo_url_out = None
    start_parameter_out = 'start_parameter_out'
    max_tip_amount_out = 100000
    suggested_tip_amounts_out = [10100, 20100, 30100, 50100]

    if id_payment == "payment_one_btn":
        title_out = 'owner = one love'
        description_out = 'Потому что я такой хорошенький'
        photo_url_out = 'https://i.ibb.co/H7Zv0qp/1.jpg'
    elif id_payment == "payment_two_btn":
        title_out = 'Денег нет, но ты держись'
        description_out = 'Не помирай плз, держи 150р'
        photo_url_out = 'https://i.ibb.co/DrR4mpk/2.jpg'
    elif id_payment == "payment_three_btn":
        title_out = 'Бот - это святое'
        description_out = 'Ты только представь свою жизнь без этого бота. Ага, и я о том же, расчехляй кошель'
        photo_url_out = 'https://i.ibb.co/6v1DT1d/3.jpg'
    elif id_payment == "payment_shinobu":
        title_out = 'ka-ka'
        description_out = 'Шинобу - лучшая девочка, ты это понимаешь?\nПоэтому давай, расчехляй свой кошель и без лишних вопросов скидывайся на кошерные фигурки.\nВсе скидываются, и ты скидывайся, давай, не ломайся\n(тут могла быть ваша пассивно-агрессивная реклама)'
        photo_url_out = 'https://i.ibb.co/pbQLhks/123123-0-Rf5-U.jpg'
        max_tip_amount_out = 1000000
        suggested_tip_amounts_out = [10100, 50100, 100100, 500100]

    PyBot.MypyBot.send_invoice(chat_id               = message.chat.id,
                               title                 = title_out,
                               description           = description_out,
                               invoice_payload       = invoice_payload_out,
                               provider_token        = my_cfg.provider_token,
                               currency              = currency_out,
                               prices                = prices_out,
                               photo_url             = photo_url_out,
                               photo_height          = 512,
                               photo_width           = 512,
                               photo_size            = 512,
                               is_flexible           = False,
                               start_parameter       = start_parameter_out,
                               max_tip_amount        = max_tip_amount_out,
                               suggested_tip_amounts = suggested_tip_amounts_out)
"""
@PyBot.MypyBot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    PyBot.MypyBot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Ооох, кажется у курьерского собакена сейчас обед, попробуй позже.')


@PyBot.MypyBot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    PyBot.MypyBot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Ты не поверишь, пришельцы пытались украсть твой CVV-код, но я отбился. Сейчас я отдохну пару мин, а ты затем попробуй еще разок.")


@PyBot.MypyBot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    PyBot.MypyBot.send_message(message.chat.id,
                     'Атлы, все прошло успешно. Сейчас мы обработаем платеж `{} {}` настолько быстро насколько это вообще в принципе возможно.\nОставайтесь с нами и спасибо за покупку!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')"""
