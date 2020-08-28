from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from PIL import ImageTk,Image
import database

root = Tk()
root.title("MP3 Player")
root.iconbitmap(r"images\Wwalczyszyn-Android-Style-Honeycomb-Music.ico")
root.geometry("500x370")
root.config(bg="grey")


# Initialize Pygame Mixer
pygame.mixer.init()


# List of Paths of every .mp3 file imported
song_dir_list = []


playlists_record = database.Database()


# Grab Song Lenght Time Info
def play_time():
    # Check for double timing
    if stopped:
        return

    # Grab Current Song Elapsed Time
    current_time = pygame.mixer.music.get_pos()/1000


    # Convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))


    # Get Currently Playing Song
    current_song = song_box.get(ACTIVE)


    # Getting song index in order to choose the right path for it in the Path List
    song_index = song_box.index(ACTIVE)

    current_song = f'{song_dir_list[song_index]}{current_song}.mp3'

    # Get Song Lenght with Mutagen
    song_mut = MP3(current_song)    

    # Get song length
    global song_length
    song_length = song_mut.info.length


    # Convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Increase Current Time by 1 second (for sync)
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed:   {converted_song_length}   of   {converted_song_length}  ')
       
    elif paused:
        pass
    
    elif int(my_slider.get()) == int(current_time):
        # slider hasn't been moved
        # Update Slider to Position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value = int(current_time))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed:   {converted_current_time}   of   {converted_song_length}  ')


    else:
        # Update Slider to Position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value = int(my_slider.get()))
        
        # Convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed:   {converted_current_time}   of   {converted_song_length}  ')


        # Move this thing along by one second
        next_time = int(my_slider.get()) + 1

        my_slider.config(value=next_time)

    # Update Time
    status_bar.after(1000, play_time)



# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir="audio/", title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))


    # Getting the path of the .mp3 file
    song_dir = song.split("/")

    song_dir_len = len(song_dir)

    song_dir.pop(song_dir_len-1)

    song_file = song_dir[0]

    song_dir.pop(0)

    for elem in song_dir:
        song_file = song_file + "/" + elem

    song_file = song_file + "/"


    # Saving path of the .mp3 file in the path List
    song_dir_list.append(song_file)


    # Strip out the directory info and .mp3 extension from the song name
    song = song.replace(song_file, "")
    song = song.replace(".mp3", "")

    # Add song to list box
    song_box.insert(END, song)



# Add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="audio/", title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))
    
    # Strip out the directory info and .mp3 extension from the song name
    for song in songs:
        
        # Getting the path of the .mp3 file
        song_dir = song.split("/")

        song_dir_len = len(song_dir)

        song_dir.pop(song_dir_len-1)

        song_file = song_dir[0]

        song_dir.pop(0)

        for elem in song_dir:
            song_file = song_file + "/" + elem

        song_file = song_file + "/"


        # Saving path of the .mp3 file in the path List
        song_dir_list.append(song_file)


        # Strip out the directory info and .mp3 extension from the song name
        song = song.replace(song_file, "")
        song = song.replace(".mp3", "")

        # Add song to list box
        song_box.insert(END, song)



# Play Selected Song
def play():
    # Set Stopped Variable to False so song can play
    global stopped
    stopped = False
    
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    
    song = song_box.get(ACTIVE)

    # Getting song index in order to choose the right path for it in the Path List
    song_index = song_box.index(ACTIVE)

    song = f'{song_dir_list[song_index]}{song}.mp3'
        

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Call the play_time function to get the song lenght
    play_time()



# Stop Playing Current Song
global stopped
stopped = False
def stop():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Stop Song From Playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Clear The Status Bar
    status_bar.config(text='')

    # Set Stop Variable To True
    global stopped
    stopped = True



