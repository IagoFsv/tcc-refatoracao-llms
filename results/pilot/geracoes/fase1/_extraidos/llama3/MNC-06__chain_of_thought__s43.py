import json
import sqlite3


def format_question(question):
    """Formata uma pergunta para armazenamento no banco"""
    return question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")


def format_question_data(question_data):
    """Formata os dados de uma pergunta para armazenamento no banco"""
    return json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question in data['results']:
        question.pop('type')
        question.pop('difficulty')
        question.pop('question')
        formatted_question = format_question(question['question'])
        formatted_question_data = format_question_data(question)
        c.execute("INSERT INTO questions (question, questionData)" "VALUES (?, ?)", (formatted_question, formatted_question_data))
    conn.commit()
    conn.close()


def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
