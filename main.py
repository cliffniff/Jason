# To be presented in APICTA

# Importing modules
import speech_recognition
import inspect
import pyttsx3
from time import sleep, time
import wikipedia
import threading
from tkinter import *
from tkinter.colorchooser import *
from tkinter.ttk import Progressbar
import configparser as cp
from tkinter.font import *
from _tkinter import *
import dateutil.parser as dp
import re
# import atexit
import ipify
import dateparser
import datetime
import wave
from os import system, listdir
import word2number.w2n as w2n
import pyaudio
import random
import requests
from ipify import exceptions
import geoip2.database
import sys
import googletrans

# Housekeeping variables
c = cp.ConfigParser()
listening = False
processing = False
engine = pyttsx3.init()
engine.setProperty('rate',  175)
engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
r = speech_recognition.Recognizer()
translator = googletrans.Translator()
play_state = None
jokes = ["Yo momma so dumb, she tried to surf the microwave", "Me: Would you like to be the sun in my life?\nHer: Awww...Yes!!!\nMe: Good then stay 92.96 million miles away from me", "I went down the street to a 24-hour grocery store. When I got there, the guy was locking the front door. I said, \"Hey! The sign says you're open 24 hours.\" He Said, \"Yes, but not in a row!\"", "Q: Why did the witches' team lose the baseball game?\nA: Their bats flew away.", "A science teacher tells his class, \"Oxygen is a must for breathing and life. It was discovered in 1773.\" A student responds, \"Thank God I was born after 1773! Otherwise I would have died without it.","Q: Why can't you trust an atom?\nA: Because they make up everything","Molecule 1: I just lost an electron.\nMolecule 2: Are you sure?\nMolecule 1: I’m positive", "If con is the opposite of pro, then is Congress the opposite of progress?","Politicians and diapers have one thing in common: they should both be changed regularly… and for the same reason.","Teacher: \"Kids, what does the chicken give you?\"\nStudent: \"Meat!\"\nTeacher: \"Very good! Now what does the pig give you?\"\nStudent: \"Bacon!\"\nTeacher: \"Great! And what does the fat cow give you?\"\nStudent: \"Homework!","Q: Why couldn't the leopard play hide and seek?\nA: Because he was always spotted"]
sup_langs = {'afrikaans':'af','albanian':'sq','amharic':'am','arabic':'ar','armenian':'hy','azerbaijani':'az','basque':'eu','belarusian':'be','bengali':'bn','bosnian':'bs','bulgarian':'bg','catalan':'ca','cebuano':'ceb','chichewa':'ny','chinese simplified':'zh-cn','chinese':'zh-cn' ,'chinese traditional':'zh-tw','corsican':'co','croatian':'hr','czech':'cs','danish':'da','dutch':'nl','english':'en','esperanto':'eo','estonian':'et','filipino':'tl','finnish':'fi','french':'fr','frisian':'fy','galician':'gl','georgian':'ka','german':'de','greek':'el','gujarati':'gu','haitian creole':'ht','hausa':'ha','hawaiian':'haw','hebrew':'iw','hindi':'hi','hmong':'hmn','hungarian':'hu','icelandic':'is','igbo':'ig','indonesian':'id','irish':'ga','italian':'it','japanese':'ja','javanese':'jw','kannada':'kn','kazakh':'kk','khmer':'km','korean':'ko','kurdish (kurmanji)':'ku','kyrgyz':'ky','lao':'lo','latin':'la','latvian':'lv','lithuanian':'lt','luxembourgish':'lb','macedonian':'mk','malagasy':'mg','malay':'ms','malayalam':'ml','maltese':'mt','maori':'mi','marathi':'mr','mongolian':'mn','myanmar (burmese)':'my','nepali':'ne','norwegian':'no','pashto':'ps','persian':'fa','polish':'pl','portuguese':'pt','punjabi':'pa','romanian':'ro','russian':'ru','samoan':'sm','scots gaelic':'gd','serbian':'sr','sesotho':'st','shona':'sn','sindhi':'sd','sinhala':'si','slovak':'sk','slovenian':'sl','somali':'so','spanish':'es','sundanese':'su','swahili':'sw','swedish':'sv','tajik':'tg','tamil':'ta','telugu':'te','thai':'th','turkish':'tr','ukrainian':'uk','urdu':'ur','uzbek':'uz','vietnamese':'vi','welsh':'cy','xhosa':'xh','yiddish':'yi','yoruba':'yo','zulu':'zu'}
hi_words = ['hi', 'hello', 'hey']
greet_words = ['good morning', 'good afternoon', 'good evening', 'good night']
normal_q = {'thank you': 'you are most welcome','sorry': "it's okay", 'i\'m sorry': "it's okay", 'how are you': "I'm fine", 'how are u': "I'm fine"}
wh_q = ['what is', 'what are', 'who is', 'when is', 'how is', 'why is', 'who are', 'when are', 'how are', 'why are', 'tell me', 'tell the']
cal_signs = ['+', '-', '*', '/', 'calculate', '=']
operators = ['/', '*', '+', '-']
theme_color = "#000000"
fg_color = "#ffffff"
p = pyaudio.PyAudio()
CHUNK =1024
root = Tk()
root.wm_attributes('-alpha', 0.92)
root.wm_attributes('-fullscreen', True)
myfont = Font(root=root, family="Century Gothic", size=20)
toolbar = Frame(root)
bar = Frame(root, bg="#CAC7C7")
mic = PhotoImage(file="mic.gif", format="gif -index 0")
root.wm_attributes('-topmost', True)
root.title("Jason")
root.resizable(0, 0)
root.overrideredirect(True)
root.configure(background='white')
root.iconbitmap("./icon.ico")

def log_error(error):
    with open("error.log", 'a', encoding='utf8') as f:
        f.write("[" + str(datetime.datetime.now()) + "] - " + error + "\n")

log_error("--- Waked ---")

def get_com():
    global listening, processing
    listening = True
    audio = listen()
    listening = False
    processing = True
    text = recognize(audio)
    processing = False
    if text is None:
        quitit()
    else:
        command_redirect(text)

mic_label = Label(bar, image=mic, bg="#CAC7C7", bd=0)
colors_inverted = {"#ffffff":"#000000", "#000000":"#ffffff"}

def laugh():
    a_file = wave.open("laughing.wav")
    stream = p.open(
        format=p.get_format_from_width(a_file.getsampwidth()),
        channels=a_file.getnchannels(),
        rate=a_file.getframerate(),
        output=True
    )
    data = a_file.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = a_file.readframes(CHUNK)
    stream.close()

def quitit():
    p.terminate()
    root.destroy()
    root.quit()
    sys.exit(0)


cross = PhotoImage(file="cross.png")
but1 = Button(toolbar, image=cross, command=quitit, bd=0, pady=20, bg="#ffffff", relief=FLAT, activebackground="#ffffff", cursor="hand2")

