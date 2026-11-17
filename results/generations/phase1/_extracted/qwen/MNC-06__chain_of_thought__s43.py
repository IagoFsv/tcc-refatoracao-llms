"""Storing the questions of a trivia game in a local database.

Public entry point: run(data). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

import json
import sqlite3


def extract_question_data(question_data):
    """Extracts and cleans the question data from the input dictionary."""
    cleaned_data = question_data.copy()
    cleaned_data.pop('type')
    cleaned_data.pop('difficulty')
    return cleaned_data


def format_question(question):
    """Formats the question by escaping special characters."""
    return question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")


def format_question_data(question_data):
    """Formats the question data by escaping special characters and converting to JSON."""
    return json.dumps(format_question_data(extract_question_data(question_data))).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    # add and id for each question
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question in data['results']:
        question = format_question(question['question'])
        question_data = format_question_data(question)
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)", (question, question_data))

    conn.commit()
    conn.close()


def run(data):
    """Stores the questions in data and returns the database rows. Public entry point of this unit."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    rows = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return rows
