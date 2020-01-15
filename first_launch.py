from tkinter.font import Font
from tkinter import *
from os import system, remove
import configparser as cp
import datetime
import pyttsx3
import googletrans

t = googletrans.Translator()
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty('rate',  - 50)
engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')

def speak(text):
    engine.say(text)
    engine.runAndWait()

class InputDialog:
    def __init__(self, prompt):
        self.sub_root = Tk()
        self.sub_root.title("Jason")
        self.myfont = Font(root=self.sub_root, family="Arial", size=8)
        self.sub_root.maxsize(320, 240)
        self.sub_root.wm_attributes("-topmost", True)
        self.sub_root.overrideredirect(True)
        self.sub_root.update_idletasks()
        screen_width = self.sub_root.winfo_screenwidth()
        screen_height = self.sub_root.winfo_screenheight()
        size = tuple(int(_) for _ in self.sub_root.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2
        self.sub_root.geometry("+%d+%d" % (x, y))
        prompt_label = Label(self.sub_root, text=prompt)
        self.var = StringVar(self.sub_root)
        entry = Entry(self.sub_root, textvariable=self.var, width=160 )
        entry.focus_set()
        button = Button(self.sub_root, command=self.return_text, text="OK", bg = "#448DE0", fg="White", bd=0, width=12, pady=4, padx=4, height=1,font=self.myfont, highlightcolor="#A3C7F0")
        prompt_label.pack(fill=X, expand=YES)
        entry.pack()
        button.pack(side=BOTTOM)
        self.text = ""
    def return_text(self):
        self.text = self.var.get()
        self.sub_root.destroy()

    def ask(self):
        self.sub_root.mainloop()

class ListDialog:
    def __init__(self, names, prompt):
        self.names = names
        self.sub_root = Tk()
        self.sub_root.title("Jason")
        self.myfont = Font(root=self.sub_root, family="Arial", size=8)
        self.sub_root.maxsize(640, 480)
        self.sub_root.wm_attributes("-topmost", True)
        self.sub_root.overrideredirect(True)
        self.sub_root.update_idletasks()
        screen_width = self.sub_root.winfo_screenwidth()
        screen_height = self.sub_root.winfo_screenheight()
        size = tuple(int(_) for _ in self.sub_root.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2
        self.sub_root.geometry("+%d+%d" % (x, y))
        label = Label(self.sub_root, text=prompt)
        label.pack(fill=X)
        scroll = Scrollbar(self.sub_root)
        scroll.pack(side=RIGHT,fill=Y)
        self.box = Listbox(self.sub_root, yscrollcommand=scroll.set, selectmode=SINGLE)
        scroll.config(command=self.box.yview)
        c = 0
        for i in names:
            self.box.insert(c, i)
            c+=1
        self.box.pack(fill=X)
        button = Button(self.sub_root, command=self.get_choice, text="OK", bg = "#448DE0", fg="White", bd=0, width=12, pady=4, padx=4, height=1,font=self.myfont, highlightcolor="#A3C7F0")
        button.pack(side=BOTTOM)
        self.choice = names[0]

    def get_choice(self):
        if len(self.box.curselection()) != 0:
            self.choice = self.names[self.box.curselection()[0]]
        self.sub_root.destroy()

    def ask(self):
        self.sub_root.mainloop()

try:
    remove("config.ini")
except:
    pass
c = cp.ConfigParser()
speak("Hello!!! I am Jason, your loyal assistant.")
speak("I need some of your information to personalize some content?")
lang = ListDialog(list(map(lambda x: x.capitalize(), googletrans.LANGUAGES.values())), "Default language")
lang.ask()
lang = lang.choice
for i,f in googletrans.LANGUAGES.items():
    if f == lang.lower():
        lang = i
        break
name = InputDialog(t.translate("What is your name?", dest=lang).text)
name.ask()
name = name.text
year = ListDialog(list(map(lambda x: str(x), range(1900, datetime.datetime.now().year))), t.translate("When were you born?", dest=lang).text)
year.ask()
year = year.choice
info = {"name": name, "year": year}
c["Profile"] = info
c["Settings"] = {"color": "#000000", "color_hex": "0,0,0", "lang":str(lang)}
c["Other"] = {"lst_com": "null"}
with open("config.ini", "w") as f:
    c.write(f)

with open('error.log', 'w') as f:
    f.write("[{0}] - Initialized".format(str(datetime.datetime.now().year)))

system("main.py")