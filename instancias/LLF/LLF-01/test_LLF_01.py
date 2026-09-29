"""Testes da instancia LLF-01: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar as lambdas por funcoes
nomeadas, lacos ou metodos vetorizados; o que nao pode mudar e a lista de
cidades devolvida, uma por descricao, na mesma ordem, e o erro diante de
descricao curta demais.

Os testes fixam o comportamento como ele e, inclusive o defeito do original:
cidade de duas palavras ("Abu Dhabi") nunca e encontrada.
"""

import pytest

from LLF_01 import executar

CIDADES = ["Dubai", "Sharjah", "Abu Dhabi", "London"]


def test_tipico_ultima_palavra_penultima_ou_unknown():
    descricoes = [
        "Lulu Hypermarket Dubai",       # ultima palavra e cidade
        "Starbucks Sharjah AE",         # so a penultima e cidade
        "Netflix Subscription Online",  # nenhuma das duas
        "Transfer London Dubai",        # as duas: vale a ultima
    ]

    assert executar(descricoes, CIDADES) == ["Dubai", "Sharjah", "Unknown", "Dubai"]


def test_borda_maiusculas_cidade_composta_e_descricao_de_uma_palavra():
    descricoes = [
        "AMAZON LONDON",              # descricao toda em maiusculas
        "payment dubai",              # descricao toda em minusculas
        "Emirates Palace Abu Dhabi",  # cidade de duas palavras: nunca achada
        "Dubai",                      # uma palavra so, mas e cidade: sem erro
    ]
    cidades = ["DUBAI", "london", "Abu Dhabi"]  # lista com caixa misturada

    assert executar(descricoes, cidades) == ["London", "Dubai", "Unknown", "Dubai"]


def test_invalido_descricao_de_uma_palavra_que_nao_e_cidade():
    with pytest.raises(IndexError):
        executar(["Lulu Hypermarket Dubai", "Netflix"], CIDADES)