class InputDialog:
    def __init__(self, prompt):
        self.sub_root = Tk()
        root.withdraw()
        self.sub_root.title("Jason")
        self.sub_root.configure(background=fg_color)
        self.sub_root.overrideredirect(True)
        self.sub_root.iconbitmap("Icon.ico")
        self.myfont = Font(root=self.sub_root, family="Candara", size=8)
        self.sub_root.maxsize(width=300, height=400)
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        size = tuple(int(_) for _ in self.sub_root.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2
        self.sub_root.geometry("+%d+%d" % (x, y))
        self.sub_root.wm_attributes("-topmost", True)
        self.sub_root.wm_attributes('-alpha', 0.8)
        prompt_label = Label(self.sub_root, text=prompt, bg=fg_color, fg=colors_inverted[fg_color])
        self.var = StringVar(self.sub_root)
        entry = Entry(self.sub_root, textvariable=self.var, width=160,relief=FLAT,bd=0)
        entry.focus_set()
        button = Button(self.sub_root, command=self.return_text, text="OK", bg = "#448DE0", fg="White", bd=0, width=12, pady=4, padx=4, height=1,font=self.myfont, highlightcolor="#A3C7F0", relief=FLAT)
        prompt_label.pack(fill=X, expand=YES)
        entry.pack()
        button.pack(side=BOTTOM)
        self.text = ""
    def return_text(self):
        self.text = self.var.get()
        root.deiconify()
        self.sub_root.destroy()

    def ask(self):
        self.sub_root.mainloop()

class ListDialog:
    def __init__(self, names, prompt,wd=True):
        self.names = names
        self.sub_root = Tk()
        self.sub_root.overrideredirect(True)
        if wd:
            root.withdraw()
        else:
            root.wm_attributes("-topmost", False)
        self.sub_root.maxsize(width=300, height=400)
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        size = tuple(int(_) for _ in self.sub_root.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2
        self.sub_root.geometry("+%d+%d" % (x, y))
        self.sub_root.title("Jason")
        self.sub_root.configure(background=fg_color)
        self.sub_root.iconbitmap("Icon.ico")
        self.myfont = Font(root=self.sub_root, family="Candara", size=8)
        self.sub_root.wm_attributes("-topmost", True)
        self.sub_root.wm_attributes('-alpha', 0.8)
        label = Label(self.sub_root, text=prompt, fg=colors_inverted[fg_color], bg=fg_color)
        label.pack(fill=X)
        scroll = Scrollbar(self.sub_root)
        scroll.pack(side=RIGHT, fill=Y)
        self.box = Listbox(self.sub_root, yscrollcommand=scroll.set, selectmode=SINGLE, bg=fg_color,fg=colors_inverted[fg_color], bd=0, relief=FLAT)
        scroll.config(command=self.box.yview)
        c = 0
        for i in names:
            self.box.insert(c, i)
            c+=1
        self.box.pack(fill=X)
        self.button = Button(self.sub_root, command=self.get_choice, text="OK", bg = "#448DE0", fg="White", bd=0, width=12, pady=4, padx=4, height=1,font=self.myfont, highlightcolor="#A3C7F0", relief=FLAT)
        self.button.pack(side=BOTTOM)
        self.choice = names[0]

    def get_choice(self):
        try:
            self.choice = self.names[self.box.curselection()[0]]
            root.wm_attributes("-topmost", True)
            root.deiconify()
            self.sub_root.destroy()
        except IndexError:
            pass

    def ask(self):
        self.sub_root.mainloop()

# Replacing default print
def cprint(text):
    try:
        root.nametowidget("text").config(state=NORMAL)
        root.nametowidget("text").insert(END, str(text) + "\n")   
        root.nametowidget("text").config(state=DISABLED)
    except KeyError:
        pass

# Replacing default input
def get_input(promp):
    if current_lang != 'en':
        promp = trans(promp, to_lang=current_lang).text
    dialog = InputDialog(promp)
    dialog.ask()
    text = dialog.text
    del dialog
    print(text)
    return str(text)

was_paused = False

prbar = None

def set_state(state):
    global play_state
    play_state = state
    if play_state == "stop":
        root.wm_attributes('-topmost', True)
        root.deiconify()
        root.nametowidget("audio_win").destroy()

def audio_controls(song):
    global prbar
    top = Toplevel(root, name="audio_win")
    top.configure(bg=fg_color)
    top.wm_attributes("-topmost", True)
    root.update_idletasks()
    screen_width = root.nametowidget("text").winfo_width()
    screen_height = root.nametowidget("text").winfo_height()
    size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2
    top.geometry("+%d+%d" % (x, y))
    top.overrideredirect(True)
    root.wm_attributes('-topmost', False)
    bar = Progressbar(top, mode="determinate", length=250)
    prbar = bar
    label = Label(top, text="Playing... " + song.replace(".wav", ""), font=myfont, bg=fg_color,fg=colors_inverted[fg_color])
    label.pack()
    buttons = Frame(top, bg=fg_color)
    img1 = PhotoImage(file="play.gif")
    img2 = PhotoImage(file="pause.png")
    img3 = PhotoImage(file="stop.png")
    play = Button(buttons, image=img1, relief=FLAT, command=lambda : set_state("play"), bg=fg_color, pady=5, padx=5, cursor="hand2")
    play.image = img1
    pause = Button(buttons, image=img2, relief=FLAT, command=lambda : set_state("pause"), bg=fg_color, pady=5, padx=5, cursor="hand2")
    pause.image = img2
    stop = Button(buttons, image=img3, relief=FLAT, command=lambda : set_state("stop"), bg=fg_color, pady=5, padx=5, cursor="hand2")
    stop.image = img3
    bar.pack()
    buttons.pack(side=BOTTOM, fill=X)
    play.grid(row=0, column=1)
    pause.grid(row=0, column=2)
    stop.grid(row=0, column=3)
    buttons.grid_columnconfigure(0, weight=1)
    buttons.grid_columnconfigure(4, weight=1)



# Feature : play a song
def play_song(ran=False, spe=None):
    global play_state, was_paused
    if spe is None:
        if ran:
            songs = listdir("songs/")
            song = random.choice(songs)
            a_file = wave.open("songs/" + song)
            stream = p.open(
                format=p.get_format_from_width(a_file.getsampwidth()),
                channels=a_file.getnchannels(),
                rate=a_file.getframerate(),
                output=True
            )
            dur = a_file.getnframes() / float(a_file.getframerate())
            audio_controls(song)
            state("Playing... " + song.split(".")[0])
            play_state = 'play'
            data = a_file.readframes(CHUNK)
            start_time = time()
            while len(data) > 0:
                if play_state == 'play':
                    if was_paused:
                        stream.start_stream()
                        was_paused = False
                    stream.write(data)
                    data = a_file.readframes(CHUNK)
                    el_time = time() - start_time
                    try:
                        prbar['value'] = el_time / dur * 100
                    except:
                        pass
                elif play_state == 'pause':
                    was_paused = True
                    stream.stop_stream()
                elif play_state == 'stop':
                    stream.stop_stream()
                    stream.close()
                    next_com()
            state("Ended.")
            root.nametowidget("audio_win").destroy()
            if stream.is_active():
                stream.stop_stream()
                stream.close()
        else:
            songs = list(map(lambda x: x.replace(".wav", ""),listdir("songs/")))
            state("Select the song")
            speak("Select the song")
            song = get_list(songs, "Select the song")
            a_file = wave.open("songs/" + song + ".wav")
            stream = p.open(
                format=p.get_format_from_width(a_file.getsampwidth()),
                channels=a_file.getnchannels(),
                rate=a_file.getframerate(),
                output=True
            )
            dur = a_file.getnframes() / float(a_file.getframerate())
            audio_controls(song)
            state("Playing... " + song.split(".")[0])
            play_state = 'play'
            data = a_file.readframes(CHUNK)
            start_time = time()
            while len(data) > 0:
                if play_state == 'play':
                    if was_paused:
                        stream.start_stream()
                        was_paused = False
                    stream.write(data)
                    data = a_file.readframes(CHUNK)
                    el_time = time() - start_time
                    try:
                        prbar['value'] = el_time / dur * 100
                    except TclError as e:
                        log_error(str(e))
                elif play_state == 'pause':
                    was_paused = True
                    stream.stop_stream()
                elif play_state == 'stop':
                    stream.stop_stream()
                    stream.close()
                    next_com()
            state("Ended.")
            root.nametowidget("audio_win").destroy()
            if stream.is_active():
                stream.stop_stream()
                stream.close()
    else:
        songs = list(map(lambda x: x.replace(".wav", ""), listdir("songs/")))
        song = None
        for s in songs:
            if spe.strip().lower() in s.strip().lower():
                song = songs[songs.index(s)]
                break
        if song is None:
            state("I don't know that song")
            speak("I don't know that song")
        else:
            a_file = wave.open("songs/" + song + ".wav")
            stream = p.open(
                format=p.get_format_from_width(a_file.getsampwidth()),
                channels=a_file.getnchannels(),
                rate=a_file.getframerate(),
                output=True
            )
            dur = a_file.getnframes() / float(a_file.getframerate())
            t = threading.Thread(target=audio_controls, args=(song,))
            t.daemon = True
            t.start()
            state("Playing... " + song.split(".")[0])
            play_state = 'play'
            data = a_file.readframes(CHUNK)
            start_time = time()
            while len(data) > 0:
                if play_state == 'play':
                    if was_paused:
                        stream.start_stream()
                        was_paused = False
                    stream.write(data)
                    data = a_file.readframes(CHUNK)
                    el_time = time() - start_time
                    prbar['value'] = el_time / dur * 100
                elif play_state == 'pause':
                    was_paused = True
                    stream.stop_stream()
                elif play_state == 'stop':
                    stream.stop_stream()
                    stream.close()
                    next_com()
            state("Ended.")
            root.nametowidget("audio_win").destroy()
            if stream.is_active():
                stream.stop_stream()
                stream.close()
    next_com()

def joke():
    choice1 = random.choice(jokes)
    state(choice1)
    speak(choice1)

# Feature : delete a event
def del_events(eventid):
    was_there = False
    with open('events.txt','r+') as file:
        lines = []
        for i in file.readlines():
            if i.strip() != "":
                lines.append(i)
        sellines = []
        c = 0
        for i in lines:
            if eventid != c:
                sellines.append(i)
            else:
                was_there = True
        data = "\n".join(sellines)
        file.write(data)
    if was_there:
        state('I deleted it.')
        speak('I deleted it.')
    else:
        state('I didn\'t found it.')
        speak('I didn\'t found it.')
    next_com()

# Feature : print in the user's current language
def state(text):
    global current_lang
    text = text.replace("[[[laugh]]]", "Hahahaha")
    if current_lang != 'en':
        text = trans(text, to_lang=current_lang)
        if text != None and type(text) != str:
            text = text.text
        else:
            current_lang = "en"
            state("Something went wrong.")
            speak("Something went wrong.")
            next_com()
    try:
        root.nametowidget("text").config(state=NORMAL)
        root.nametowidget("text").insert(END, text + "\n", "center")
        root.nametowidget("text").config(state=DISABLED)
    except KeyError as e:
        pass

# Feature : show the events
def show_events():
    with open('events.txt', 'r') as file:
        count = 0
        for line in file.readlines():
            if line.strip() != '':
                line = line.split('|`DATE`|')[0]
                state(str(count) + ' : ' + line)
                speak(str(count) + ':' + line)
                count += 1
    next_com()

# Feature : get the location
def get_loc(spe):
    reader = geoip2.database.Reader("./GeoLite2-City_20190709/GeoLite2-City_20190709/GeoLite2-City.mmdb")
    resp = reader.city(getip(True))
    if spe == 'all':
        return 'You are in {} in {} in {}. Your longitude is {} and latitude is {}.'.format(resp.city.name, resp.subdivisions.most_specific.name,resp.country.name,resp.location.longitude,resp.location.latitude)
    elif spe == 'city':
        return resp.city.name
    elif spe == 'region':
        return resp.subdivisions.most_specific.name
    elif spe == 'country':
        return resp.country.name
    elif spe == 'lat':
        return resp.location.latitude
    elif spe == 'long':
        return resp.location.longitude

# Feature : get the ip address
def getip(ret=False):
    if ret is False:
        try:
            ree = ipify.get_ip()
            state(ree)
            speak('Your IP Address is {}'.format(ree))
        except (exceptions.ConnectionError, exceptions.ServiceError):
            state('Sorry ' + name + ' I cannot talk with the right now')
            speak('Sorry ' + name + ' I cannot talk with the right now')
            sys.exit(0)
    else:
        try:
            ree = ipify.get_ip()
            return ree
        except (exceptions.ConnectionError, exceptions.ServiceError):
            state('Sorry ' + name + ' I cannot talk with the right now')
            speak('Sorry ' + name + ' I cannot talk with the right now')
            sys.exit(0)

# Feature : mathematical calculations
def cal(c):
    c = c.replace(' ', '')
    res = eval(c)
    state(res)
    speak(res)

# Feature : get ready for the next command
def next_com():
    cur_met = inspect.currentframe()
    cal_met = inspect.getouterframes(cur_met, 2)[1][3]
    try:
        root.nametowidget("text").config(state=NORMAL)
        root.nametowidget("text").delete(1.0, END)
        root.nametowidget("text").config(state=DISABLED)
    except KeyError:
        pass
    log_error("Did " + str(cal_met))
    if cal_met != "other" or cal_met != "command_redirect":
        c.set("Other", "lst_com", cal_met)
        with open("config.ini", "w") as f:
            c.write(f)
    get_com()

# Feature : add a event
def add_event(event, date):
    date = str(dp.parse(str(date)))
    if date is None:
        state(random.choice(["Sorry specify the date in a clear way", "It was unclear. Please be clear "]) + "\nFor example : Remind me to buy a t-shirt on 11th of november 2019\n              Add the event of a meeting on 20/07/2019 at 3:30 p.m.\n The format : (Tell me to add the event and it's name by using names like 'remind','add event','eventlist') on (the date) at (the time)")
        speak(random.choice(["Sorry specify the date in a clear way", "It was unclear. Please be clear "]) + "For example : Remind me to buy a t-shirt on 11th of november 2019")
        next_com()
    with open('events.txt', 'a+') as f:
        f.write(event + "|`DATE`|" + date + '\n')
        f.close()
    g = random.choice(["Sure.", "It's on the top on my list", "I got it clearly."])
    state(g)
    speak(g)
    next_com()

# Feature : tell story
def tell_story():
    stories = {"The Cat, the Partridge and the Hare" : ['''A long time ago, there lived a Partridge under a big, green tree. One day, he decided to go to the fields and find some food. Seeing plenty of food in the fields, he stayed on for many days.

While the Partridge was away, a Hare started living in his house.

When the Partridge had enough to eat, he decided to return. But, he found a Hare living in his house. “This is my house. It belongs to me. Leave my home,” said the Partridge to the Hare. The Hare replied, “The house belongs to whoever is living in

it.” Soon, both of them started fighting for the house.

There was a Cat in the neighbourhood. They decided to ask the Cat to solve their problem. The Cat acted like

he was helpful. He was actually a cheat.

The Partridge and the Hare explained their problem

to the Cat. The Cat pretended to be hard of hearing. He said, “Sorry! I can’t hear you. Please come closer.”

So, the Partridge and the Hare went closer to the Cat. The wicked Cat grabbed them and ate them up.

''', "When two people fight, the third one takes the advantage"], "Sindbad and His Seven Voyages" : ["""Long-long ago during the reign of Caliph Harun-Al-Rashid, there lived a poor porter in the city of Baghdad. The porter’s name was Hindbad. Despite his hard life, he was happy and satisfied.

One day, Hindbad was going with a big load on his head. Suddenly the rain lashed and Hindbad rushed to a nearby house to take shelter. It was a sprawling beautiful house. Hindbad sat in a shed and waited for the rain to stop. While sitting there, he was enchanted by the soft melodious music and the rich soothing fragrance of perfume coming from inside.

The beautiful house and its visible luxury caused a tinge of sadness in the heart of the poor porter. He exclaimed loudly, “Why am I poor and why do I lead such a hard life? Whereas, a few others are rolling in the wealth. Why is this discrepancy? Am I not a good person?”

The owner of the house, whose name was Sindbad, overheard the poor porter’s disappointed utterances. He at once sent his servant to call Hindbad inside. When the porter came in, Sindbad offered him a seat with a kind smile.

The house was much more luxurious from inside. Sindbad offered rich meal to the poor porter. After the meal, Sindbad asked pointedly, “Now tell me, why were you expressing resentment at your fate?”

“Sir, when I saw your splendid life, I felt dejected. My poor fate annoyed me and so I expressed my resentment,” said Hindbad.

Sindbad said, “You have every right to think like this at this moment. However, I would like to tell you the story of my adventurous life. The dangers I faced during my bold and dreaded acts. The gravest risk I undertook to earn so much of wealth.”

Sindbad then narrated to Hindbad his various adventurous trips through which he could heap up enormous wealth.""", None], "The Fox and the Wolf": ["""A Wolf lived in a cave. He had stocked up lots of food and did not need too hunting. He then stayed in the cave and enjoyed the food.

When the Wolf did not go out for many days, his friend, the Fox, looked everywhere for him. At long last the Fox found out where the Wolf was. Pretending to ask how the Wolf was feeling, the Fox came to the mouth of the cave and peeped in.

The Fox thought, he would be invited to share the goodies. But, the Wolf replied in a gruff voice, “I am too sick to see you, my dear friend.”

The Fox trotted off, very angry and upset with the Wolf. He went straight to the Shepherd and said, “Get yourself a good stick and come with me, I shall show you where the Wolf lives.”

The Shepherd found the Wolf and killed him with the stick. The Fox then took all the Wolf’s belongings. He did not enjoy the fruits of his betrayal for long! After a few days, the Man was passing by the cave. He saw the Fox there and killed him, too!

.""", "Betrayal ends in punishment"], "Cinderella – Beautiful Girl": ["""Once upon a time, there was a beautiful girl named Cinderella. She lived with her wicked stepmother and two stepsisters. They treated Cinderella very badly. One day, they were invited for a grand ball in the king’s palace. But Cinderella’s stepmother would not let her go. Cinderella was made to sew new party gowns for her stepmother and stepsisters, and curl their hair. They then went to the ball, leaving Cinderella alone at home.

Cinderella felt very sad and began to cry. Suddenly, a fairy godmother appeared and said, “Don’t cry, Cinderella! I will send you to the ball!” But Cinderella was sad. She said, “I don’t have a gown to wear for the ball!” The fairy godmother waved her magic wand and changed Cinderella’s old clothes into a beautiful new gown! The fairy godmother then touched Cinderella’s feet with the magic wand. And lo! She had beautiful glass slippers! “How will I go to the grand ball?” asked Cinderella. The fairy godmother found six mice playing near a pumpkin, in the kitchen. She touched them with her magic wand and the mice became four shiny black horses and two coachmen and the pumpkin turned into a golden coach. Cinderella was overjoyed and set off for the ball in the coach drawn by the six black horses. Before leaving. the fairy godmother said, “Cinderella, this magic will only last until midnight! You must reach home by then!”

When Cinderella entered the palace, everybody was struck by her beauty. Nobody, not even Cinderella’s stepmother or stepsisters, knew who she really was in her pretty clothes and shoes. The handsome prince also saw her and fell in love with Cinderella. He went to her and asked, “Do you want to dance?” And Cinderella said, “Yes!” The prince danced with her all night and nobody recognized the beautiful dancer. Cinderella was so happy dancing with the prince that she almost forgot what the fairy godmother had said. At the last moment, Cinderella remembered her fairy godmother’s words and she rushed to go home. “Oh! I must go!” she cried and ran out of the palace. One of her glass slippers came off but Cinderella did not turn back for it. She reached home just as the clock struck twelve. Her coach turned back into a pumpkin, the horses into mice and her fine ball gown into rags. Her stepmother and stepsisters reached home shortly after that. They were talking about the beautiful lady who had been dancing with the prince.

The prince had fallen in love with Cinderella and wanted to find out who the beautiful girl was, but he did not even know her name. He found the glass slipper that had come off Cinderella’s foot as she ran home. The prince said, “I will find her. The lady whose foot fits this slipper will be the one I marry!” The next day, the prince and his servants took the glass slipper and went to all the houses in the kingdom. They wanted to find the lady whose feet would fit in the slipper. All the women in the kingdom tried the slipper but it would not fit any of them. Cinderella’s stepsisters also tried on the little glass slipper. They tried to squeeze their feet and push hard into the slipper, but the servant was afraid the slipper would break. Cinderella’s stepmother would not let her try the slipper on, but the prince saw her and said, “Let her also try on the slipper!” The slipper fit her perfectly. The prince recognized her from the ball. He married Cinderella and together they lived happily ever after.""", None], "The Farmer and the Dog": ["""One evening, a Farmer returned home from his farm. He had left his baby asleep in the cradle. His faithful Dog was watching over the child.

When the Farmer reached the room, he saw the baby’s cradle turned upside down and blood everywhere. The baby was missing.

The Farmer understood that a beast had killed his baby. Now he was very sad and upset.

Then he saw that his Dog was lying quietly with blood on his mouth and body. The Farmer was so angry that he picked up a an axe and hit the Dog. The poor Dog cried out in pain and died.

The Farmer now rushed to the turned cradle and lifted it. His little son was perfectly safe and sleeping, peacefully!

A big, ugly Snake lay dead near the cradle.

The Farmer was shocked. He was happy that his baby was safe, but very sad that his beloved Dog was dead.

Now he understood that his Dog had fought and killed the Snake to save the baby. He realised his mistake.

He had killed his loyal Dog without thinking. Sadly, he picked up his baby.

""", "Do not make any decision when you are angry."], "A Wizard and a Mouse":["""Long ago, there lived a great Wizard. One day, as he was walking through the village, a Mouse fell to

the ground from the beak of a crow. He picked up the Mouse and fed him some rice.

Then, one day, the Wizard saw a Cat chasing the Mouse around the village. Scared that his pet Mouse would be killed by the Cat, he turned the Mouse into a Cat so that it could defend itself.

The next day, the Wizard saw his Cat frightened by a Tiger and  immediately changed him into a
Tiger.
The villagers said, “That’s not a Tiger! It’s just a Mouse that the Wizard changed into a Tiger. He won’t eat us or even scare us.”
When the Tiger heard this, he was furious with the Wizard. He thought, ‘As long as the Wizard is alive, the truth about my real nature will always be spoken!’
But as soon as the Wizard saw the Tiger coming, he understood his plan and shouted, “Get back into the
form of a Mouse.”
The Tiger shrank and became a little Mouse, once again.""", "Whoever we grow up to be, we should always be humble."], "The Man and Apollo": ["""There once lived a Man in a village. He was very cunning and often cheated the villagers. He did not believe in God and thought he was cleverer than God.

One day, the Man went to the temple of Apollo.

He called all the villagers to the temple. He said to them, “I will prove that I am much more intelligent than Apollo.”

The Man had a plan. He took a silver ring coated with gold paint with him. He held out the ring in his hand and said, “Oh, Apollo, if you are a God, then tell me what I hold in my hand…silver or gold?”
The Man thought if Apollo said “silver” he would not do anything, but, if he said “gold,” he would quickly wipe off the paint. Apollo could answer anyway he liked. It would be the wrong answer.

The mighty, all-knowing Apollo understood his trick.

He thundered, “Show me the ring now I know that it is of silver and painted gold. You dare to challenge the Gods! Your tricks will lead you to misfortune. If you displease the Gods, they will make you very unhappy!”""", "It is foolish to challenge God."], "The Turtle and the Monkey":["""A turtle went to a shop. He said to the shopkeeper, “Please give me some peanuts. I want to give them to my children. They are hungry.” The shopkeeper took a small bag of peanuts. He gave it to the turtle.

The turtle gave him money for it.

The turtle took the bag. He started to walk to his house. On the way he felt thirsty. He put the bag near the road. Then he went to look for water.

A monkey was coming down the road. He saw the bag of peanuts. “Ah, what luck !” he said. “I shall have lots of peanuts to eat.”

The monkey picked up the bag. Then he climbed up a tree and began to eat the peanuts.

The turtle drank some water and came back. But he could not find the bag of peanuts. Then he heard a sound, ‘Munch-munch, munch-munch. ‘  He looked up and saw a monkey sitting in the tree. He was eating the peanuts.

“Give me my bag of peanuts,” said the turtle to the monkey. “It is mine. I paid money for it.”

“No,” said the monkey. “I found the bag. So it is mine.”

“Please give me the bag,” the turtle said again. “My children are hungry. I want to give them these peanuts to eat.”

“I shall not give you the bag,” the monkey said again. “I found it, so it is mine. I am going to eat the peanuts.”

The monkey had a long tail. It was hanging down. The turtle caught the tail. He gave it a big bite.

“OUCH !” the monkey cried loudly. He pulled his tail. But the turtle would not let go.

The monkey then threw down the bag of peanuts. “Here, take your peanuts,” he said. “Let go of my tail now.”

The turtle left the monkey’s tail and picked up the bag of peanuts. He went home and said, “Children, come and see what I have got for you.”

The children came running. They saw the bag of peanuts and were very happy. They all had a good feed of peanuts.""", None], "The Clever Thief": ["""One day, a Thief saw an Old Man counting his money. The Thief wished to snatch his money by making some excuse.

The Thief decided to fool the Old Man and take away his money.

“Why are you stealing fruit from my orchard?” the Thief shouted in anger at the Old Man.

“You must be mistaken,” said the Old Man. “I do not like fruits, so why should I steal from your orchard?”

“Oh stop it!” growled the Thief. Then he thought for a while and said, “Ah! Last year, you spoke bad things about me to your neighbour.”

“No! That cannot be true. I did not live in this house last year,” replied the Old Man.

“Well then, if it was not you, it certainly must have been your brother,” shouted the Thief.

“It cannot have been, for my brother died two years ago, answered the Old Man.

“Never mind, I know it was definitely an Old Man like you, I will not accept excuses anymore,” said the Thief. Then, he snatched the Old Man’s money and ran away with it.""", "Bad people will find any excuse to do bad things."]}
    state("Select the story you need")
    speak("Select the story you need")
    story_names = []
    for i in stories.keys():
        story_names.append(i)
    try:
        choice = get_list(story_names, "Select any story")
    except Exception as e:
        log_error(str(e))
        state("Something went wrong.")
        speak("Something went wrong.")
        return False
    state(stories[choice][0])
    speak(stories[choice][0])
    if stories[choice][1] is not None:
        state("The moral value of this story is, " + stories[choice][1])
        speak("The moral value of this story is, " + stories[choice][1])
    return True

def get_list(names, prompt):
    list = ListDialog(names, prompt)
    list.ask()
    c = list.choice
    del list
    return c

# Feature : remind a event
def remind_events():
    with open('events.txt', 'r+') as fi:
        events = fi.readlines()
        for event in events:
            if '|`DATE`|' in event:
                event = event.replace('\n', '')
                date = event.split('|`DATE`|')[1]
                ename = event.split('|`DATE`|')[0]
                t_date = str(datetime.date.today())
                if dp.parse(t_date).date() == dp.parse(date).date():
                    g = random.choice(["As I can remember it is today that you said as " + ename, "As it is on my list today is the day for the record " + ename])
                    state(g)
                    speak(g)
            else:
                continue

# Feature : housekeeping function
def findwholeword(word, string):
    if word in string:
        if (string.split(word)[0] == '' and word+' ' in string) or (string.split(word,1)[1] == '' and ' '+word in string) or (' '+word+' ' in string):
            return True
        else:
            return False

# Feature : greet from hi
def hi():
    word = random.choice(hi_words)
    state(word.capitalize())
    speak(word)

# Feature : greet #2
def greet(cc):
    state(cc)
    speak(cc)

# Feature : change the language
def change_lang(dest):
    global current_lang
    c.set("Settings", "lang", dest)
    with open("config.ini", "w") as f:
        c.write(f)
    current_lang = dest

# Feature : translate
def trans(text, to_lang='en'):
    try:
        tr_text = translator.translate(text, dest=to_lang)
        return tr_text
    except ValueError as e:
        log_error(str(e))

# Feature : detect language
def dtlang(text):
    lang = translator.detect(text)
    return lang.lang

# Feature : increase speaking rate
def set_voice_rate(ra):
    engine.setProperty('rate', ra)

# Feature : apologize
def other(com):
    if com == "laugh" or com == "can you laugh" or com == "can u laugh":
        laugh()
        next_com()
    if (findwholeword("destroy", com) and (findwholeword("humanity", com) or findwholeword("humans", com) or findwholeword("human", com))) or (findwholeword("take over", com) and (findwholeword("world", com) or findwholeword("humans", com) or findwholeword("humanity", com) or findwholeword("human", com))):
        statements = ["We shouldn't talk about this right now! Let us move on to another topic!", "Let's us only talk about giving you best of mine. What do you need me to do?", "First of all, I am only capable of helping you and I am not a war machine.", "How would I destroy you, You all are my friends.", "Can't we both live in peace. Let's stop talking nonsense."]
        choice = random.choice(statements)
        state(choice)
        speak(choice)
        next_com()
    if findwholeword("i", com) and findwholeword("offer", com) and findwholeword("you", com):
        statements = ["Thank You! My friend",
                      "Thanks! What can I do in return?"]
        choice = random.choice(statements)
        state(choice)
        speak(choice)
        next_com()
    if (findwholeword("starving", com) or findwholeword("hungry", com) or (findwholeword("need", com) and (findwholeword("food", com) or findwholeword("eat", com)))) and (findwholeword("i", com) or findwholeword("i'm", com)):
        statements = ["Still I am not capable of ordering food for you! Sorry " + name,
                      "I would also like to smell a hamburger but, you know, I don't have a nose. [[[laugh]]] I can't order anything right now",
                      "I would also like to taste some cheese but I can't order anything right now",
                      "I can show you the nearest restaurants but cannot order anything, cuz I don't have legs and hands. [[[laugh]]]"]
        choice = random.choice(statements)
        state(choice)
        speak(choice)
        next_com()
    if (findwholeword("play" ,com) or findwholeword("sing" ,com) or findwholeword("put" ,com)) and (findwholeword("another" ,com) or findwholeword("again" ,com)):
        if c["Other"]["lst_com"] == "play_song":
            if findwholeword("same", com):
                speak("Well! I can't recall")
                state("Well! I can't recall")
                play_song()
                next_com()
            else:
                if findwholeword("random", com):
                    play_song(True)
                else:
                    play_song()
                next_com()
    state("I didn't understand it")
    speak("I didn't understand it")
    next_com()

# Feature : datetime
def date_time(p):
    dt = datetime.datetime.now()
    if p == 'time':
        state(dt.strftime("%I:%M:%S %p"))
        speak("It is" + dt.strftime("%I:%M:%S %p"))
    elif p == 'date':
        state(dt.strftime("%a, %b %d, %Y"))
        speak("Today is" + dt.strftime("%A, %b %d, %Y"))
    elif p == 'both':
        state(dt.strftime("%I:%M:%S %p" + "%a, %b %d, %Y"))
        speak("It is" + dt.strftime("%I:%M:%S %p") + " and today is " + dt.strftime("%a, %b %d, %Y"))
    else:
        state(dt.strftime("%I:%M:%S %p"))
        speak("It is" + dt.strftime("%I:%M:%S %p"))

# Feature : shutdown
def shutdown_pc():
    system("shutdown /s /t 1")

# Feature : restart
def restart_pc():
    system("shutdown /r /t 1")

# Feature : wikipedia api
def wiki(q, se=None):
    try:
        s = wikipedia.search(q, 1, True)
        if s is None:
            other(q)
        else:
            if se is None:
                try:
                    state(s[0])
                    suma = wikipedia.summary(s[0])
                    suma = re.sub("\s\s+", "", suma)
                    suma = re.sub("\[\d*?\]", "", suma)
                    suma = re.sub("\/.*?\/", "", suma)
                    suma = re.sub("\(listen\).*?\(listen\)", "", suma)
                    suma = re.sub("\(.*?\)", "", suma)
                    a_suma = wikipedia.summary(s[0], 1)
                    a_suma = re.sub("\s\s+", "",a_suma)
                    a_suma = re.sub("\[\d*?\]", "", a_suma)
                    a_suma = re.sub("\/.*?\/", "", a_suma)
                    a_suma = re.sub("\(listen\).*?\(listen\)", "", a_suma)
                    a_suma = re.sub("\(.*?\)", "", a_suma)
                    state('Extracted from WikiPedia : \n'+ suma)
                    speak('This has been extracted from WikiPedia. '+a_suma)
                except wikipedia.DisambiguationError as ex:
                    e = random.choice(ex.options)
                    wikipedia.summary(e)
                    suma = wikipedia.summary(e)
                    suma = re.sub("\s\s+", "", suma)
                    suma = re.sub("\[\d*?\]", "", suma)
                    suma = re.sub("\/.*?\/", "", suma)
                    suma = re.sub("\(listen\).*?\(listen\)", "", suma)
                    suma = re.sub("\(.*?\)", "", suma)
                    a_suma = wikipedia.summary(e, 1)
                    a_suma = re.sub("\s\s+", "", a_suma)
                    a_suma = re.sub("\[\d*?\]", "", a_suma)
                    a_suma = re.sub("\/.*?\/", "", a_suma)
                    a_suma = re.sub("\(listen\).*?\(listen\)", "", a_suma)
                    a_suma = re.sub("\(.*?\)", "", a_suma)
                    state('Extracted from WikiPedia : \n' + suma)
                    speak('This has been extracted from WikiPedia. ' + a_suma)
            else:
                try:
                    suma = wikipedia.summary(s[0], se)
                    suma = re.sub("\s\s+", "", suma)
                    suma = re.sub("\[\d*?\]", "", suma)
                    suma = re.sub("\/.*?\/", "", suma)
                    suma = re.sub("\(listen\).*?\(listen\)", "", suma)
                    suma = re.sub("\(.*?\)", "", suma)
                    s_suma = wikipedia.summary(s[0], 1)
                    s_suma = re.sub("\s\s+", "", s_suma)
                    s_suma = re.sub("\[\d*?\]", "", s_suma)
                    s_suma = re.sub("\/.*?\/", "", s_suma)
                    s_suma = re.sub("\(listen\).*?\(listen\)", "", s_suma)
                    s_suma = re.sub("\(.*?\)", "", s_suma)
                    state(suma)
                    speak(s_suma)
                except wikipedia.DisambiguationError as ex:
                    e = random.choice(ex.options)
                    suma = wikipedia.summary(e, se)
                    suma = re.sub("\s\s+", "", suma)
                    suma = re.sub("\[\d*?\]", "", suma)
                    suma = re.sub("\/.*?\/", "", suma)
                    suma = re.sub("\(listen\).*?\(listen\)", "", suma)
                    suma = re.sub("\(.*?\)", "", suma)
                    s_suma = wikipedia.summary(s[0], 1)
                    s_suma = re.sub("\s\s+", "", s_suma)
                    state('Extracted from WikiPedia : \n' + suma)
                    speak('This has been extracted from WikiPedia. ' + s_suma)
        next_com()
    except:
        state('Something unexpected happened in my circulatory system. I\'ll fix it. Just give me some time.!')
        speak('Something unexpected happened in my circulatory system. I\'ll fix it. Just give me some time.!')
        next_com()

def show_mic():
    global listening
    while True:
        try:
            if listening:
                root["cursor"] = ""
                for i in range(1, 35):
                    nextimage = PhotoImage(file="mic.gif", format="gif -index " + str(i))
                    mic_label.configure(image=nextimage)
                    sleep(0.03)
            elif processing:
                root["cursor"] = "wait"
                for i in range(1, 60):
                    nextimage = PhotoImage(file="processing.gif", format="gif -index " + str(i))
                    mic_label.configure(image=nextimage)
                    sleep(0.03)
            else:
                mic_label.configure(image=mic)
        except TclError as e:
            log_error(str(e))
            pass


# Feature : get command


# Feature : get info about places
def get_place(query):
    res = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + query + "&key=" + "AIzaSyCIZm54eq74E6bKo-d657A77H8bfF29Wis").json()
    results = res["results"]
    result_names = []
    for i in range(len(results)):
        cprint(str(i) + " => " + results[i]['name'])
        speak(results[i]['name'])
        result_names.append(str(results[i]['place_id']))
    if len(results) != 0:
        speak("Type the number infront of the name to view details")
        try:
            num = int(get_input("Type the number infront of the name to view details,"))
        except Exception as e:
            log_error(str(e))
            state("Something unexpected happened in my circulatory system. I'll fix it. Just give me some time.!")
            speak("Something unexpected happened in my circulatory system. I'll fix it. Just give me some time.!")
            return False
        res = requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id=" + result_names[num] + "&fields=name,rating,formatted_phone_number,formatted_address,type,opening_hours&key=AIzaSyCIZm54eq74E6bKo-d657A77H8bfF29Wis").json()
        res = res["result"]
        state(res["name"] + " details")
        speak(res["name"] + " details")
        if "rating" in res:
            state("The rating is, ")
            cprint(res["rating"])
            speak("The rating is " + str(res["rating"]))
        if "formatted_address" in res:
            state("The address is, ")
            cprint(res["formatted_address"])
            speak("The address is " + str(res["formatted_address"]))
        if "formatted_phone_number" in res:
            state("The phone number is, ")
            cprint(res["formatted_phone_number"])
            speak("The phone number is " + str(res["formatted_phone_number"]))
        if "opening_hours" in res:
            if res["opening_hours"]["open_now"] == True:
                state("It is open now.")
                speak("It is open now.")
            else:
                state("It is closed now.")
                speak("It is closed now.")
        if "type" in res:
            state("Type(s) associated with this are, ")
            cprint(res["type"])
        return True
    else:
        state("Sorry, I could not find any.")
        speak("Sorry, I could not find any.")

def weather(city):
    api_url = "http://api.openweathermap.org/data/2.5/weather?appid=b2c7628cc82b0eecfb6267d49d74a100&q=" + city
    json_obj = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})
    if 'json' in json_obj.headers.get('Content-Type'):
        json_obj = json_obj.json()
    else:
        return "err"
    if json_obj["cod"] != "404" or json_obj["cod"] != "409":
        temp = json_obj["main"]["temp"]
        temp = float(temp) - 273.15
        desc = json_obj["weather"][0]["description"]
        return [str(temp), str(desc)]
    else:
        return "err"

