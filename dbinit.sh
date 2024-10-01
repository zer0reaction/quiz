#!/bin/bash

mkdir data
touch data/users.db
touch data/quiz.db

sqlite3 data/users.db \
"create table state (
    id int primary key,
    state text
)"

sqlite3 data/users.db \
"create table questions (
    id int,
    number int,
    status text
)"

sqlite3 data/quiz.db \
"create table questions (
    label text,
    photo blob,
    question text,
    answer text,
    info text,
    info_photo blob
)"

sqlite3 data/quiz.db \
"create table hints (
    question_number int,
    hint_number int,
    hint text,
    photo blob
)"
