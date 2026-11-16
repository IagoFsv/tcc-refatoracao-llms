from dataclasses import dataclass

@dataclass
class Question:
    question: str
    question_data: dict

@dataclass
class QuestionData:
    results: list[dict]

@dataclass
class TriviaData:
    results: list[Question]

def add_question(data: TriviaData):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for question in data.results:
        question_data = json.dumps(question.results).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;", "\'\'")
        c.execute("INSERT INTO questions (question, questionData)" "VALUES (?, ?)", (question.question, question_data))
    conn.commit()
    conn.close()

def executar(data: TriviaData):
    add_question(data)
    conn = sqlite3.connect('Trivia.sqlite')
    linhas = conn.execute("SELECT id, question, questionData FROM questions ORDER BY id").fetchall()
    conn.close()
    return linhas
