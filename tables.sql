
drop table if exists Playlists;
CREATE TABLE Playlists
(
    P_Id integer primary key,
    P_Name text not null,
    N_Musics integer,
    data_test timestamp
);

drop table if exists Musics;
CREATE TABLE Musics
(
    M_Id integer primary key,
    M_Name text not null,
    M_Path text not null,
    P_Id integer,
    P_Name timestamp,
    Position_in_P integer
);

drop table if exists directory;
CREATE TABLE directory 
(
    folder_path text
);

