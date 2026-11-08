import json
import sqlite3

def add_question(question_data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    question = clean_question(question_data['question'])
    question_data.pop('question')
    question_data.pop('type')
    question_data.pop('difficulty')
    questionData = json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
    c.execute(
        "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)", (question, questionData))
    conn.commit()
    conn.close()

def clean_question(question):
    return question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")

def executar(data):
    for question in data['results']:
        add_question(question)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
