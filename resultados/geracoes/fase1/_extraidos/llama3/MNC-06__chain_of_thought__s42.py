import json
import sqlite3


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    questions_to_insert = []
    for question_data in data['results']:
        data_to_insert = {}
        data_to_insert['question'] = question_data['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        data_to_insert['questionData'] = json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        questions_to_insert.append(data_to_insert)
    c.executemany("INSERT INTO questions (question, questionData) VALUES (?, ?)", [(q['question'], q['questionData']) for q in questions_to_insert])
    conn.commit()
    conn.close()


def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
