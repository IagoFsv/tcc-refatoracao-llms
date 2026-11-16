import json
import sqlite3


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for i in range(len(data['results'])):
        data['results'][i].pop('type')
        data['results'][i].pop('difficulty')
        question = data['results'][i]['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                         "\'\'")
        data['results'][i].pop('question')
        questionData = json.dumps(data['results'][i]).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                               "\'")
        c.execute(
            "INSERT INTO questions  (question, questionData)" + " VALUES(\"" + question + "\", \"" + questionData + "\")")

    conn.commit()
    conn.close()


def execute(data):
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    rows = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return rows
