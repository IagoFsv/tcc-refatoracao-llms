import json
import sqlite3


def clean_question_data(question_data):
    question_data.pop('type')
    question_data.pop('difficulty')
    return question_data


def format_question(question):
    return question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")


def format_question_data(question_data):
    return json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for item in data['results']:
        cleaned_data = clean_question_data(item)
        formatted_question = format_question(item['question'])
        formatted_data = format_question_data(cleaned_data)
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)", (formatted_question, formatted_data))

    conn.commit()
    conn.close()


def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
