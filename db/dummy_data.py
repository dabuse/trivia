#!/usr/bin/env python3

import sqlite3
import csv
import hasher

conn = sqlite3.connect('trivia.db')
cur = conn.cursor()
difficulties = {"easy":0, "medium":1, "hard":2}
with open("categories.csv") as f:
    question_id = 1
    for i, category in enumerate(csv.DictReader(f)):
        cat_id = i+1
        # add the category to the database
        cur.execute("INSERT INTO categories VALUES(?, ?)", (cat_id, category["Category"]))

        with open(category["CSV File"]) as fc:
            for question in csv.DictReader(fc):
                # add the question
                # question id, question text, times answered, times correct, category id, difficulty
                cur.execute('INSERT INTO questions VALUES(?, ?, 0, 0, ?, ?)', (question_id, question['Question'], cat_id, difficulties[question['Difficulty']]))
                # answer id, question id, is the correct answer, answer text
                # add the correct answer
                cur.execute('INSERT INTO answers VALUES(NULL, ?, 1, ?)', (question_id, question['Correct Answer']))
                # add the incorrect answers
                for j in range(1, 4):
                    cur.execute('INSERT INTO answers VALUES(NULL, ?, 0, ?)', (question_id, question['Wrong Answer %d' % j]))
                question_id += 1

def add_user(username, password, email):
    salt = hasher.new_salt()
    cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?);', (username, hasher.hash(password, salt), salt, email))

add_user('awesomealex', 'password', 'dummy@example.com')
add_user('fantasticfeddie', 'pword', 'dummy1@example.com')
add_user('amazingaretha', 'admin', 'dummy2@example.com')

cur.execute('INSERT INTO flags VALUES(NULL,3);')
cur.execute('INSERT INTO flags VALUES(NULL,3);')
cur.execute('INSERT INTO flags VALUES(NULL,3);')

cur.execute('INSERT INTO scores VALUES(1,2,20,19);')
cur.execute('INSERT INTO scores VALUES(2,1,18,4);')
cur.execute('INSERT INTO scores VALUES(3,1,20,20);')

conn.commit()
