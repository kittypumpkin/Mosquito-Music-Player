import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from mutagen.mp3 import MP3
from pygame import mixer

mixer.init()  # initialising mixer
mosquito = Tk()
mosquito.title("Mosquito Music Player")
# mosquito.geometry("600x600")
mosquito.iconbitmap("img/icon.ico")

# Initialising Frames for the player
leftframe = Frame(mosquito)
rightframe = Frame(mosquito)

topleftframe = Frame(leftframe)
middleleftframe1 = Frame(leftframe)
middleleftframe2 = Frame(leftframe)
bottomleftframe = Frame(leftframe)

middlerightframe = Frame(rightframe)
bottomrightframe = Frame(rightframe)

# Initialise icon variables
playpic = PhotoImage(file="img/play.png")
pausepic = PhotoImage(file="img/pause.png")
prevpic = PhotoImage(file="img/prev.png")
nextpic = PhotoImage(file="img/next.png")
addpic = PhotoImage(file="img/add.png")
delpic = PhotoImage(file="img/del.png")
volpic = PhotoImage(file="img/vol.png")
mutepic = PhotoImage(file="img/mute.png")
mosquitopic = PhotoImage(file="img/mascot.png")

# Playlist ScrollBar
playlistscroll = Scrollbar(middlerightframe)
playlistscroll.pack(side=RIGHT, fill=Y)

# PlayList
playlistbox = Listbox(middlerightframe, height=20, width=50, highlightcolor="blue", bd=10, relief=SUNKEN,
                      yscrollcommand=playlistscroll.set, fg="purple", bg="lightblue", selectbackground="green",
                      font="Times")

# putting the above icons into Label
defaultpic = Label(middleleftframe1, image=mosquitopic)
statusbar = Label(mosquito, text="Hi There!", relief=SUNKEN, anchor=W)
totallength = Label(middleleftframe2, relief=GROOVE, text="--:--")
currenttime = Label(middleleftframe2, relief=GROOVE, text="--:--")
currentfile = Label(topleftframe, text="Currently Playing: ----")

# Default operations
mixer.music.set_volume(0.5)
filename = "-+*/"
paused = False
muted = False
index = 0
playlist = []


# Functions of the Buttons

def play_btn():
    global paused
    if filename == "-+*/":
        tkinter.messagebox.showerror("File Not Found! You'll die of Malaria", "Mosquito couldn't find the File to "
                                                                              "bite! File-->Open-->Choose! ")
    else:
        mixer.music.unpause()
        statusbar["text"] = "Now Playing - " + os.path.basename(filename)
        playbtn.configure(image=pausepic)
        paused = False


def pause_btn():
    global paused
    if filename == "-+*/":
        tkinter.messagebox.showerror("File Not Found! You'll die of Malaria", "Mosquito couldn't find the File to "
                                                                              "bite! File-->Open-->Choose! ")
    elif paused:
        play_btn()
    else:
        mixer.music.pause()
        statusbar["text"] = "Music Paused - " + os.path.basename(filename)
        playbtn.configure(image=playpic)
        paused = True


def next_btn():
    pass


def prev_btn():
    pass


def add_btn():
    global index, filename
    filename = filedialog.askopenfilename()
    playlistbox.insert(index, os.path.basename(filename))
    playlist.insert(index, filename)
    index += 1
    browse()


def del_btn():
    pass


def vol_btn():
    global muted
    mixer.music.set_volume(0.7)
    volbar.set(70)
    volbtn.configure(image=volpic)
    muted = False


def mute_btn():
    global muted
    if muted:
        vol_btn()
    else:
        muted = True
        mixer.music.set_volume(0)
        volbar.set(0)
        volbtn.configure(image=mutepic)


def vol_bar(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)  # this only takes value from 0 to 1


def crn_ptr(val):
    pass


def abt_us():
    tkinter.messagebox.showinfo("About Us", "Hey There! I'm CivilisedFalcon")


def stop_btn():
    mixer.music.stop()
    statusbar["text"] = "Music Stopped - " + os.path.basename(filename)


def browse():
    global filename, index
    mixer.music.load(filename)
    mixer.music.play()
    statusbar["text"] = "Music Started - " + os.path.basename(filename)
    playbtn.configure(image=pausepic)
    details()



