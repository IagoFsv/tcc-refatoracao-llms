import json
import sqlite3

def process_question_data(question_data):
    question_data.pop('type')
    question_data.pop('difficulty')
    question_data.pop('question')
    return json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")

def add_question_to_db(question, question_data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    c.execute(
        "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)",
        (question, question_data)
    )
    conn.commit()
    conn.close()

def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    for result in data['results']:
        question = result['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        question_data = process_question_data(result)
        add_question_to_db(question, question_data)

    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
