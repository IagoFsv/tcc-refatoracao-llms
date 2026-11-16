import json
import sqlite3

@dataclass
class Question:
    id: int
    question: str
    question_data: str

def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question in data['results']:
        question.pop('type')
        question.pop('difficulty')
        question['question'] = question['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        question_data = json.dumps(question).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        c.execute("INSERT INTO questions (question, questionData)" " VALUES (?, ?)", (question['question'], question_data))
    conn.commit()
    conn.close()

def executar(data):
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
