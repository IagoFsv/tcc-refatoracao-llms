"""Storing the questions of a trivia game in a local database.

Public entry point: run(data). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

import json
import sqlite3
from typing import Dict, List


class Question:
    def __init__(self, question: str, question_data: Dict):
        self.question = question
        self.question_data = question_data


class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def create_questions_table(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")

    def add_question(self, question: Question):
        question_str = question.question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        question_data_str = json.dumps(question.question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace(
            "&#039;", "\'")
        self.c.execute(
            "INSERT INTO questions  (question, questionData)" + " VALUES(\"" + question_str + "\", \"" + question_data_str + "\")")
        self.conn.commit()

    def get_questions(self) -> List[Dict[str, str]]:
        rows = self.conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
        return rows

    def close(self):
        self.conn.close()


def run(data: Dict) -> List[Dict[str, str]]:
    """Stores the questions in data and returns the database rows. Public entry point of this unit."""
    db = Database('Trivia.sqlite')
    db.create_questions_table()
    for i in range(len(data['results'])):
        data['results'][i].pop('type')
        data['results'][i].pop('difficulty')
    for question_data in data['results']:
        question = question_data.pop('question')
        db.add_question(Question(question, question_data))
    rows = db.get_questions()
    db.close()
    return rows
