import json
import sqlite3

def create_table():
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    conn.commit()
    return conn

def insert_question(conn, data):
    c = conn.cursor()
    for i in range(len(data['results'])):
        data['results'][i].pop('type')
        data['results'][i].pop('difficulty')
        question = data['results'][i]['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        data['results'][i].pop('question')
        questionData = json.dumps(data['results'][i]).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        c.execute("INSERT INTO questions  (question, questionData) VALUES(?, ?)", (question, questionData))
    conn.commit()

def executar(data):
    conn = create_table()
    insert_question(conn, data)
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
