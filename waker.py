import speech_recognition
import os

r = speech_recognition.Recognizer()
with speech_recognition.Microphone()as s:
    while True:
        r.adjust_for_ambient_noise(s)
        print(".")
        audio = r.listen(s)
        print("..")
        try:
            text = r.recognize_google(audio, language="en")
            print("...")
        except:
            continue
        print(text)
        text = text.lower()
        if text == "hey jason" or text == "hay jason" or text == "hay assistant" or text == "hey assistant"or text == "jason":
            os.system("main.py")
        else:
            continue
