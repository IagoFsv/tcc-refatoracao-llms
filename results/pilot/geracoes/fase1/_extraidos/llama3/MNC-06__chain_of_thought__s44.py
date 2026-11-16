import json
import sqlite3


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    # add and id for each question
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for i in range(len(data['results'])):
        data['results'][i] = _prepare_question(data['results'][i])
    _insert_questions(c, data['results'])
    conn.commit()
    conn.close()


def _prepare_question(question):
    question.pop('type')
    question.pop('difficulty')
    question['question'] = question['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
    return question


def _insert_questions(c, questions):
    for question in questions:
        questionData = json.dumps(question).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(\"" + question['question'] + "\", \"" + questionData + "\")")


def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
