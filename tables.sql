
drop table if exists Playlists;
CREATE TABLE Playlists
(
    P_Name text not null,
    N_Musics integer
);

drop table if exists Musics;
CREATE TABLE Musics
(
    M_Name text not null,
    M_Path text not null,
    P_Name text--,
    --Position_in_P integer
);

drop table if exists directory;
CREATE TABLE directory 
(
    folder_path text
);

