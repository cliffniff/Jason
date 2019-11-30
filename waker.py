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
        if text == "hey alpha" or text == "hay alpha" or text == "hay assistant" or text == "hey assistant"or text == "alpha":
            os.system("main.py")
        else:
            continue
