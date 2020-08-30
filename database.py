import sqlite3
import os
from datetime import datetime


class Database:

    def __init__(self):

        file_ = ''
        files = [f for f in os.listdir() if f.endswith('.db')]

        if len(files) == 1:
            file_ = files[0]
            self.reset = False
        elif len(files) == 0:
            file_ = f'playlists_record.db'
            self.reset = True


        self.conn = sqlite3.connect(file_)
        self.cur = self.conn.cursor()

        if self.reset:
            self.cur.executescript(open('tables.sql', 'r').read())
            self.conn.commit()



    # Register New Playlist on the Database
    def register_playlist(self, pl_name):

        self.cur.execute("SELECT * FROM Playlists WHERE P_Name = :p_name", {'p_name': pl_name})

        repeated_playlists = self.cur.fetchall()

        if len(repeated_playlists) > 0:
            return -1


        self.cur.execute("SELECT * FROM Musics WHERE P_Name = :p_name", {'p_name': pl_name})
        
        musics = self.cur.fetchall()

        num_musics = len(musics)

        self.cur.execute("""INSERT INTO Playlists (P_Name, N_Musics) VALUES (:name, :n_musics)""", {'name': pl_name, 'n_musics': num_musics})
        self.conn.commit()
        
        return 0



    # Get All Playlists on the Database
    def get_playlists(self):

        self.cur.execute("SELECT * FROM Playlists")
        
        playlists = self.cur.fetchall()

        return playlists



    # Delete Playlist from Database
    def delete_playlist(self, p_name):
        
        self.cur.execute("SELECT * FROM Playlists WHERE P_Name = :name", {'name': p_name})
        
        playlists = self.cur.fetchall()

        if len(playlists) == 1:
            
            self.cur.execute("DELETE FROM Playlists WHERE P_Name = :name", {'name': p_name})
            self.conn.commit()
            return 1

        else:
            return 0



    # Identify if is an existing Playlist
    def playlist_exists(self, p_name):

        self.cur.execute("SELECT * FROM Playlists WHERE P_Name = :name", {'name': p_name})
        
        playlists = self.cur.fetchall()

        if len(playlists) == 1:
            return 1

        else:
            return 0



    # Get All Musics belonging to the Playlist
    def get_musics_from_playlist(self, p_name):

        self.cur.execute("SELECT * FROM Musics WHERE P_Name = :name", {'name': p_name})
        
        musics = self.cur.fetchall()

        return musics



    # Check if there is any directory in the database and get it
    def DB_dir(self):

        self.cur.execute("SELECT * FROM directory")

        dir = self.cur.fetchall()

        return dir



    # Change Directory to a new one
    def change_dir(self, new_path):

        self.cur.execute("SELECT * FROM directory")

        dir = self.cur.fetchall()


        if len(dir) == 0:
            
            self.cur.execute("""INSERT INTO directory (folder_path) VALUES (:path)""", {'path': new_path})
            self.conn.commit()


        elif len(dir) == 1:

            self.cur.execute("UPDATE directory SET folder_path = :path WHERE oid = 1", {'path': new_path})
            self.conn.commit()
    