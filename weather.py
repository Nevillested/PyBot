from geopandas.tools import geocode
import common_methods
import requests
import json
import my_cfg

#получает долготу и широту по месту
def get_coordinates(place):
    location = geocode(place, provider="nominatim" , user_agent = 'my_request')
    point = location.geometry.iloc[0]
    return point.y, point.x

#выдает погоду на текущее время
def current_weather(cur_data):
    
    api_key = my_cfg.weather_token
    latitude = ''
    longitude = ''
    if cur_data.content_type == 'text':
        latitude, longitude = get_coordinates(cur_data.text)
    else:
        latitude = cur_data.location.latitude
        longitude = cur_data.location.longitude

    address = f'https://api.openweathermap.org/data/2.5/weather?lat={str(latitude)}&lon={str(longitude)}&lang=ru&appid={api_key}'
    x = requests.get(address)
    
    response = json.loads(str(x.json()).replace('[','').replace(']','').replace('\'', '\"'))
    
    new_dict = {}
    for item in response:
        if item in ['weather', 'main', 'wind', 'sys']:
            new_dict[item] = response[item]
    
    weather_description  = str(new_dict['weather']['description'])
    
    main_temp            = str(round((int(new_dict['main']['temp']) - 273.15),2)) + '°'
    main_feels_like      = str(round((int(new_dict['main']['feels_like']) - 273.15),2))+ '°'
    main_temp_min        = str(round((int(new_dict['main']['temp_min']) - 273.15),2))+ '°'
    main_temp_max        = str(round((int(new_dict['main']['temp_max']) - 273.15),2))+ '°'
    main_pressure        = str(round((float(new_dict['main']['pressure']) * 0.75006375541921), 0)) + ' мм.рт.ст.'
    wind_speed           = str(new_dict['wind']['speed']) + ' м/с'

    
    result = 'На небе: ' + weather_description + '.'
    result = result + '\nТемпература: ' + main_temp + '. Ощущается как ' + main_feels_like + '. Минимальная ' + main_temp_min + '. Максимальная ' + main_temp_max + '. Давление ' + main_pressure + '.'
    result = result + '\nВетер: ' + wind_speed + '.'

    return result

#выдает погоду на определенный день - НЕ РАБОТАЕТ И НЕ ДОДЕЛАНО, ПОТОМУ ЧТО https://openweathermap.org/ ЕБУЧИЕ ЖЛОБЫ
def certain_day_weather(day, place):
    
    api_key = my_cfg.weather_token
    list_chars_coord = {'1234567890.; '}
    latitude = ''
    longitude = ''

    result_check = 0 #по умолчанию сделаем, что результат проверки это уже имеющиеся координаты

    for c in place:
        for r in list_chars_coord:
            if c != r:
                #если во время прогонки в строки, полученной из бд, нашлись символы, которых нет в list_chars_coord, 
                #то строка, которую проверяем - это место, написанное текстом, а не имеющиеся координаты
                result_check = -1 
                break

    if result_check == -1 :
        latitude, longitude = get_coordinates(place)
    else:
        x = place.split(";")
        latitude = x[0]
        longitude = x[1]
        
    print(str(latitude))
    print(str(longitude))
    
    address = f'https://api.openweathermap.org/data/2.5/forecast/daily?lat={str(latitude)}&lon={str(longitude)}&cnt=7&appid={api_key}'
    #address = f'https://api.openweathermap.org/data/2.5/weather?lat={str(latitude)}&lon={str(longitude)}&exclude=hourly,daily&appid={api_key}'
    x = requests.get(address)
    
    response = json.loads(str(x.json()).replace('[','').replace(']','').replace('\'', '\"'))
    print(str(response))
    
    #new_dict = {}
    #for item in response:
    #    if item in ['weather', 'main', 'wind', 'sys']:
    #        new_dict[item] = response[item]
    
    #weather_main         = common_methods.translate_en_to_ru(str(new_dict['weather']['main']))
    #weather_description  = common_methods.translate_en_to_ru(str(new_dict['weather']['description']))
    #main_temp            = str(round((int(new_dict['main']['temp']) - 273.15),2)) + '°'
    #main_feels_like      = str(round((int(new_dict['main']['feels_like']) - 273.15),2))+ '°'
    #main_temp_min        = str(round((int(new_dict['main']['temp_min']) - 273.15),2))+ '°'
    #main_temp_max        = str(round((int(new_dict['main']['temp_max']) - 273.15),2))+ '°'
    #main_pressure        = str(round((float(new_dict['main']['pressure']) * 0.75006375541921), 0)) + ' мм.рт.ст.'
    #wind_speed           = str(new_dict['wind']['speed']) + ' м/с'

    
    #result = 'На небе: ' + weather_main + ', ' + weather_description + '.'
    #result = result + '\nТемпература: ' + main_temp + '. Ощущается как ' + main_feels_like + '. Минимальная ' + main_temp_min + '. Максимальная ' + main_temp_max + '. Давление ' + main_pressure + '.'
    #result = result + '\nВетер: ' + wind_speed + '.'

    return 'сори'