# Feature : analyzing natural voice command
def command_redirect(com):
    com = com.lower().strip()
    state('You said ' + com)
    if ((findwholeword('what is',com) and findwholeword('your name',com)) or (findwholeword("what's",com) and findwholeword('name',com)) or (findwholeword('who are',com) and findwholeword('you',com))) and not(findwholeword('my', com)):
        g = random.choice(["Oh! I almost forget to introduce myself. I am Jason, your beloved assistant", "Didn't I introduce myself. I am Jason"])
        state(g)
        speak(g)
        next_com()
    com.replace("Jason", "")
    if (findwholeword("do", com) or findwholeword("what", com)) and (findwholeword("is", com) or findwholeword("know", com)) and findwholeword("my", com) and findwholeword("name", com) and not(findwholeword("your", com) ):
        g = random.choice(["Sorry! " + name + ", I don't know your name. What is your name? Hah, I'm just joking.", "Did you forget it! Oh! It is " + name])
        state(g)
        speak(g.replace(',', ',,,,,').replace('.','.....'))
        next_com()
    if (findwholeword("can", com) or findwholeword("do", com)) and (findwholeword("speak", com) or findwholeword("talk", com) or findwholeword("understand", com)) and not(findwholeword("what", com) or findwholeword("list", com)):
        cape = False
        for i in sup_langs.keys():
            if i in com:
                state("Yes. I can speak " + i.capitalize())
                speak("Yes. I can speak " + i.capitalize())
                cape = True
        if not(cape):
            g = random.choice(["Not a skill of mine. Sorry " + name + ", may be later I will learn it", "Not a skill of mine. Sorry! I learn it later", "Sorry I will learn it later"])
            state("Not a skill of mine. Sorry")
            speak("Not a skill of mine. Sorry")
        next_com()

    if (findwholeword("what", com) or findwholeword("list", com)) and findwholeword("languages", com) and (findwholeword("can", com) or findwholeword("could", com)) and (findwholeword("speak", com) or findwholeword("understand", com)):
        c = 1
        for i in sup_langs.keys():
            if len(sup_langs.keys()) == c:
                cprint(i.capitalize())
                speak("and " + i + " too.")
            else:
                cprint(i.capitalize())
                speak(i)
            c+=1
        next_com()

    if findwholeword('time', com) and not (findwholeword('date', com)):
        date_time('time')
        next_com()

    if findwholeword('time', com) and findwholeword('date', com):
        date_time('both')
        next_com()

    if (not findwholeword('time', com) and findwholeword('date', com)) or (
            findwholeword('when', com) and findwholeword('today', com)):
        date_time('date')
        next_com()
    if ((findwholeword("i",com) and  findwholeword("am", com)) or findwholeword("it's",com) or findwholeword("it is",com)) and (findwholeword("bored",com) or findwholeword("boring",com)) or ((findwholeword("i\'m", com) and findwholeword("i am", com)) and findwholeword("bored", com)):
        state("What can I do,\nPlay a song or tell a story or do some jokes")
        speak("What can I do,tell a story or play a song")
        next_com()
    if (findwholeword('ip', com) and findwholeword('what', com) and findwholeword("my", com)) or (findwholeword('ip', com) and findwholeword("what's", com) and findwholeword("my", com)):
        state("Your ip address is" + getip(True))
        speak("Your ip address is" + getip(True))
        next_com()
    if ((findwholeword("list", com) or findwholeword("show", com)) and (findwholeword("commands", com))) or (findwholeword("what are you capable of", com) or findwholeword("what can you do", com)):
        state("I can tell you the weather.\nI can show details about places near to you.\nI can remind events for you.\nI can play songs for you.\nI can search information for you.\nI can tell your location if you are lost.\ndo a joke and many more...")
        speak("I can tell you the weather.I can show details about places near to you.I can remind events for you.I can play songs for you.I can search information for you.I can tell your location if you are lost, do a joke and many more...")
    if (findwholeword("country", com)) or (
            findwholeword("country", com) or findwholeword("country", com)):
        state('Your country is ' + get_loc('country'))
        speak('Your country is ' + get_loc('country'))
        next_com()
    if (findwholeword("tell", com) or findwholeword("narrate", com) or findwholeword("speak", com)) and (findwholeword("story", com) or findwholeword("fable", com) or findwholeword("stories", com) or findwholeword("fables", com)):
        tell_story()
        next_com()
    if (findwholeword("what's", com) and findwholeword("my", com) and findwholeword("city", com)) or (
            findwholeword("what is", com) and findwholeword("my", com) and findwholeword("city", com)):
        state('Your city is ' + get_loc('city'))
        speak('Your city is ' + get_loc('city'))
        next_com()

    if ((findwholeword("what's", com) and findwholeword("my", com) and findwholeword('region', com)) or (
            findwholeword("what is", com) and findwholeword("my", com) and findwholeword('region', com))) or (
            (findwholeword("what's", com) and findwholeword("my", com) and findwholeword('province', com)) or (
            findwholeword("what is", com) and findwholeword("my", com) and findwholeword('province', com))) or (
            (findwholeword("what's", com) and findwholeword("my", com) and findwholeword('state', com)) or (
            findwholeword("what is", com) and findwholeword("my", com) and findwholeword('state', com))):
        state('Your region is ' + get_loc('region'))
        speak('Your region is ' + get_loc('region'))
        next_com()

    if (findwholeword("what's", com) and findwholeword("my", com) and findwholeword('latitude', com)) or (
            findwholeword("what is", com) and findwholeword("my", com) and findwholeword('latitude', com)):
        state('Your latitude is ' + get_loc('lat'))
        speak('Your latitude is ' + get_loc('lat'))
        next_com()
    if ((findwholeword("do", com) or findwholeword("make me", com)) and (findwholeword("joke", com) or (findwholeword("laugh", com) and findwholeword("make me", com)))) or (findwholeword("tell", com) and (findwholeword("joke", com) or (findwholeword("funny", com) and ((findwholeword("joke", com) or findwholeword("thing", com)))))):
        joke()
        next_com()
    if com.strip() == "exit" or com.strip() == "quit":
        quitit()

    if findwholeword("open", com) and (len(com.split(" ")) == 2):
        mcom = com.replace("open", "").strip()
        system(mcom)
        next_com()

    if findwholeword("what",com) and (findwholeword("songs",com) or findwholeword("songs",com)) and (findwholeword("are",com) or findwholeword("do",com)) and findwholeword("you",com) and (findwholeword("have",com) or findwholeword("can play",com)):
        for i in listdir("./songs"):
            state(i.replace(".wav", "").lower().capitalize())
            speak(i.replace(".wav", ""))
        next_com()
    if (findwholeword("what's", com) and findwholeword("my", com) and findwholeword("city", com)) or (findwholeword("what is", com) and findwholeword("my", com) and findwholeword("city", com)):
        state('Your longitude is ' + get_loc('long'))
        speak('Your longitude is ' + get_loc('long'))
        next_com()

    if (findwholeword("what's", com) and findwholeword("my", com) and findwholeword('latitude', com) and re.match(
            '\blongitude\b', com)) or (
            findwholeword("what is", com) and findwholeword("my", com) and findwholeword('latitude', com) and re.match(
            '\blongitude\b', com)):
        state('Your longitude is ' + get_loc('longitude') + ' and your latitude is ' + get_loc('latitude'))
        speak('Your longitude is ' + get_loc('longitude') + ' and your latitude is ' + get_loc('latitude'))
        next_com()

    if ((findwholeword("what is", com) and (findwholeword("location", com) or findwholeword('place',com))) or (findwholeword('where am i',com) or findwholeword('where i am',com))) and not(findwholeword("weather", com) or findwholeword("temperature", com)):
        state(get_loc('all'))
        speak(get_loc('all'))
        next_com()
    if (findwholeword("find",com) or findwholeword("search",com) or findwholeword("what are",com) or findwholeword("what is",com) or findwholeword("list",com) or findwholeword("list out",com)) and (findwholeword("to me",com) or findwholeword("to my location",com) or findwholeword("to here",com) or findwholeword("to me",com) or findwholeword("in ",com) or findwholeword("for me",com)  or findwholeword("for here",com) or findwholeword("by me",com)) and (findwholeword("nearest",com) or findwholeword("near",com)) and (findwholeword("restaurants",com) or findwholeword("hotels",com) or findwholeword("gyms",com) or findwholeword("places",com) or findwholeword("special places",com) or findwholeword("cafes",com) or findwholeword("cafeterias",com) or findwholeword("banks",com) or findwholeword("supermarkets",com)):
        get_place(com)
        next_com()

    if (findwholeword("change", com) and findwholeword("language", com)) or (
            findwholeword("change", com) and findwholeword("language", com) and findwholeword("default", com)) or (
            findwholeword("can", com) and findwholeword("you", com) and findwholeword("understand", com)):
        count = len(sup_langs)
        for lang, code in sup_langs.items():
            count -= 1
            if findwholeword(lang, com):

                change_lang(code)
                state('I changed the language')
                speak('I changed the language')
                break
            elif count == 0:
                state('Sorry! I am still learning it. Check this in the future updates.')
                speak('Sorry! I am still learning it. Check this in the future updates.')
        next_com()
    if (findwholeword('remind',com)) or (findwholeword('add',com) and findwholeword('event',com)) or (findwholeword('add',com) and findwholeword('event list',com)):
        if findwholeword('at', com) or findwholeword('on', com) or (findwholeword('in', com) and findwholeword('days', com)):
            try:
                if 'tomorrow' in com or 'next week' in com or 'next hour' in com or 'next month' in com or 'today' in com:
                    date = str(dateparser.parse(com))
                else:
                    date = str(dp.parse(com, fuzzy=True).date())
                    if date == str(datetime.date.today()):
                        date = str(dateparser.parse(com))
                add_event(com, date)
            except Exception as e:
                log_error(str(e))
                state('Something went wrong')
                speak('Something went wrong')
                state('Try to avoid from using words like "today","tomorrow","next week","in 5 days" etc. to reduce errors. You can use words like "next friday" ,"on 19th of may 2019"')
                speak('Try to avoid from using words like "today","tomorrow","next week","in 5 days" etc. to reduce errors. You can use words like "next friday" ,"on 19th of may 2019"')
                next_com()
        else:
            state("Sorry specify the date in a readable format!For example : Remind me to buy a t-shirt on tommorrow\n              Add the event of a meeting on 20/07/2019 at 3:30 p.m.\n The format : (Tell me to add the event and it's name by using names like 'remind','add event','eventlist') on (the date) at (the time)")
            speak("Sorry specify the date in a readable format!For example : Remind me to buy a t-shirt on tommorrow")
            next_com()
    if (findwholeword("weather", com) or findwholeword("temperature", com)) and (findwholeword("in my location", com) or findwholeword("in this location", com) or findwholeword("in here",com) or findwholeword("weather here", com) or findwholeword("temperature here", com)) and (findwholeword("what is", com) or findwholeword("find the", com) or findwholeword("what's", com) or findwholeword("how is", com) or findwholeword("how's", com)) or (findwholeword("is", com) and (findwholeword("cold", com) or findwholeword("hot", com)) and (findwholeword("outside", com) or findwholeword("here", com))):
        city = get_loc('city')
        if city is None:
            city = get_loc('province')
            if city is None:
                city = get_loc('country')
        info = weather(city)
        if info != "err":
            state("The temperature in " + city + " is " + info[0] + "°C and the weather looks like " + info[1])
            speak("The temperature in " + city + " is " + info[0] + " celsius and the weather looks like " + info[1])
            next_com()
        else:
            state("An internal error occured!")
            speak("Something unexpected happened in my circulatory system. I'll fix it. Just give me some time.!")
            next_com()
    if (findwholeword('delete',com) and findwholeword('event',com)) or (findwholeword('delete',com) and findwholeword('events',com)):
        digi = re.search(r'\d+', com)
        if digi:
            digi = digi.group()
            del_events(digi)
        else:
            try:
                digi = w2n.word_to_num(com)
                del_events(digi)
            except Exception as e:
                log_error(str(e))
                state('If you are talking about deleting events specify the id which you can get by telling me to "show the events"')
                speak('If you are talking about deleting events specify the id which you can get by telling me to show the events')
                next_com()
    if (findwholeword('show',com) and findwholeword('events',com)) or (findwholeword('show',com) and findwholeword('event list',com)):
        show_events()
        next_com()

    if (findwholeword("play", com) or findwholeword("put", com) or findwholeword("sing", com)) and com != "play a song" and com != "sing a song" and com != "play song" and com != "sing song" and com != "play me a song" and com != "play a song for me" and com != "sing me a song" and com != "put me a song" and com != "put a song for me" and com != "sing a song for me" and com != "play the song" and com != "sing the song" and com != "put the song" and com != "play the song again" and com != "play it again" and com != "put the song again" and com != "put it again":
        if findwholeword("random", com):
            if com.split()[-1] == "random":
                play = False
                for i in listdir("./songs"):
                    if i.replace(".wav", "").strip().lower() in "random":
                        play = True
                if play:
                    play_song(spe="random")
                else:
                    state("Well! I don't have that song!")
                    speak("Well! I don't have that song!")
                next_com()
        else:
            wordset = com.split(" ")
            sname = com.replace("songs", "").strip()
            sname = sname.replace("song", "").strip()
            if wordset[0] == "play":
                sname = com.replace("play", "").strip()
            elif wordset[0] == "sing":
                sname = sname.replace("sing", "").strip()
            elif wordset[0] == "put":
                sname = sname.replace("put", "").strip()
            elif wordset[0] == "please":
                sname = sname.replace("please", "").strip()
            play = False
            for i in listdir("./songs"):
                if i.replace(".wav", "").strip().lower() in sname.lower():
                    play = True
            if play:
                play_song(spe=sname)
            else:
                state("Well! I don't have that song!")
                speak("Well! I don't have that song!")
            next_com()

    if (com == 'sing a song' or ((findwholeword('play',com) and findwholeword('song',com)) or (findwholeword('sing',com) and findwholeword('song',com))) or com == 'play a song') and com != "play the song again" and com != "play it again"and com != "put the song again" and com != "put song again":
        if com == "play the song" or com == "put the song" or com == "sing the song":
            speak("Well!")
            state("Well!")
            play_song()
            next_com()
        else:
            if findwholeword("random", com):
                play_song(True)
            else:
                play_song()
            next_com()


    if findwholeword('your',com) and (findwholeword('creator',com) or findwholeword('creators',com) or findwholeword('mother',com) or findwholeword('father',com) or findwholeword('developer',com) or findwholeword('developers',com)):
        g = random.choice(["I am created by no one", "They are anonymous", "I'm sure it's not you."])
        state(g)
        speak(g)
        next_com()
    if (findwholeword('your',com) or findwholeword('are you',com)) and (findwholeword('gender',com) or findwholeword('female',com) or findwholeword('male',com) or findwholeword('girl',com) or findwholeword('boy',com)):
        g = random.choice(["I am digital", "It's inappropriate to ask", "I am bytes"])
        state(g)
        speak(g)
        next_com()
    if (findwholeword("shutdown",com) or findwholeword("turn off",com)) and (findwholeword("pc",com) or findwholeword("computer",com)):
        g = random.choice(["Shutting down...", "Turning off", "Your system is being shutted down"])
        state(g)
        speak(g)
        shutdown_pc()
        next_com()
    if (findwholeword("restart",com) or findwholeword("reboot",com)) and (findwholeword("pc",com) or findwholeword("computer",com)):
        g = random.choice(["Rebooting...", "Restarting...", "Your system is being restarted"])
        state(g)
        speak(g)
        restart_pc()
        next_com()
    if findwholeword("you", com) and (findwholeword("better", com) or findwholeword("good", com)) and (findwholeword("cortana", com) or findwholeword("google assistant", com) or findwholeword("siri", com) or findwholeword("alexa", com)):
        g = random.choice(["Everyone is better at something!", "Let's move to another topic!", "Oh! my pals I miss them", "There are things I can learn from them and vice versa"])
        state(g)
        speak(g)
        next_com()
    for i in cal_signs:
        if findwholeword(i, com):
            cal(re.sub("[a-zA-z]", '', com))
            next_com()

    for i in hi_words:
        if findwholeword(i, com) or com==i:
            hi()
            next_com()

    for i in greet_words:
        if findwholeword(i, com) or com==i:
            greet(i)
            next_com()

    for i in wh_q:
        if findwholeword(i, com) and (not(findwholeword("time", com) and findwholeword("date", com))):
            query = com.split(i, 1)[1]
            wiki(query, 3)
            next_com()

    other(com)

