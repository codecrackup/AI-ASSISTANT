
#HELLO THIS A TEXT TO MALE SPEECH CONVERTER .........

import win32com.client

def say(text):
    voice=win32com.client.Dispatch("SAPI.SpVoice")

    voices=voice.GetVoices()

    for i,v in enumerate(voices):

        voice.Voice=voices[1]
    voice.Speak(text)




