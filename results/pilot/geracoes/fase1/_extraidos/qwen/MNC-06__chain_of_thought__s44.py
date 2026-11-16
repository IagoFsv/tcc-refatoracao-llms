import json
import sqlite3

def clean_question_data(question_data):
    """Limpa os dados da pergunta para evitar problemas de escape."""
    question_data.pop('type')
    question_data.pop('difficulty')
    question_data['question'] = question_data['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
    return question_data

def insert_question_data(question, question_data):
    """Insere uma pergunta no banco de dados."""
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    questionData = json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
    c.execute(
        "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)", (question, questionData))
    conn.commit()
    conn.close()

def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    for question_data in data['results']:
        cleaned_data = clean_question_data(question_data)
        insert_question_data(cleaned_data['question'], cleaned_data)
    
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