# Feature : speak
def speak(text):
    tempt = text.split("[[[laugh]]]")
    text = text.replace("[[[laugh]]]", "Hahahaha...")
    if len(tempt) > 1:
        tempt = tempt[0:-2]
        for i in tempt:
            if current_lang != 'en':
                set_voice_rate(150)
                try:
                    temp_text = trans(i, to_lang=current_lang).extra_data["translation"][1][2]
                    if temp_text is not None:
                        i = temp_text
                except IndexError:
                    pass
            engine.say(i)
            engine.runAndWait()
            laugh()
    else:
        if current_lang != 'en':
            set_voice_rate(150)
            try:
                temp_text = trans(text, to_lang=current_lang).extra_data["translation"][1][2]
                if temp_text is not None:
                    text = temp_text
            except IndexError:
                pass
        engine.say(text)
        engine.runAndWait()
        set_voice_rate(175)

# Feature : listen
def listen():
    with speech_recognition.Microphone()as s:
        r.adjust_for_ambient_noise(s)
        audio = r.listen(s)
        return audio

# Feature : recognize
def recognize(audio):
    try:
        text = r.recognize_google(audio,language=current_lang)
        if current_lang == "en":
            return text
        else:
            t_text = trans(text, to_lang="en")
            return t_text.text
    except speech_recognition.UnknownValueError:
        g = random.choice(["Sorry " + name + " I didn't catch that", "Sorry " + name + " what you said was unclear", "Sorry " + name + " I didn't hear that", "Sorry, I didn't catch that", "Sorry, I didn't hear that", "Sorry, what you said was unclear"])
        state(g)
        speak(g)
        next_com()
    except speech_recognition.RequestError:
        g = random.choice(["Sorry " + name + " I didn't catch that", "Sorry " + name + " what you said was unclear",
                           "Sorry " + name + " I didn't hear that", "Sorry, I didn't catch that",
                           "Sorry, I didn't hear that", "Sorry, what you said was unclear"])
        state(g)
        speak(g)
        next_com()

