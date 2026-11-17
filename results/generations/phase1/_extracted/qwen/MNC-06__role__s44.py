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
    for item in data['results']:
        clean_item = remove_unnecessary_fields(item)
        question = clean_item['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                          "\'\'")
        questionData = json.dumps(clean_item).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                              "\'")
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(\"" + question + "\", \"" + questionData + "\")")

    conn.commit()
    conn.close()


def remove_unnecessary_fields(item):
    item.pop('type')
    item.pop('difficulty')
    item.pop('question')
    return item


def run(data):
    """Stores the questions in data and returns the database rows. Public entry point of this unit."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    rows = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return rows
