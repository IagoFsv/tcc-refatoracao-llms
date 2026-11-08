from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Question:
    id: int
    question: str
    question_data: Dict

@dataclass
class Result:
    type: str
    difficulty: str
    question: str
    question_data: Dict

@dataclass
class TriviaData:
    results: List[Result]

def add_question(data: TriviaData):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for result in data.results:
        question = result.question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        question_data = json.dumps(result.question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(\"" + question + "\", \"" + question_data + "\")")

    conn.commit()
    conn.close()

def executar(data: TriviaData):
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
