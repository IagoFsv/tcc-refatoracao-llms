"""Testes da instancia MNC-06: fixam o comportamento observavel de executar().

So executar() e importado. O teste roda numa pasta temporaria, onde o banco
Trivia.sqlite e criado. A refatoracao pode reorganizar o laco e o acesso aos
dicionarios; o que nao pode mudar e o que fica gravado (pergunta e o resto
dos dados em JSON, sem type e difficulty, na ordem de entrada) e o erro
diante de pergunta sem os campos esperados.

Os testes fixam o comportamento como ele e, inclusive o defeito do original:
na pergunta, &#039; vira duas aspas simples, nao uma.
"""

import pytest

from MNC_06 import executar


def pergunta(texto, resposta):
    return {
        "type": "multiple",
        "difficulty": "easy",
        "category": "Geo",
        "question": texto,
        "correct_answer": resposta,
    }


def test_tipico_perguntas_gravadas_sem_tipo_e_dificuldade(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {"results": [pergunta("Capital da Noruega?", "Oslo"), pergunta("Maior planeta?", "Jupiter")]}

    assert executar(data) == [
        (1, "Capital da Noruega?", '{"category": "Geo", "correct_answer": "Oslo"}'),
        (2, "Maior planeta?", '{"category": "Geo", "correct_answer": "Jupiter"}'),
    ]


def test_borda_entidades_aspas_e_banco_ja_existente(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    executar({"results": [pergunta("Primeira?", "Sim")]})

    linhas = executar({"results": [pergunta("Quem disse &quot;eu&quot; e &#039;tu&#039;?", 'O "autor"')]})

    assert linhas[1] == (
        2,
        "Quem disse \"eu\" e ''tu''?",
        '{"category": "Geo", "correct_answer": "O \\"autor\\""}',
    )
    assert executar({"results": []}) == linhas  # lista vazia nao grava nada


def test_invalido_pergunta_sem_tipo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(KeyError):
        executar({"results": [{"difficulty": "easy", "question": "Sem tipo?"}]})
