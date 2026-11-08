import json
import sqlite3


def clean_question(question_data):
    """Limpa e formata os dados da pergunta."""
    question_data.pop('type')
    question_data.pop('difficulty')
    return question_data


def format_question_data(question_data):
    """Formata os dados da pergunta para inserção no banco de dados."""
    return json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")


def add_question_to_database(question, question_data):
    """Adiciona uma pergunta ao banco de dados."""
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    c.execute(
        "INSERT INTO questions (question, questionData)" + " VALUES(?, ?)", (question, question_data))
    conn.commit()
    conn.close()


def add_question(data):
    """Adiciona múltiplas perguntas ao banco de dados."""
    for question_data in data['results']:
        cleaned_data = clean_question(question_data)
        formatted_data = format_question_data(cleaned_data)
        question = cleaned_data['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                          "\'\'")
        cleaned_data.pop('question')
        add_question_to_database(question, formatted_data)


def executar(data):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada público desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
