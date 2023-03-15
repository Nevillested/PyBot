import keyboards_buttons
from serpapi import GoogleSearch
import telebot
import cfg

def inline_mode_processed(bot, query):
    params = {
      "engine": "yandex_images",
      "text": query.query,
      "api_key": cfg.serpapi_token
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results.get('images_results')
    results = []
    idx = 0
    for item in images_results:
        if str(item.get('original').__contains__('.jpg')) or str(item.get('original').__contains__('.jpeg')):
            sizes = item.get('size')
            width = sizes.get('width')
            height = sizes.get('height')
            byte_size = sizes.get('bytes')
            thumbnail = item.get('thumbnail')
            original = item.get('original')
            if byte_size < 5242880:
                msg = telebot.types.InlineQueryResultPhoto(
                    id = str(idx), thumb_url = thumbnail, photo_url = original, photo_width = width, photo_height = height
                )
                results.append(msg)
                idx +=1

    bot.answer_inline_query(query.id, results)