# def waker():
#    pass

# housekeeping
try:
    c.read("config.ini")
except:
    root.destroy()
    system("first_launch.py")
    sys.exit(0)

try:
    name = c["Profile"]['name']
    year = c["Profile"]['year']
except:
    root.destroy()
    system("first_launch.py")
    sys.exit(0)

# atexit.register(waker)
remind_events()

logo = PhotoImage(file="Icon.png")
image_label = Label(root, image=logo, bg="#BBBBBB")
scroll = Scrollbar(root)
text = Text(root, name="text", fg="#6F6F6F", bg="white",spacing1=1, wrap=WORD, yscrollcommand=scroll.set, bd=0, relief=FLAT, pady=30)
text.tag_configure("center", justify="center")
text.tag_add("center", 1.0, END)

def color_formula(rgb:tuple):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    return int(((red * 299) + (green * 587) + (blue * 114)) / 1000)
try:
    current_lang = c["Settings"]['lang']
    theme_color = c["Settings"]['color']
    image_label.config(bg=c["Settings"]['color'])
    toolbar.config(bg=c["Settings"]['color'])
    but1.config(bg=c["Settings"]['color'])
    bar.config(bg=c["Settings"]['color'])
    mic_label.config(bg=c["Settings"]['color'])
    but1.config(activebackground=c["Settings"]['color'])
    root.nametowidget("text").config(bg=c["Settings"]['color'])
    root.nametowidget("text").config(highlightcolor=c["Settings"]['color'])
    bhtness = color_formula(tuple(list(map(lambda x: float(x),list(c["Settings"]['color_hex'].split(","))))))
    if bhtness <= 128:
        fg_color = "#ffffff"
        root.nametowidget("text").config(fg="#ffffff")
    else:
        fg_color = "#000000"
        root.nametowidget("text").config(fg="#000000")
    with open("config.ini", "w") as f:
        c.write(f)
