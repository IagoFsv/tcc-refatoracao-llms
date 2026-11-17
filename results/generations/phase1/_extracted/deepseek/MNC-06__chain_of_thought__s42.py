import json
import sqlite3


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for i in range(len(data['results'])):
        question_data = data['results'][i]
        question_data.pop('type')
        question_data.pop('difficulty')
        question = question_data['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        question_data.pop('question')
        question_data = json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        c.execute(
            "INSERT INTO questions  (question, questionData)" + " VALUES(\"" + question + "\", \"" + question_data + "\")")
    conn.commit()
    conn.close()


def run(data):
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    rows = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return rows
