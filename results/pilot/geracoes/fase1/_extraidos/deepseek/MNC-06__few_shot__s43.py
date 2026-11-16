import json
import sqlite3


class Question:
    def __init__(self, data):
        self.data = data
        self.data.pop('type')
        self.data.pop('difficulty')

    @property
    def question(self):
        question = self.data['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        return question

    @property
    def question_data(self):
        question_data = json.dumps(self.data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        return question_data


class QuestionsDB:
    def __init__(self, db_name='Trivia.sqlite'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")

    def add_question(self, question):
        self.c.execute(
            "INSERT INTO questions  (question, questionData)" + " VALUES(\"" + question.question + "\", \"" + question.question_data + "\")")
        self.conn.commit()

    def get_questions(self):
        rows = self.conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
        self.conn.close()
        return rows


def executar(data):
    db = QuestionsDB()
    for question_data in data['results']:
        question = Question(question_data)
        db.add_question(question)
    return db.get_questions()