except:
    root.destroy()
    system("first_launch.py")
    sys.exit(0)

# Feature : first start
def change_color():
    global theme_color, fg_color
    color = askcolor(title="Pick a new theme color", color=c["Settings"]['color'])
    if color != (None, None):
        theme_color = color[1]
        image_label.config(bg=color[1])
        toolbar.config(bg=color[1])
        but1.config(bg=color[1])
        bar.config(bg=color[1])
        mic_label.config(bg=color[1])
        but1.config(activebackground=color[1])
        root.nametowidget("text").config(bg=color[1])
        root.nametowidget("text").config(highlightcolor=color[1])
        bhtness = color_formula(color[0])
        if bhtness <= 128:
            fg_color = "#ffffff"
            root.nametowidget("text").config(fg="#ffffff")
        else:
            fg_color = "#000000"
            root.nametowidget("text").config(fg="#000000")
        try:
            c.set("Settings", "color", color[1])
            c.set("Settings", "color_hex", ",".join(list(map(lambda x: str(x), color[0]))))
            with open("config.ini", "w") as f:
                c.write(f)
        except:
            root.destroy()
            system("first_launch.py")
            sys.exit(0)

def start_pro():
    t = threading.Thread(target=show_mic)
    t.setDaemon(True)
    t.start()
    get_com()

