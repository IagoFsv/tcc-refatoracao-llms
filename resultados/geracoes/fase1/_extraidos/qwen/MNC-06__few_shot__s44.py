import json
import sqlite3
from typing import List, Dict

def add_question(data: Dict) -> None:
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    
    for item in data['results']:
        item.pop('type')
        item.pop('difficulty')
        question = item['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        item.pop('question')
        questionData = json.dumps(item).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'")
        c.execute("INSERT INTO questions (question, questionData) VALUES(?, ?)", (question, questionData))

    conn.commit()
    conn.close()

def executar(data: Dict) -> List:
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
