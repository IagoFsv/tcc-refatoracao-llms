import json
import sqlite3


def create_questions_table():
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    conn.commit()
    conn.close()


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    for i in range(len(data['results'])):
        data['results'][i].pop('type')
        data['results'][i].pop('difficulty')
    conn.close()
    return data


def parse_question_data(data):
    question = data['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
    data.pop('question')
    questionData = json.dumps(data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
    return question, questionData


def insert_into_questions_table(question, questionData):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(f"INSERT INTO questions  (question, questionData)" + f" VALUES(\"{question}\", \"{questionData}\")")
    conn.commit()
    conn.close()


def executar(data):
    create_questions_table()
    data = add_question(data)
    for question_data in data['results']:
        question, questionData = parse_question_data(question_data)
        insert_into_questions_table(question, questionData)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
