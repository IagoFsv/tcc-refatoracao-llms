import json
import sqlite3


def clean_question(question):
    # Remove unwanted characters and prepare the question for insertion
    return question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")


def prepare_data(question_data):
    # Prepare the data for insertion, removing unwanted fields and converting to JSON
    question_data.pop('type')
    question_data.pop('difficulty')
    return json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")


def insert_question(conn, question, question_data):
    # Insert the question and its data into the database
    c = conn.cursor()
    c.execute(
        "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)",
        (question, question_data))


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    # Create the table if it doesn't exist
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    
    for result in data['results']:
        question = clean_question(result['question'])
        question_data = prepare_data(result)
        insert_question(conn, question, question_data)
    
    conn.commit()
    conn.close()


def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
