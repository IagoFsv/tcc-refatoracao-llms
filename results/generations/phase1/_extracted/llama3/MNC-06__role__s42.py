"""Storing the questions of a trivia game in a local database.

Public entry point: run(data). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

import json
import sqlite3


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    # add and id for each question
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question_data in data['results']:
        question_data = process_question_data(question_data)
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)", (question_data['question'], question_data['questionData']))

    conn.commit()
    conn.close()


def process_question_data(question_data):
    question_data.pop('type')
    question_data.pop('difficulty')
    question = question_data['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
    question_data.pop('question')
    question_data['question'] = question
    question_data['questionData'] = json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
    return question_data


def run(data):
    """Stores the questions in data and returns the database rows. Public entry point of this unit."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    rows = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return rows