# Play The Next Song in the Playlist
def forward():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number
    next_song = song_box.curselection()
    size = song_box.size()
    

    # Add one to the current song number
    next_song = next_song[0]+1

    if next_song == size:
        next_song = 0

    song = song_box.get(next_song)

    song = f'{song_dir_list[next_song]}{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, END)
    
    # Activate new song bar
    song_box.activate(next_song)

    # Set Active Bar to Next Song
    song_box.selection_set(next_song, last=None)



def back():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number
    previous_song = song_box.curselection()
    size = song_box.size()
    

    # Add one to the current song number
    previous_song = previous_song[0]-1

    if previous_song < 0:
        previous_song = size-1

    song = song_box.get(previous_song)

    song = f'{song_dir_list[previous_song]}{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, END)
    
    # Activate new song bar
    song_box.activate(previous_song)

    # Set Active Bar to Next Song
    song_box.selection_set(previous_song, last=None)



# Delete a Song
def delete_song():
    stop()
    

    # Getting song index in order to choose the right path for it in the Path List
    song_idx = song_box.index(ANCHOR)

    song_box.delete(ANCHOR)


    # Delete Song path from the Path List
    song_dir_list.pop(song_idx)

    # Stop Music If it's playing
    pygame.mixer.music.stop()

    

# Delete All Songs from Playlist
def delete_all_songs():
    stop()
    song_box.delete(0, END)

    # Delete Songs paths from the Path List
    for i in range(len(song_dir_list)):
        song_dir_list.pop(0)

    # Stop Music If it's playing
    pygame.mixer.music.stop()



# Create Global Pause Variable
global paused
paused = False

# Pause and Unpause the Current Song
def pause(paused_1):
    global paused
    paused = paused_1

    # Unpause
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    # Pause
    else:
        pygame.mixer.music.pause()
        paused = True



# Create Slider Function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)

    song_index = song_box.index(ACTIVE)

    song = f'{song_dir_list[song_index]}{song}.mp3'

    # Get Current Volume
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))



# Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(1-volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    slider_label.config(text=int((current_volume)*100))

    

# Create Master Frame
master_frame = Frame(root, bg="grey")
master_frame.pack(pady=20, padx=(30,0))

# Create Playlist Box
song_box = Listbox(master_frame, bg = "black", fg="green", width=60, selectbackground="white", selectforeground="black")
song_box.grid(row=0, column=0)


# Create Player Control Button Images
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img = PhotoImage(file='images/forward.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')


# Create Player Control Frame

ctrl_frame = Frame(master_frame, bg="grey")
ctrl_frame.grid(row=1, column=0)

# Create Volume Label Frame
volume_frame = LabelFrame(master_frame, text="Volume", bg="grey")
volume_frame.grid(row=0, column=1, padx=(20,0))


# Create Player Control Buttons

back_btn = Button(ctrl_frame, image=back_btn_img, borderwidth = 0, command=back)
forward_btn = Button(ctrl_frame, image=forward_btn_img, borderwidth = 0, command=forward)
play_btn = Button(ctrl_frame, image=play_btn_img, borderwidth = 0, command=play)
pause_btn = Button(ctrl_frame, image=pause_btn_img, borderwidth = 0, command=lambda:pause(paused))
stop_btn = Button(ctrl_frame, image=stop_btn_img, borderwidth = 0, command=stop)


back_btn.grid(row=0, column=0, pady=(20,0))
forward_btn.grid(row=0, column=4, pady=(20,0))
play_btn.grid(row=0, column=2, pady=(20,0))
pause_btn.grid(row=0, column=1, pady=(20,0))
stop_btn.grid(row=0, column=3, pady=(20,0))


# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# Add Many Songs to Playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)


# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu = remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command = delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command = delete_all_songs)


# Create Status Bar
status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length = 360)
my_slider.grid(row=2, column=0, pady=(30,10))


# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=0, command=volume, length = 111)
volume_slider.pack(pady=(10, 4))

# Create Current Volume Label
slider_label = Label(volume_frame, text="100", bg="grey")
slider_label.pack()

root.mainloop()