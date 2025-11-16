CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password_hash TEXT );

CREATE TABLE items (
id INTEGER PRIMARY KEY,
poster_id INTEGER REFERENCES users,
title TEXT,
body TEXT );