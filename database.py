import sqlite3
import os
from datetime import datetime


class Database:

    def __init__(self):

        file_ = ''
        files = [f for f in os.listdir() if f.endswith('.db')]
        print(files)
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


    def register_playlist(self, pl_name):
        self.cur.execute("SELECT * FROM Playlists")
        
        playlists = self.cur.fetchall()

        num_playlists = len(playlists)


        self.cur.execute("SELECT * FROM Musics WHERE P_Name = :p_name", {'p_name': pl_name})
        
        musics = self.cur.fetchall()

        num_musics = len(musics)
        
        time_now = datetime.now()

        self.cur.execute("""INSERT INTO Playlists (P_Id, P_Name, N_Musics, data_test) VALUES (:id , :name, :n_musics, :time)""", {'id': num_playlists, 'name': pl_name, 'n_musics': num_musics, 'time': time_now})
        self.conn.commit()