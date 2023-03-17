from pickle import FALSE
import keyboards_buttons
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib2
import telebot
import my_cfg
import requests
import xmltodict
import pandas as panda
from pytube import YouTube
import urllib.request
import re
import common_methods
from googlesearch import search as SeArCh
from urltitle import URLTitleReader
import requests
import json

def inline_mode_processed(bot, query):
    if (str(query.query)[0:3]).lower() == 'pic':
        current_query = str(query.query)[3:len(str(query.query))]
        if len(current_query)>1:
            params = {
              "engine": "yandex_images",
              "text": current_query,
              "api_key": my_cfg.serpapi_token
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
                            id = str(idx), 
                            thumb_url = thumbnail, 
                            photo_url = original, 
                            photo_width = width, 
                            photo_height = height
                        )
                        results.append(msg)
                        idx +=1
            bot.answer_inline_query(query.id, results, cache_time = 0)

    elif (str(query.query)[0:3]).lower() == 'vid':
        current_query = (str(query.query)[4:len(str(query.query))]).replace(' ','+')
        if len(current_query) > 1:
            current_query = common_methods.translit(current_query)
            results = []
            cnt = 0
            html = urllib2.urlopen("https://www.youtube.com/results?search_query=" + current_query)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            video_ids = common_methods.unique_list_from_list(video_ids)
            
            #InlineQueryResultVideo заменен на InlineQueryResultArticle
            for item in video_ids:
                cur_video_url = "https://www.youtube.com/watch?v=" + str(item)
                cur_description = ''
                cur_thumb = ''
                html = urllib2.urlopen(cur_video_url)
                html_read = str(html.read())
                start_title = html_read.index( '<title>' ) + len( '<title>' )
                end_title = html_read.index( '</title>', start_title )
                cur_title = html_read[start_title:end_title]
                
                if '"shortViewCount":{"simpleText":"' in html_read:
                    cur_thumb = 'https://img.youtube.com/vi/'+str(item)+'/1.jpg'

                    what_desc_start = '"shortViewCount":{"simpleText":"'
                    what_desc_end = '"}}'
                    idx_start_desc =  html_read.index(what_desc_start) + len(what_desc_start)
                    idx_end_desc = html_read.find(what_desc_end,idx_start_desc)
                    cur_description = html_read[idx_start_desc:idx_end_desc]

                elif '"viewCount":{"runs":[{"text":"' in html_read:
                    cur_thumb = 'https://img.youtube.com/vi/'+str(item)+'/0.jpg'

                    what_desc_start = '"viewCount":{"runs":[{"text":"'
                    what_desc_end = '"}'
                    idx_start_desc =  html_read.index(what_desc_start) + len(what_desc_start)
                    idx_end_desc = html_read.find(what_desc_end,idx_start_desc)
                    cur_description = html_read[idx_start_desc:idx_end_desc] + ' watching now'
                else:
                    print('Нераспозннанный формат видео. Текст для отладки: \n' + html_read)
                    cur_description = 'Нет описания'
                    
                MsgCont = telebot.types.InputTextMessageContent(message_text = cur_video_url, disable_web_page_preview = False)
                
                msg = telebot.types.InlineQueryResultArticle(
                    id=str(cnt),
                    title=cur_title,
                    description=cur_description,
                    input_message_content=MsgCont,
                    thumb_url = cur_thumb,
                    hide_url = True)
                
                results.append(msg)
                if cnt == 4:
                    break
                cnt += 1

            bot.answer_inline_query(query.id, results, cache_time = 0)
            
    elif (str(query.query)[0:6]).lower() == 'search':
        current_query = (str(query.query)[7:len(str(query.query))]).replace(' ','+')
        if len(current_query) > 1:
            results =[]
            url = "https://google.serper.dev/search" #https://serper.dev/playground
            
            payload = json.dumps({
              "q": current_query,
              "gl": "ru",
              "num": 20
            })
            headers = {
              'X-API-KEY': '39c2b10be47144b2074098afe32ab163e4e265a4',
              'Content-Type': 'application/json'
            }
            
            response = requests.request("POST", url, headers=headers, data=payload)
            aDict = json.loads(response.text)

            org_res = aDict['organic']

            idx = 0
            for item in org_res:

                cur_title = item['title']
                cur_message = item['link']
                cur_description = item['snippet']
                
                MsgCont = telebot.types.InputTextMessageContent( message_text = cur_message, disable_web_page_preview = False)
                
                msg = telebot.types.InlineQueryResultArticle(
                    id=str(idx),
                    title=cur_title,
                    description=cur_description,
                    input_message_content=MsgCont)
                
                results.append(msg)
                idx += 1

            bot.answer_inline_query(query.id, results, cache_time = 5)
            
    elif (str(query.query)[0:6]).lower() == 'google':
        current_query = str(query.query)[7:len(str(query.query))]
        if len(current_query) > 1:

            results = []
            current_query = urllib.parse.quote(current_query)
            url = 'https://google.gik-team.com/?q='+current_query

            result = '<a href="'+url+'">Я нашел, не благодари!</a>'

            MsgCont = telebot.types.InputTextMessageContent(message_text = result, disable_web_page_preview = True, parse_mode = 'HTML')
                
            msg = telebot.types.InlineQueryResultArticle(
                id="1",
                title='Давай я погуглю вместо тебя',
                description='Ведь это же так сложно',
                input_message_content=MsgCont,
                hide_url = True)
            
            results.append(msg)

            bot.answer_inline_query(query.id, results, cache_time = 0)