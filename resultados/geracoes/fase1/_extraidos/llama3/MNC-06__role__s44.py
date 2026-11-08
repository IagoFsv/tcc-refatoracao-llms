import json
import sqlite3


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    questions = []
    for result in data['results']:
        del result['type']
        del result['difficulty']
        question = result['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        del result['question']
        question_data = json.dumps(result).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        questions.append((question, question_data))
    c.executemany("INSERT INTO questions (question, questionData) VALUES (?, ?)", questions)
    conn.commit()
    conn.close()


def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