def details():
    filedetail = os.path.splitext(filename)
    currentfile["text"] = "Currently Playing: " + os.path.basename(filename)
    global paused
    if filedetail[1] == ".mp3":
        mus = MP3(filename)
        musiclength = mus.info.length
    else:
        mus = mixer.Sound(filename)
        musiclength = mus.get_length()

    mins, secs = divmod(musiclength, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    totallength["text"] = "Total Length: " + timeformat
    t1 = threading.Thread(target=start_count, args=(musiclength,))
    t1.start()


def start_count(t):
    global paused
    crnttime = 0
    while crnttime <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(crnttime, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttime["text"] = "Current Time " + timeformat
            time.sleep(1)
            crnttime += 1


def close():
    stop_btn()
    mosquito.destroy()


# BUTTONS

playbtn = Button(bottomleftframe, image=playpic, border="0", command=pause_btn)
nextbtn = Button(bottomleftframe, image=nextpic, border="0", command=next_btn)
prevbtn = Button(bottomleftframe, image=prevpic, border="0", command=prev_btn)
addbtn = Button(bottomrightframe, image=addpic, border="0", command=add_btn)
delbtn = Button(bottomrightframe, image=delpic, border="0", command=del_btn)
volbtn = Button(topleftframe, image=volpic, border="0", command=mute_btn)

# Volume Bar
volbar = Scale(topleftframe, from_=0, to=100, orient=HORIZONTAL, command=vol_bar)
volbar.set(50)

# Current Pointer Bar
crnptr = Scale(middleleftframe2, from_=0, to=100, orient=HORIZONTAL, command=crn_ptr)
crnptr.set(0)

# Scroll Bar for Playlist
playlistscroll.config(command=playlistbox.yview)

# Menu bar
menubar = Menu(mosquito)
mosquito.config(menu=menubar)

# Submenu
submenu1 = Menu(menubar, tearoff=0)
submenu2 = Menu(menubar, tearoff=0)
submenu3 = Menu(menubar, tearoff=0)

# Naming Submenu (officially called cascades)
menubar.add_cascade(label="File", menu=submenu1)
menubar.add_cascade(label="Playback", menu=submenu2)
menubar.add_cascade(label="Sound", menu=submenu3)

# About us
menubar.add_command(label="About Us", command=abt_us)

# Adding commands to submenu1
submenu1.add_command(label="Open", command=add_btn)
submenu1.add_command(label="Exit")

# Adding commands to submenu2
submenu2.add_command(label="Play", command=play_btn)
submenu2.add_command(label="Pause", command=pause_btn)
submenu2.add_command(label="Next Song", command=next_btn)
submenu2.add_command(label="Prev Song", command=prev_btn)
submenu2.add_command(label="Stop", command=stop_btn)

# Adding Commands to submenu3
submenu3.add_command(label="Volume = 100%", command=vol_bar(100))
submenu3.add_command(label="Volume = 75%", command=vol_bar(75))
submenu3.add_command(label="Volume = 50%", command=vol_bar(50))
submenu3.add_command(label="Volume = 25%", command=vol_bar(25))
submenu3.add_command(label="Mute", command=vol_bar(0))

# Layout of the Mosquito Player
statusbar.pack(side=BOTTOM, fill=X)
leftframe.pack(side=LEFT, padx=10)
rightframe.pack(side=RIGHT, padx=10)

topleftframe.grid(row=0, column=0)
middleleftframe1.grid(row=1, column=0)
middleleftframe2.grid(row=2, column=0)
bottomleftframe.grid(row=3, column=0)

middlerightframe.grid(row=0, rowspan=3, column=0)
bottomrightframe.grid(row=3, column=0)

volbtn.grid(row=0, column=0, sticky=W)
volbar.grid(row=0, column=1, columnspan=5)

defaultpic.grid(column=0, columnspan=6)

currenttime.grid(row=0, column=0)
crnptr.grid(row=0, column=1, columnspan=4)
totallength.grid(row=0, column=5)

playbtn.grid(row=0, column=0, columnspan=2, padx=5)
prevbtn.grid(row=0, column=2, columnspan=2, padx=2)
nextbtn.grid(row=0, column=4, columnspan=2, padx=2)

addbtn.grid(row=0, column=0)
delbtn.grid(row=0, column=1)

playlistbox.pack()

mosquito.protocol("WM_DELETE_WINDOW", close)
mosquito.mainloop()
