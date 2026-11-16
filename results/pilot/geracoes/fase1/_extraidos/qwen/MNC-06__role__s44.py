import json
import sqlite3

def prepare_question_data(data):
    for i in range(len(data['results'])):
        data['results'][i].pop('type')
        data['results'][i].pop('difficulty')
        question = data['results'][i]['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        data['results'][i].pop('question')
        data['results'][i]['question'] = question
        data['results'][i]['questionData'] = json.dumps(data['results'][i]).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
    return data

def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question_data in data['results']:
        c.execute("INSERT INTO questions (question, questionData) VALUES(?, ?)", (question_data['question'], question_data['questionData']))
    conn.commit()
    conn.close()

def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    data = prepare_question_data(data)
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
