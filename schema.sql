CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password_hash TEXT );

CREATE TABLE posts (
id INTEGER PRIMARY KEY,
poster_id INTEGER REFERENCES users,
title TEXT,
body TEXT );

CREATE TABLE comments (
id INTEGER PRIMARY KEY,
commenter_id INTEGER REFERENCES users,
post_id INTEGER REFERENCES posts,
comment TEXT );

CREATE TABLE saved (
id INTEGER PRIMARY KEY,
post_id INTEGER REFERENCES posts,
saver_id INTEGER REFERENCES users);

CREATE TABLE classes (
id INTEGER PRIMARY KEY,
name TEXT,
value TEXT );

CREATE TABLE post_classes (
id INTEGER PRIMARY KEY,
post_id REFERENCES posts,
name TEXT,
value TEXT );

INSERT INTO classes (name, value) VALUES ('tyyli', 'asiallinen');
INSERT INTO classes (name, value) VALUES ('tyyli', 'asiaton');
INSERT INTO classes (name, value) VALUES ('tyyli', 'kysymys');

INSERT INTO classes (name, value) VALUES ('aihe', 'uutiset');
INSERT INTO classes (name, value) VALUES ('aihe', 'viihde');
INSERT INTO classes (name, value) VALUES ('aihe', 'ihmiset');
INSERT INTO classes (name, value) VALUES ('aihe', 'historia');
INSERT INTO classes (name, value) VALUES ('aihe', 'urheilu');
INSERT INTO classes (name, value) VALUES ('aihe', 'kirjallisuus');
INSERT INTO classes (name, value) VALUES ('aihe', 'tiede');
INSERT INTO classes (name, value) VALUES ('aihe', 'eläimet');
INSERT INTO classes (name, value) VALUES ('aihe', 'pilkkiminen');
INSERT INTO classes (name, value) VALUES ('aihe', 'ruoka ja juoma');
INSERT INTO classes (name, value) VALUES ('aihe', 'musiikki');
INSERT INTO classes (name, value) VALUES ('aihe', 'arki');
INSERT INTO classes (name, value) VALUES ('aihe', 'MUU');