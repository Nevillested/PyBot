from gtts import gTTS
import subprocess
import os

def convert_text_to_speech(text_in, language_in):
    myobj = gTTS(text=text_in, lang=language_in, slow=False)

    myobj.save("voice_out.mp3")
    
    process = subprocess.run(['C:/assets_data/ffmpeg','-y', '-i', r'voice_out.mp3', r'voice_out.ogg'])
    #ffmpeg -i in.mp3 -ar 48000 -vn -c:a libvorbis out.ogg
    result = os.getcwd() + r'\voice_out.ogg'
    print(result)
    return result