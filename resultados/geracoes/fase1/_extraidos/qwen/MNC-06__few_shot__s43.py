import json
import sqlite3
from dataclasses import dataclass, field
from typing import List

@dataclass
class QuestionData:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]

@dataclass
class Question:
    id: int = None
    question: str = None
    question_data: QuestionData = None

def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for item in data['results']:
        question_data = QuestionData(**item)
        question = question_data.question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                  "\'")
        question_data = json.dumps(question_data).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                            "\'")
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(\"" + question + "\", \"" + question_data + "\")")
    conn.commit()
    conn.close()

def executar(data):
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
