import subprocess
import speech_recognition as sr

def voice_processing(message, bot, lang):

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('assets/temp/voice_in.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    process = subprocess.run(['ffmpeg','-y', '-i', r'assets/temp/voice_in.ogg', r'assets/temp/voice_in.wav'])

    if lang == 'en':
        rec_lang = "en-EN"
    elif lang == 'ru':
        rec_lang = "ru-RU"

    r = sr.Recognizer()

    hellow=sr.AudioFile('assets/temp/voice_in.wav')
    with hellow as source:
        audio = r.record(source)
    try:
       s = r.recognize_google(audio, language = rec_lang)
    except Exception as e:
        print("Exception: "+str(e))

    return s