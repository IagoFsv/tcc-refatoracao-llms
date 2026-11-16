"""Tests for instance MNC-06: they pin the observable behavior of run().

Only run() is imported. The test runs in a temporary folder, where the
Trivia.sqlite database is created. The refactoring may reorganize the loop
and the access to the dictionaries; what must not change is what gets stored
(the question and the rest of the data as JSON, without type and difficulty,
in input order) and the error on a question without the expected fields.

The tests pin the behavior as it is, including the defect of the original:
in the question, &#039; becomes two single quotes, not one.
"""

import pytest

from MNC_06 import run


def question(text, answer):
    return {
        "type": "multiple",
        "difficulty": "easy",
        "category": "Geo",
        "question": text,
        "correct_answer": answer,
    }


def test_typical_questions_stored_without_type_and_difficulty(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {"results": [question("Capital of Norway?", "Oslo"), question("Largest planet?", "Jupiter")]}

    assert run(data) == [
        (1, "Capital of Norway?", '{"category": "Geo", "correct_answer": "Oslo"}'),
        (2, "Largest planet?", '{"category": "Geo", "correct_answer": "Jupiter"}'),
    ]


def test_edge_entities_quotes_and_existing_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run({"results": [question("First?", "Yes")]})

    rows = run({"results": [question("Who said &quot;I&quot; and &#039;you&#039;?", 'The "author"')]})

    assert rows[1] == (
        2,
        "Who said \"I\" and ''you''?",
        '{"category": "Geo", "correct_answer": "The \\"author\\""}',
    )
    assert run({"results": []}) == rows  # an empty list stores nothing


def test_invalid_question_without_type(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(KeyError):
        run({"results": [{"difficulty": "easy", "question": "No type?"}]})