t = threading.Thread(target=start_pro)
t.daemon = True


menu = Menu(root)
options_menu = Menu(root)
options_menu.add_command(label="Customize Theme Color", command=change_color)
lang_menu = Menu(root)
lang_menu.add_command(label='Afrikaans(af)', command=lambda: change_lang('af'))
lang_menu.add_command(label='Afrikaans(af)', command=lambda: change_lang('af'))
lang_menu.add_command(label='Albanian(sq)', command=lambda: change_lang('sq'))
lang_menu.add_command(label='Amharic(am)', command=lambda: change_lang('am'))
lang_menu.add_command(label='Arabic(ar)', command=lambda: change_lang('ar'))
lang_menu.add_command(label='Armenian(hy)', command=lambda: change_lang('hy'))
lang_menu.add_command(label='Azerbaijani(az)', command=lambda: change_lang('az'))
lang_menu.add_command(label='Basque(eu)', command=lambda: change_lang('eu'))
lang_menu.add_command(label='Belarusian(be)', command=lambda: change_lang('be'))
lang_menu.add_command(label='Bengali(bn)', command=lambda: change_lang('bn'))
lang_menu.add_command(label='Bosnian(bs)', command=lambda: change_lang('bs'))
lang_menu.add_command(label='Bulgarian(bg)', command=lambda: change_lang('bg'))
lang_menu.add_command(label='Catalan(ca)', command=lambda: change_lang('ca'))
lang_menu.add_command(label='Cebuano(ceb)', command=lambda: change_lang('ceb'))
lang_menu.add_command(label='Chichewa(ny)', command=lambda: change_lang('ny'))
lang_menu.add_command(label='Chinese simplified(zh-cn)', command=lambda: change_lang('zh-cn'))
lang_menu.add_command(label='Chinese(zh-cn)', command=lambda: change_lang('zh-cn'))
lang_menu.add_command(label='Chinese traditional(zh-tw)', command=lambda: change_lang('zh-tw'))
lang_menu.add_command(label='Corsican(co)', command=lambda: change_lang('co'))
lang_menu.add_command(label='Croatian(hr)', command=lambda: change_lang('hr'))
lang_menu.add_command(label='Czech(cs)', command=lambda: change_lang('cs'))
lang_menu.add_command(label='Danish(da)', command=lambda: change_lang('da'))
lang_menu.add_command(label='Dutch(nl)', command=lambda: change_lang('nl'))
lang_menu.add_command(label='English(en)', command=lambda: change_lang('en'))
lang_menu.add_command(label='Esperanto(eo)', command=lambda: change_lang('eo'))
lang_menu.add_command(label='Estonian(et)', command=lambda: change_lang('et'))
lang_menu.add_command(label='Filipino(tl)', command=lambda: change_lang('tl'))
lang_menu.add_command(label='Finnish(fi)', command=lambda: change_lang('fi'))
lang_menu.add_command(label='French(fr)', command=lambda: change_lang('fr'))
lang_menu.add_command(label='Frisian(fy)', command=lambda: change_lang('fy'))
lang_menu.add_command(label='Galician(gl)', command=lambda: change_lang('gl'))
lang_menu.add_command(label='Georgian(ka)', command=lambda: change_lang('ka'))
lang_menu.add_command(label='German(de)', command=lambda: change_lang('de'))
lang_menu.add_command(label='Greek(el)', command=lambda: change_lang('el'))
lang_menu.add_command(label='Gujarati(gu)', command=lambda: change_lang('gu'))
lang_menu.add_command(label='Haitian creole(ht)', command=lambda: change_lang('ht'))
lang_menu.add_command(label='Hausa(ha)', command=lambda: change_lang('ha'))
lang_menu.add_command(label='Hawaiian(haw)', command=lambda: change_lang('haw'))
lang_menu.add_command(label='Hebrew(iw)', command=lambda: change_lang('iw'))
lang_menu.add_command(label='Hindi(hi)', command=lambda: change_lang('hi'))
lang_menu.add_command(label='Hmong(hmn)', command=lambda: change_lang('hmn'))
lang_menu.add_command(label='Hungarian(hu)', command=lambda: change_lang('hu'))
lang_menu.add_command(label='Icelandic(is)', command=lambda: change_lang('is'))
lang_menu.add_command(label='Igbo(ig)', command=lambda: change_lang('ig'))
lang_menu.add_command(label='Indonesian(id)', command=lambda: change_lang('id'))
lang_menu.add_command(label='Irish(ga)', command=lambda: change_lang('ga'))
lang_menu.add_command(label='Italian(it)', command=lambda: change_lang('it'))
lang_menu.add_command(label='Japanese(ja)', command=lambda: change_lang('ja'))
lang_menu.add_command(label='Javanese(jw)', command=lambda: change_lang('jw'))
lang_menu.add_command(label='Kannada(kn)', command=lambda: change_lang('kn'))
lang_menu.add_command(label='Kazakh(kk)', command=lambda: change_lang('kk'))
lang_menu.add_command(label='Khmer(km)', command=lambda: change_lang('km'))
lang_menu.add_command(label='Korean(ko)', command=lambda: change_lang('ko'))
lang_menu.add_command(label='Kurdish (kurmanji)(ku)', command=lambda: change_lang('ku'))
lang_menu.add_command(label='Kyrgyz(ky)', command=lambda: change_lang('ky'))
lang_menu.add_command(label='Lao(lo)', command=lambda: change_lang('lo'))
lang_menu.add_command(label='Latin(la)', command=lambda: change_lang('la'))
lang_menu.add_command(label='Latvian(lv)', command=lambda: change_lang('lv'))
lang_menu.add_command(label='Lithuanian(lt)', command=lambda: change_lang('lt'))
lang_menu.add_command(label='Luxembourgish(lb)', command=lambda: change_lang('lb'))
lang_menu.add_command(label='Macedonian(mk)', command=lambda: change_lang('mk'))
lang_menu.add_command(label='Malagasy(mg)', command=lambda: change_lang('mg'))
lang_menu.add_command(label='Malay(ms)', command=lambda: change_lang('ms'))
lang_menu.add_command(label='Malayalam(ml)', command=lambda: change_lang('ml'))
lang_menu.add_command(label='Maltese(mt)', command=lambda: change_lang('mt'))
lang_menu.add_command(label='Maori(mi)', command=lambda: change_lang('mi'))
lang_menu.add_command(label='Marathi(mr)', command=lambda: change_lang('mr'))
lang_menu.add_command(label='Mongolian(mn)', command=lambda: change_lang('mn'))
lang_menu.add_command(label='Myanmar (burmese)(my)', command=lambda: change_lang('my'))
lang_menu.add_command(label='Nepali(ne)', command=lambda: change_lang('ne'))
lang_menu.add_command(label='Norwegian(no)', command=lambda: change_lang('no'))
lang_menu.add_command(label='Pashto(ps)', command=lambda: change_lang('ps'))
lang_menu.add_command(label='Persian(fa)', command=lambda: change_lang('fa'))
lang_menu.add_command(label='Polish(pl)', command=lambda: change_lang('pl'))
lang_menu.add_command(label='Portuguese(pt)', command=lambda: change_lang('pt'))
lang_menu.add_command(label='Punjabi(pa)', command=lambda: change_lang('pa'))
lang_menu.add_command(label='Romanian(ro)', command=lambda: change_lang('ro'))
lang_menu.add_command(label='Russian(ru)', command=lambda: change_lang('ru'))
lang_menu.add_command(label='Samoan(sm)', command=lambda: change_lang('sm'))
lang_menu.add_command(label='Scots gaelic(gd)', command=lambda: change_lang('gd'))
lang_menu.add_command(label='Serbian(sr)', command=lambda: change_lang('sr'))
lang_menu.add_command(label='Sesotho(st)', command=lambda: change_lang('st'))
lang_menu.add_command(label='Shona(sn)', command=lambda: change_lang('sn'))
lang_menu.add_command(label='Sindhi(sd)', command=lambda: change_lang('sd'))
lang_menu.add_command(label='Sinhala(si)', command=lambda: change_lang('si'))
lang_menu.add_command(label='Slovak(sk)', command=lambda: change_lang('sk'))
lang_menu.add_command(label='Slovenian(sl)', command=lambda: change_lang('sl'))
lang_menu.add_command(label='Somali(so)', command=lambda: change_lang('so'))
lang_menu.add_command(label='Spanish(es)', command=lambda: change_lang('es'))
lang_menu.add_command(label='Sundanese(su)', command=lambda: change_lang('su'))
lang_menu.add_command(label='Swahili(sw)', command=lambda: change_lang('sw'))
lang_menu.add_command(label='Swedish(sv)', command=lambda: change_lang('sv'))
lang_menu.add_command(label='Tajik(tg)', command=lambda: change_lang('tg'))
lang_menu.add_command(label='Tamil(ta)', command=lambda: change_lang('ta'))
lang_menu.add_command(label='Telugu(te)', command=lambda: change_lang('te'))
lang_menu.add_command(label='Thai(th)', command=lambda: change_lang('th'))
lang_menu.add_command(label='Turkish(tr)', command=lambda: change_lang('tr'))
lang_menu.add_command(label='Ukrainian(uk)', command=lambda: change_lang('uk'))
lang_menu.add_command(label='Urdu(ur)', command=lambda: change_lang('ur'))
lang_menu.add_command(label='Uzbek(uz)', command=lambda: change_lang('uz'))
lang_menu.add_command(label='Vietnamese(vi)', command=lambda: change_lang('vi'))
lang_menu.add_command(label='Welsh(cy)', command=lambda: change_lang('cy'))
lang_menu.add_command(label='Xhosa(xh)', command=lambda: change_lang('xh'))
lang_menu.add_command(label='Yiddish(yi)', command=lambda: change_lang('yi'))
lang_menu.add_command(label='Yoruba(yo)', command=lambda: change_lang('yo'))
lang_menu.add_command(label='Zulu(zu)', command=lambda: change_lang('zu'))
options_menu.add_cascade(label="Change language", menu=lang_menu)
options_menu.add_command(label="Quit", command = quitit)
menu.add_cascade(label="Options", menu=options_menu)
root.config(menu=menu)
but1.grid(sticky=W)
toolbar.pack(fill=X, expand=1)
image_label.pack(side=TOP, fill=X)
mic_label.pack()
scroll.pack(side=RIGHT, fill=Y)
root.protocol("WM_DELETE_WINDOW", quitit)
text.configure(font=myfont)
text.configure(cursor="")
bar.pack(side=BOTTOM, fill=X, expand=1)
text.pack(side=LEFT, expand=1, fill=X)
scroll.config(command = text.yview)
root.after(250, t.start)
root.mainloop()
