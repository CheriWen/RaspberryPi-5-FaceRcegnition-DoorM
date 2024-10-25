import os
import time
"""
voice = pyttsx3.init()

def speak(text):
    voice.say(text)
    voice.runAndWait()
"""

def speak(text):
    os.system("espeak -v en-us -s 150 '{}'".format(text))