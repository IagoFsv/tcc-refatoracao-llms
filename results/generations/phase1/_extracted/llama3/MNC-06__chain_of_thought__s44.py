"""Storing the questions of a trivia game in a local database.

Public entry point: run(data). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

import json
import sqlite3

class Question:
    def __init__(self, question, question_data):
        self.question = question
        self.question_data = question_data

def process_question_data(data):
    questions = []
    for result in data['results']:
        question = result['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        question_data = json.dumps(result).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        questions.append(Question(question, question_data))
    return questions

def add_questions_to_db(questions):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question in questions:
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(\"" + question.question + "\", \"" + question.question_data + "\")")
    conn.commit()
    conn.close()

def run(data):
    """Stores the questions in data and returns the database rows. Public entry point of this unit."""
    questions = process_question_data(data)
    add_questions_to_db(questions)
    conn = sqlite3.connect('Trivia.sqlite')
    rows = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return rows
