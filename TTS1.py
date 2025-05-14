
# HELLO THIS IS A FEMALE TEXT TO SPEECH CONVERTER............

import win32com.client
# import speech_recognition as sr 

speaker=win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate=0.50
speaker.Volume=100

def say(text):
    speaker.Speak(text)



    
     
