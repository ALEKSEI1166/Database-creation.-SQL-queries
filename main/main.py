1.   CREATE DATABASE music WITH OWNER = postgres;
\c music-new;

CREATE TABLE IF NOT EXISTS Tracks (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR(50) NOT NULL,
	duration TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS Artists (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR(50) NOT NULL unique
);

CREATE TABLE IF NOT EXISTS Albums (	
	Id SERIAL PRIMARY KEY,
	id_artist INTEGER REFERENCES Artists,
	Name VARCHAR(50) NOT NULL,
	Year INTEGER CHECK (Year > 1970 and Year < 2023)
);
ALTER TABLE Tracks ADD COLUMN id_album INTEGER REFERENCES Albums;

CREATE TABLE IF NOT EXISTS Genres (
	Id SERIAL PRIMARY KEY,	
	Name VARCHAR(30) NOT NULL UNIQUE
);
ALTER TABLE Artists ADD COLUMN id_genre INTEGER NOT NULL REFEREN



2. --CREATE-запросы

CREATE TABLE IF NOT EXISTS Artists (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	genre VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genres (
	id SERIAL PRIMARY KEY,	
	name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ArtistGenres (
	id_artist INTEGER REFERENCES Artists(id),
	id_genre INTEGER REFERENCES Genres(id),
	constraint AG PRIMARY KEY (id_artist, id_genre)
);

CREATE TABLE IF NOT EXISTS Albums (	
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	year INTEGER CHECK (Year > 1970 and Year < 2023)
);

CREATE TABLE IF NOT EXISTS AlbumArtist (
	id_artist INTEGER REFERENCES Artists(id),
	id_album INTEGER REFERENCES Albums(id),
	constraint AA PRIMARY KEY (id_artist, id_album)
);

CREATE TABLE IF NOT EXISTS Tracks (
	id_track SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	duration INTEGER NOT NULL CHECK (duration > 0),
	album INTEGER REFERENCES Albums(id)
);

CREATE TABLE IF NOT EXISTS Collection (	
	Id SERIAL PRIMARY KEY,
	Name VARCHAR(50) NOT NULL,
	Year INTEGER CHECK (Year > 1970 and Year < 2023)
);

CREATE TABLE IF NOT EXISTS CollectionTracks (
	id_collection INTEGER REFERENCES Collection(id),
	id_track INTEGER REFERENCES Tracks(id_track),
	constraint CT PRIMARY KEY (id_collection, id_track)
);




3.  INSERT INTO DATABASE music_new WITH OWNER = postgres;

--запросы для записи Genres:
INSERT INTO genres (name) VALUES
	('Disco'),
    ('Country'),
	('Glam rock'),
	('Hard rock'),
	('Heavy metal'),
	('Electronic music'),
	('Jazz'),
	('Folk');

--запросы для записи Artists:
INSERT INTO artists(name) VALUES 
    ('Boney M'),
	('Smokie'),
	('Kiss'),
	('AC/DC'),
	('Metallica'),
	('Kraftwerk'),
	('Jeff Lofton'),
	('Bob Dylan');
	

--запросы для записи Albums:
INSERT INTO albums (name, year) VALUES
    ('Nightflight to Venus', 1978),
    ('Pass it Around', 1975),
	('Dynasty', 1979),
	('Flick of The Switch', 1983),
	('Reload', 1997),
	('Computerwelt', 2009),
	('Silvers Strut', 2021),
	('The Freewheelin', 1971);


--запросы для записи Tracks:
INSERT INTO tracks (name, duration, album) VALUES
    ('Rasputin', 539, 1),
    ('Rivers of Babylon', 346, 1),
	('Ill Meet You at Midnitht', 315, 2),
    ('What Can I Do', 336, 2),
	('I Was Made for Lovin You', 434, 3),
    ('Love Gun', 316, 3),
	('Rising Power', 343, 4),
	('Brain Snake', 400, 4),
	('Fuel', 429, 5),
    ('Slither', 513, 5),
	('Nummern', 320, 6),
	('Antenna', 337, 6),
	('Of the Hook', 336, 7),
	('Song For Thomas', 508, 7),
	('Justine', 523, 8),
	('Clean Cut Kid', 622, 8);


--запросы для записи Collection:
INSERT INTO collection(year, name) VALUES
    (2022, 'BoneyM The Best'),
    (2011, 'Smokie Createst Hits'),
    (2009, 'Kiss-Createst Hits'),
    (2022, 'The best of AC/DC'),
    (2008, 'Metallica'),
    (2009, 'Kraftwerk- 25 Best Songs'),
    (2019, 'Jevico'),
    (1985, 'Springtime in New Jork');
	

--запросы для записи отношений Аlbumartist:
INSERT INTO albumartist VALUES 
	(1, 1),
	(2, 2),
	(3, 3),
	(4, 4),
	(5, 5),
	(6, 6),
	(7, 7),
	(8, 8);

--запросы для записи отношений Artistgenres:
INSERT INTO artistgenres (id_artist, id_genre) VALUES
	(1, 1),
	(2, 2),
	(2, 3),
	(5, 4),
	(2, 5),
    (2, 6),
    (1, 7),
    (4, 8);
   
   
   
-- запросы для записи отношений Collectiontracks:
INSERT INTO collectiontracks VALUES
	(1, 1),
	(1, 9),
	(2, 2),
	(2, 10),
	(3, 3),
	(3, 11),
	(4, 4),
	(4, 12),
	(5, 5),
	(5, 13),
	(6, 6),
	(6, 14),
	(7, 7),
    (7, 15),
	(8, 8),
	(8, 16);




4. -- SELECT-запросы

--количество исполнителей в каждом жанре;
SELECT g.name, COUNT(a.name) FROM genres g
LEFT JOIN artistgenres ag on g.id = ag.id_genre
LEFT JOIN artists a on ag.id_artist = a.id 
GROUP BY g.name
ORDER by COUNT(a.id) DESC;

--количество треков, вошедших в альбомы 2019-2020 годов;
SELECT  COUNT(id_track) FROM albums a
JOIN tracks t ON t.album = a.id
WHERE year BETWEEN 2019 AND 2021;

--средняя продолжительность треков по каждому альбому;
SELECT a.name, AVG(duration) FROM albums a 
JOIN tracks t on t.album = a.id
GROUP BY a.name
ORDER BY AVG(t.duration);

--все исполнители, которые не выпустили альбомы в 2020 году;
SELECT ar.name FROM artists ar
WHERE ar.name NOT IN (SELECT ar.name FROM artists ar
LEFT JOIN albumartist aa ON ar.id = aa.id_artist 
LEFT JOIN albums a ON a.id = aa.id_album
WHERE a.year = 2020)
ORDER BY ar.name;


--названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
SELECT c.name FROM collection c
JOIN collectiontracks ct ON c.id = ct.id_collection 
JOIN tracks t ON ct.id_track = t.id_track
JOIN albums al ON t.id_track = al.id
JOIN albumartist aa ON al.id = aa.id_album
JOIN artists ar ON aa.id_artist = ar.id
WHERE ar.name = 'Boney M';


--название альбомов, в которых присутствуют исполнители более 1 жанра;
SELECT distinct a.name FROM albums a
JOIN albumartist aa ON a.id = aa.id_album
JOIN artists ar ON aa.id_artist = ar.id
JOIN artistgenres ag ON ar.id = ag.id_artist
GROUP BY a.name, ar.id
HAVING COUNT(id_genre) > 1;


--наименование треков, которые не входят в сборники;
SELECT t.name FROM tracks t
FULL OUTER JOIN collectiontracks ct ON t.id_track = ct.id_track
LEFT JOIN collection c ON ct.id_collection = c.id
WHERE c.id IS null;


--исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
SELECT ar.name, t.duration from artists ar
JOIN albumartist aa ON ar.id = aa.id_artist
JOIN albums al ON aa.id_album = al.id
JOIN tracks t ON al.id = t.id_track
WHERE t.duration = (SELECT MIN(t.duration) FROM tracks t);


--название альбомов, содержащих наименьшее количество треков.		
SELECT a.name FROM albums a
JOIN tracks t ON a.id = t.album
GROUP BY a.id
HAVING COUNT(t.name) = (
	select COUNT(t.name) from tracks t 
	group by t.album  
	order by 1
	limit 1
	);





5. --Группировки, выборки из нескольких таблиц

--количество исполнителей в каждом жанре;
SELECT g.name, COUNT(a.name) FROM genres g
LEFT JOIN artistgenres ag on g.id = ag.id_genre
LEFT JOIN artists a on ag.id_artist = a.id 
GROUP BY g.name
ORDER by COUNT(a.id) DESC;

--количество треков, вошедших в альбомы 2019-2020 годов;
SELECT  COUNT(id_track) FROM albums a
JOIN tracks t ON t.album = a.id
WHERE year BETWEEN 2019 AND 2021;

--средняя продолжительность треков по каждому альбому;
SELECT a.name, AVG(duration) FROM albums a 
JOIN tracks t on t.album = a.id
GROUP BY a.name
ORDER BY AVG(t.duration);

--все исполнители, которые не выпустили альбомы в 2020 году;
SELECT ar.name FROM artists ar
WHERE ar.name NOT IN (SELECT ar.name FROM artists ar
LEFT JOIN albumartist aa ON ar.id = aa.id_artist 
LEFT JOIN albums a ON a.id = aa.id_album
WHERE a.year = 2020)
ORDER BY ar.name;


--названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
SELECT c.name FROM collection c
JOIN collectiontracks ct ON c.id = ct.id_collection 
JOIN tracks t ON ct.id_track = t.id_track
JOIN albums al ON t.id_track = al.id
JOIN albumartist aa ON al.id = aa.id_album
JOIN artists ar ON aa.id_artist = ar.id
WHERE ar.name = 'Boney M';


--название альбомов, в которых присутствуют исполнители более 1 жанра;
SELECT distinct a.name FROM albums a
JOIN albumartist aa ON a.id = aa.id_album
JOIN artists ar ON aa.id_artist = ar.id
JOIN artistgenres ag ON ar.id = ag.id_artist
GROUP BY a.name, ar.id
HAVING COUNT(id_genre) > 1;


--наименование треков, которые не входят в сборники;
SELECT t.name FROM tracks t
FULL OUTER JOIN collectiontracks ct ON t.id_track = ct.id_track
LEFT JOIN collection c ON ct.id_collection = c.id
WHERE c.id IS null;


--исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
SELECT ar.name, t.duration from artists ar
JOIN albumartist aa ON ar.id = aa.id_artist
JOIN albums al ON aa.id_album = al.id
JOIN tracks t ON al.id = t.id_track
WHERE t.duration = (SELECT MIN(t.duration) FROM tracks t);


--название альбомов, содержащих наименьшее количество треков.		
SELECT a.name FROM albums a
JOIN tracks t ON a.id = t.album
GROUP BY a.id
HAVING COUNT(t.name) = (
	select COUNT(t.name) from tracks t 
	group by t.album  
	order by 1
	limit 1
	);




