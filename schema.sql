CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password_hash TEXT );

CREATE TABLE items (
id INTEGER PRIMARY KEY,
poster_id INTEGER REFERENCES users,
title TEXT,
body TEXT );

CREATE TABLE comments (
id INTEGER PRIMARY KEY,
commenter_id INTEGER REFERENCES users,
post_id INTEGER REFERENCES items,
comment TEXT );