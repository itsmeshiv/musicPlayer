import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as Tk    
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
from PIL import Image, ImageTk




root = tk.ThemedTk()
root.get_themes()
root.set_theme('winnative')
root.geometry('480x320')

# canvas=Canvas(root,width=480,height=320)
# img=ImageTk.PhotoImage(Image.open("C:\\Users\\Anil Dubey\\Desktop\\Tranquil-River-Bed.jpg"))
# canvas.create_image(0,0,anchor=NW,image=img)
# canvas.pack()




statusbar = ttk.Label(root, text= "Welcome to Melody", relief= SUNKEN,anchor=W, font= 'Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)




menubar = Menu(root)
root.config(menu=menubar)

sub_menu = Menu(menubar,tearoff=0)

playlist =[]


def brows_file():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename= os.path.basename(filename)
    index=0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index+=1




menubar.add_cascade(label='File', menu=sub_menu)
sub_menu.add_command(label='Open',command=brows_file)
sub_menu.add_command(label='Exit',command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About This', 'This is a music player build using python tkinter by @shiv')


sub_menu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=sub_menu)
sub_menu.add_command(label="About us",command=about_us)

mixer.init()
root.title("Music bonaza")
root.iconbitmap(r"E:\\python\\icons\\icon.ico")



leftframe = Frame(root,bg='alice blue')
leftframe.pack(side=TOP,fill=X,anchor='n')

playlistbox=Listbox(leftframe,bg='bisque')
playlistbox.pack(side=TOP,anchor='nw',padx=5,pady=5)

add_btn=Tk.PhotoImage(file="E:\\python\\icons\\addfile.png")
addbtn= ttk.Button(leftframe,image=add_btn,command=brows_file)
addbtn.pack(side=LEFT,anchor='sw',padx=5)

def del_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


del_btn=Tk.PhotoImage(file="E:\\python\\icons\\delfile.png")

delbtn = ttk.Button(leftframe,image=del_btn,command=del_song)
delbtn.pack(side=BOTTOM,anchor='nw',padx=5)

#######################################right frame
# right_frame = Frame(root)
# right_frame.pack()

T_frame= Frame(root,bg='cyan',relief=GROOVE)
T_frame.pack(side=TOP,fill=X,anchor='nw',pady=3)

lengthlabel = ttk.Label(T_frame,background='cyan',text='--:--')
lengthlabel.pack(side=LEFT,anchor='nw')

currenttime_label = ttk.Label(T_frame,background='cyan', text = "--:--",foreground='red')
currenttime_label.pack(side=RIGHT,anchor='ne')






pro_bar=ttk.Progressbar(root,length=100, orient=HORIZONTAL)
pro_bar.pack(side=TOP,fill=X)





def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] ==".mp3":
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length=a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs=round(secs)
    time_format = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = ""+' - '+time_format


    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time = 0
    # pro_bar.start(current_time)
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs =divmod(current_time, 60)
            mins=round(mins)
            secs = round(secs)
            time_format = '{:02d}:{:02d}'.format(mins,secs)
            currenttime_label['text']= " "+' - '+ time_format
            
            time.sleep(1)
            current_time+=1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text']= 'Music Resumed'
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song= playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Playing Music'+'-'+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not foung',' Music could not find the file. please try another')

def stop_music():
    mixer.music.stop()
    statusbar['text']= "Music Stoped"

paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text']="Music Paused"

def rewind_music():
    play_music()
    statusbar['text']= "Music Rewinded"

def set_vol(val):
    volume =float(val)/100
    mixer.music.set_volume(volume)


muted = FALSE


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        vlm_btn.configure(image=vol_img)
        scale.set(70)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        vlm_btn.configure(image=mute_img)
        scale.set(0)
        muted= TRUE

# def total_length():
#     audio.info.length()

# def get_length():
#     if file_data[1] ==".mp3":
#         audio = MP3(play_song)
#         total_length = audio.info.length
#     else:
#         a = mixer.Sound(play_song)
#         total_length=a.get_length()




mid_frm = Label(root)
mid_frm.pack(side=BOTTOM,fill=X,anchor='sw')

play_img= ImageTk.PhotoImage(file="E:\\python\icons\play.png")

play_btn = ttk.Button(mid_frm, image=play_img,command= play_music)
# play_btn.config(width=10,height=2)

play_btn.grid(row=0,column=0)

stop_img= Tk.PhotoImage(file="E:\\python\icons\stop.png")

stop_btn = ttk.Button(mid_frm,image=stop_img,command= stop_music)
stop_btn.grid(row=0,column=2)


pause_img= Tk.PhotoImage(file="E:\\python\icons\pause.png")

pause_btn= ttk.Button(mid_frm,image=pause_img,command=pause_music)
pause_btn.grid(row=0,column=1)

# btm_frm= Frame(root)
# btm_frm.pack()


rewind_img= Tk.PhotoImage(file="E:\\python\icons\\rewind.png")

rewindbtn=ttk.Button(mid_frm,image=rewind_img,command=rewind_music)
rewindbtn.grid(row=0,column=4)

vol_img= Tk.PhotoImage(file="E:\\python\icons\\volume.png")
mute_img= Tk.PhotoImage(file="E:\\python\icons\mute.png")

vlm_btn=ttk.Button(mid_frm,image=vol_img,command=mute_music)
vlm_btn.grid(row=0,column=5)


scale= ttk.Scale(mid_frm,from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0,column=6, pady=15, padx=30)

# music_scale=ttk.Scale(btm_frm,from_=0, to=100,orient=HORIZONTAL,command=get_length)
# music_scale.set(0)
# mixer.music.get_length()
# music_scale.grid(row=1,column=0,padx=30,pady=10)


def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
