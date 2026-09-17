"""
Montagem dos prompts enviados aos modelos.

Tres tecnicas (Role Prompting, Few-Shot e Chain-of-Thought) com o mesmo nucleo
de tarefa; o que varia entre elas e apenas a camada da tecnica. Os textos
aprovados vivem em prompts/*.txt e sao carregados verbatim: este modulo
preenche os campos e monta a mensagem, nunca reescreve o enunciado.

Todas as tecnicas viram UMA unica mensagem de papel "user", sem mensagem de
"system". Isso e deliberado: se a persona do Role fosse para o "system" e as
outras duas nao tivessem essa mensagem, a estrutura da conversa passaria a
variar junto com o texto, e a tecnica de prompt deixaria de ser o unico fator
manipulado. Sem "system" tambem nao existe contexto oculto injetado, que foi
exatamente a critica da banca a interface de chat.
"""

import functools
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
DIR_PROMPTS = RAIZ / "prompts"

TECNICAS = ("role", "few_shot", "chain_of_thought")


@functools.lru_cache(maxsize=None)
def catalogo():
    """Devolve o catalogo dos smells (nome, tecnica e par de exemplo)."""
    with open(DIR_PROMPTS / "smells.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


@functools.lru_cache(maxsize=None)
def template(tecnica):
    """Devolve o texto bruto do prompt de uma tecnica."""
    if tecnica not in TECNICAS:
        raise ValueError(
            f"Tecnica desconhecida: {tecnica!r}. Esperado um de {TECNICAS}."
        )
    return (DIR_PROMPTS / f"{tecnica}.txt").read_text(encoding="utf-8")


def montar(tecnica, smell, codigo):
    """Monta as mensagens de uma geracao.

    tecnica: "role", "few_shot" ou "chain_of_thought".
    smell:   chave do catalogo ("LM", "LPL", "LLF" ou "MNC").
    codigo:  o codigo original da instancia, ja adaptado.

    Devolve a lista de mensagens no formato que cliente.chamar_modelo espera.
    """
    smells = catalogo()
    if smell not in smells:
        raise ValueError(
            f"Smell desconhecido: {smell!r}. Esperado um de {tuple(smells)}."
        )
    s = smells[smell]

    # O exemplo do few-shot e sempre do mesmo smell da instancia, entao
    # {smell}/{technique} e {smell_exemplo}/{technique_exemplo} saem da mesma
    # entrada do catalogo. Os campos de exemplo sobram nos outros dois
    # templates; format() ignora chave nao usada.
    texto = template(tecnica).format(
        smell=s["nome"],
        technique=s["tecnica"],
        code=codigo,
        smell_exemplo=s["nome"],
        technique_exemplo=s["tecnica"],
        codigo_exemplo_antes=s["exemplo_antes"],
        codigo_exemplo_depois=s["exemplo_depois"],
    )
    return [{"role": "user", "content": texto}]
