"""Testes da instancia MNC-05: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode reorganizar o acesso aos
dicionarios; o que nao pode mudar e o aplicativo devolvido (servicos
indexados pelo nome do conteiner, sem a chave name, sem a lista containers,
demais chaves intactas) e o erro diante de conteiner sem nome.
"""

import pytest

from MNC_05 import executar


def conteiner(nome, imagem):
    return {"name": nome, "image": imagem}


def test_tipico_conteineres_viram_servicos_nomeados():
    app = {"id": "loja", "containers": [conteiner("web", "nginx"), conteiner("db", "postgres")]}

    assert executar(app) == {
        "id": "loja",
        "services": {"web": {"image": "nginx"}, "db": {"image": "postgres"}},
    }


def test_borda_nome_repetido_fica_o_ultimo_e_lista_vazia():
    app = {"containers": [conteiner("web", "nginx"), conteiner("web", "caddy")]}
    assert executar(app) == {"services": {"web": {"image": "caddy"}}}

    assert executar({"containers": []}) == {"services": {}}


def test_invalido_conteiner_sem_nome():
    with pytest.raises(KeyError):
        executar({"containers": [{"image": "nginx"}]})
