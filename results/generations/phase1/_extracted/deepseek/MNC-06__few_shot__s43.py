from typing import Dict, List
import json
import sqlite3


class Question:
    def __init__(self, question: str, question_data: Dict):
        self.question = question
        self.question_data = question_data


class QuestionsDatabase:
    def __init__(self, db_name: str = 'Trivia.sqlite'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")

    def add_question(self, data: Dict):
        for i in range(len(data['results'])):
            data['results'][i].pop('type')
            data['results'][i].pop('difficulty')
            question = data['results'][i]['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                               "\'\'")
            data['results'][i].pop('question')
            question_data = json.dumps(data['results'][i]).replace("\"", "\"\"").replace("&quot;", "\"\"").replace(
                "&#039;", "\'")
            self.c.execute(
                "INSERT INTO questions  (question, questionData)" + " VALUES(\"" + question + "\", \"" + question_data + "\")")
        self.conn.commit()

    def run(self, data: Dict):
        """Stores the questions in data and returns the database rows. Public entry point of this unit."""
        self.add_question(data)
        rows = self.conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
        self.conn.close()
        return rows
