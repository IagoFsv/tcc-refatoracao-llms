import json
import sqlite3
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Question:
    id: int
    question: str
    questionData: str

@dataclass
class QuestionList:
    results: List[Question] = field(default_factory=list)

def add_question(data: QuestionList):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question in data.results:
        question.question = question.question.replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        question.questionData = json.dumps(question.questionData).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        c.execute(
            "INSERT INTO questions  (question, questionData)" 
            + " VALUES(\"" + question.question + "\", \"" + question.questionData + "\")")
    conn.commit()
    conn.close()


def executar(data: Dict) -> List:
    """Grava as perguntas de data e devolve as linhas do banco. Ponto de entrada publico desta unidade."""
    question_list = QuestionList()
    for result in data['results']:
        result.pop('type')
        result.pop('difficulty')
        question = Question(id=result.pop('id'), question=result.pop('question'), questionData=result)
        question_list.results.append(question)
    add_question(question_list)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
