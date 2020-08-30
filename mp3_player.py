from tkinter import *
import pygame
import os
from tkinter import filedialog
from tkinter import messagebox
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from PIL import ImageTk,Image
import database

root = Tk()
root.title("MP3 Player")
root.iconbitmap(r"images\Wwalczyszyn-Android-Style-Honeycomb-Music.ico")
root.geometry("500x400")
root.config(bg="grey")


# Initialize Pygame Mixer
pygame.mixer.init()


# List of Paths of every .mp3 file imported
song_dir_list = []


# App Database
playlists_record = database.Database()


# Variable to control the Playlists Visibility
showing_playlists = False


# Directory to get musics from
songs_main_dir = ''


# Define of Create Directory to import musics
def dir_define():

    check_dir_db = []


    # Check if there is any directory in the Database
    check_dir_db = playlists_record.DB_dir()
   


    if len(check_dir_db) == 0:

        check_dir = os.path.isdir("./audio")

        if check_dir == False:
            os.mkdir("/audio")

        songs_main_dir = 'audio/'


    elif len(check_dir_db) == 1:

        check_dir_db_1 = check_dir_db[0]

        songs_main_dir = check_dir_db_1[0]
        print(check_dir_db_1[0])



# Function to display Existing Playlists
def display_playlists():

    global showing_playlists
    
    playlists_list = []

    if song_box.size() == 0:

        playlists_list = playlists_record.get_playlists()
         
        for elem in playlists_list:
            song_box.insert(END, elem[0])

        showing_playlists = True

        return_btn.grid_forget()

        info_label.grid(row=0, column=1, sticky=W)

    elif showing_playlists:
        song_box.insert(END, new_playlist_name.get())
            
        return_btn.grid_forget()

        info_label.grid(row=0, column=1, sticky=W)

    else:
        pass

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



# Function To Register New Playlist on Database
def register_new_playlist():

    # Get Playlist Name
    playlist_name = new_playlist_name.get()
    
    # Check for Repeated Playlists and register new unique names
    check_repeated = playlists_record.register_playlist(playlist_name)

    # If Playlist already exists, shows error
    if check_repeated == -1:
        response = messagebox.showerror("Repeated Playlist!", "Playlist with that Name Already Exists! Please choose a different Name.")

    # Otherwise closes Window
    else:
        display_playlists()
        new_playlist_window.destroy()




# Function to Create New Playlist
def new_playlist():

    # New Window to Write New Playlist Name
    global new_playlist_window
    new_playlist_window = Toplevel()
    new_playlist_window.title('New Playlist')
    new_playlist_window.iconbitmap(r"images\Wwalczyszyn-Android-Style-Honeycomb-Music.ico")
    
    new_playlist_label = Label(new_playlist_window, text = "New Playlist Name:")
    new_playlist_label.pack()

    # Entry to Write Playlist Name On
    global new_playlist_name
    new_playlist_name = Entry(new_playlist_window, width=50)
    new_playlist_name.pack()
    

    # Button to Save Playlist
    save_playlist_btn = Button(new_playlist_window, text="Save", command=register_new_playlist)
    save_playlist_btn.pack()



# Function to delete selected Playlist
def delete_this_playlist():

    selected_playlist = song_box.selection_get()

    playlist_index = song_box.index(ACTIVE)

    check = playlists_record.delete_playlist(selected_playlist)

    if check == 1:
        song_box.delete(playlist_index)


# Add Song Function
def add_song():

    global showing_playlists


    global songs_main_dir


    dir_define()
    #print(songs_main_dir)


    song = filedialog.askopenfilename(initialdir=songs_main_dir, title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))


    # If it's displaying Playlists, it cleans the song box
    if len(song) > 0:

        if showing_playlists:
            song_box.delete(0, END)
            showing_playlists = False

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


        # Update Directory
        playlists_record.change_dir(song_file)



# Add many songs to playlist
def add_many_songs():

    global showing_playlists


    global songs_main_dir


    dir_define()


    song_file = ''


    songs = filedialog.askopenfilenames(initialdir=songs_main_dir, title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))


    # If it's displaying Playlists, it cleans the song box
    if len(songs) > 0:

        if showing_playlists:
            song_box.delete(0, END)
            showing_playlists = False
    
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


        # Update Directory
        playlists_record.change_dir(song_file)



# Function to get back to Playlists Menu
def get_back():

    song_box.delete(0, END)
    
    display_playlists()



# Play Selected Song
def play():

    item = song_box.get(ACTIVE)

    is_playlist = playlists_record.playlist_exists(item)

    if is_playlist == 1:

        song_box.delete(0, END)

        musics_from_playlist = []

        musics_from_playlist = playlists_record.get_musics_from_playlist(item)

        song_dir_list.clear()

        info_label.grid_forget()

        for elem in musics_from_playlist:
            song_box.insert(END, elem[0])
            song_dir_list.append(elem[1])

        return_btn.grid(row=0, column=0, sticky=W, pady=(1,2))

        

    else:
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


    # If the song box is empty, it shows the Playlists
    if song_box.size() == 0:
        display_playlists()

    

# Delete All Songs from Playlist
def delete_all_songs():
    stop()
    song_box.delete(0, END)

    # Delete Songs paths from the Path List
    for i in range(len(song_dir_list)):
        song_dir_list.pop(0)

    # Stop Music If it's playing
    pygame.mixer.music.stop()


    # If the song box is empty, it shows the Playlists
    if song_box.size() == 0:
        display_playlists()



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
song_box.grid(row=1, column=0, columnspan = 2)


# Create Player Control Button Images
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img = PhotoImage(file='images/forward.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')
return_btn_img = PhotoImage(file='images/back_arrow.png')


# Create Player Control Frame

ctrl_frame = Frame(master_frame, bg="grey")
ctrl_frame.grid(row=2, column=0, columnspan = 2)

# Create Volume Label Frame
volume_frame = LabelFrame(master_frame, text="Volume", bg="grey")
volume_frame.grid(row=1, column=2, padx=(20,0))


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

# Create Playlist Menu
playlist_menu = Menu(my_menu)
my_menu.add_cascade(label = "Playlist", menu=playlist_menu)
playlist_menu.add_command(label="New Playlist", command=new_playlist)
playlist_menu.add_command(label="Delete Playlist", command=delete_this_playlist)

# Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Menu", command=add_song)

# Add Many Songs to Playlist
add_song_menu.add_command(label="Add Many Songs To Menu", command=add_many_songs)


# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu = remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Menu", command = delete_song)
remove_song_menu.add_command(label="Delete All Songs From Menu", command = delete_all_songs)


# Create Status Bar
status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length = 360)
my_slider.grid(row=3, column=0, pady=(30,10), columnspan = 2)


# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=0, command=volume, length = 111)
volume_slider.pack(pady=(10, 4))

# Create Current Volume Label
slider_label = Label(volume_frame, text="100", bg="grey")
slider_label.pack()


# Information Label
info_label = Label(master_frame, text="Playlists:", bg="grey")



# Create a return button
return_btn = Button(master_frame, image=return_btn_img, borderwidth = 0, command=get_back)



# Define Directory to get song from
dir_define()


# Check if its time to display playlists
display_playlists()


root.mainloop()