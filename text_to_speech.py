from gtts import gTTS
import subprocess
import os

def convert_text_to_speech(text_in, language_in):

    myobj = gTTS(text=text_in, lang=language_in, slow=False)

    myobj.save("voice_out.ogg")

    result = os.getcwd() + r'\voice_out.ogg'
    return result