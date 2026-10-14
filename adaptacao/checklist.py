"""Checklist automatico da adaptacao das instancias (etapa 2).

Para cada instancia, confere:
  diff          o trecho do original (funcao envolvente inteira) aparece
                identico, uma unica vez, na unidade;
  pysmell       as deteccoes dos 4 smells do estudo dentro do trecho sao as
                mesmas do original, e nao ha nenhuma fora dele (andaime);
  pytest        exatamente 3 testes (tipico, borda, invalido), todos passando;
  mutacao       mutantes gerados por regras fixas, so dentro do trecho; pelo
                menos um tem que ser morto pelos testes;
  neutralidade  fora do trecho, a unidade nao cita estudo, smell, metrica nem
                origem do codigo;
  contrato      executar() existe, a docstring declara o contrato e o
                origem.json tem os campos obrigatorios.

Uso:
    python -m adaptacao.checklist                  # todas as instancias
    python -m adaptacao.checklist LLF-01 MNC-01    # so essas
    --sem-mutacao    pula a mutacao (mais rapido)

Grava instancias/checklist.csv, uma linha por instancia. Linhas de
instancias que nao foram rodadas agora sao mantidas como estavam.
"""

import argparse
import ast
import csv
import datetime
import importlib.metadata
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
import warnings
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dados.pysmell.detectar import detectar_arquivo

RAIZ = Path(__file__).resolve().parent.parent
SELECAO = RAIZ / "dados" / "selecao" / "instancias_zhang.csv"
DATASET = RAIZ / "dados" / "dataset_zhang" / "dataset" / "files"
INSTANCIAS = RAIZ / "instancias"
TABELA = INSTANCIAS / "checklist.csv"

PACOTES = ("pytest", "pandas", "tqdm", "numpy", "scikit-image", "scipy")
TIMEOUT_MUTANTE = 30  # segundos; mutante que estoura o tempo conta como morto
PREFIXOS_TESTE = ("test_tipico_", "test_borda_", "test_invalido_")
CONTRATO = ("Ponto de entrada publico: executar(", "Nao altere o nome nem a assinatura")
CAMPOS_ORIGEM = ("id", "smell", "arquivo", "ponto_de_entrada",
                 "comportamento_fixado", "validacao_da_adaptacao")
# Palavras que, fora do trecho, dariam pista ao modelo sobre o estudo ou a
# origem do codigo. Casam no inicio da palavra ("refator" pega "refatorar").
PISTAS = re.compile(
    r"\b(smell|refator|refactor|pysmell|metrica|estudo|tcc|copilot|chatgpt|"
    r"gpt|llm|limiar|zhang)", re.IGNORECASE)

COLUNAS = ["id", "smell", "aprovada", "diff", "pysmell", "pytest", "mutacao",
           "mutantes", "neutralidade", "contrato", "mutantes_vivos",
           "observacoes", "data", "ambiente"]


# ---------------------------------------------------------------- leitura

def _ler_linhas(caminho):
    """Linhas do arquivo, sem o fim de linha. Respeita o encoding declarado."""
    try:
        with tokenize.open(caminho) as fh:
            return fh.read().splitlines()
    except (UnicodeDecodeError, SyntaxError):
        return Path(caminho).read_text(encoding="latin-1").splitlines()


def _parse(texto):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast.parse(texto)


def _selecao():
    with open(SELECAO, encoding="utf-8", newline="") as fh:
        return {linha["id"]: linha for linha in csv.DictReader(fh)}


def _caminhos(inst):
    pasta = INSTANCIAS / inst["smell"] / inst["id"]
    base = inst["id"].replace("-", "_")
    return pasta, pasta / f"{base}.py", pasta / f"test_{base}.py", pasta / "origem.json"


def _ambiente():
    versoes = [f"Python {platform.python_version()}"]
    for pacote in PACOTES:
        try:
            versoes.append(f"{pacote} {importlib.metadata.version(pacote)}")
        except importlib.metadata.PackageNotFoundError:
            versoes.append(f"{pacote} ausente")
    return "; ".join(versoes)


# ---------------------------------------------------------------- 1. diff

def _trecho_original(inst, origem):
    """(inicio, fim, linhas) do trecho no original, linhas contadas de 1.

    Funcao: do primeiro decorador ate a ultima linha do corpo, achada pela
    linha do def. Codigo de modulo (<modulo>) nao tem no de funcao; o
    intervalo vem de trecho_linhas no origem.json.
    """
    linhas = _ler_linhas(DATASET / inst["arquivo"])
    if "trecho_linhas" in origem:
        ini, fim = origem["trecho_linhas"]
        return ini, fim, linhas[ini - 1:fim]
    if inst["funcao"] == "<modulo>":
        raise ValueError("instancia <modulo>: defina trecho_linhas no origem.json")
    alvo = int(inst["linha_funcao"])
    for no in ast.walk(_parse("\n".join(linhas))):
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)) and no.lineno == alvo:
            ini = min([no.lineno] + [d.lineno for d in no.decorator_list])
            return ini, no.end_lineno, linhas[ini - 1:no.end_lineno]
    raise ValueError(f"nenhuma funcao comeca na linha {alvo} do original")


def _localizar(bloco, linhas):
    """Linhas (1-based) onde o bloco comeca dentro de `linhas`."""
    n = len(bloco)
    return [i + 1 for i in range(len(linhas) - n + 1) if linhas[i:i + n] == bloco]


# ---------------------------------------------------------------- 2. pysmell

def _deteccoes(caminho, ini, fim):
    """Deteccoes dos 4 smells, separadas em dentro e fora do trecho.

    Dentro do trecho, a linha vira relativa ao inicio, para comparar
    original e unidade.
    """
    dentro, fora = [], []
    for d in detectar_arquivo(str(caminho)):
        if ini <= d["linha"] <= fim:
            dentro.append((d["smell"], d["linha"] - ini, d["metricas"]))
        else:
            fora.append(f"{d['smell']} L{d['linha']} {d['metricas']}")
    return sorted(dentro), fora


# ---------------------------------------------------------------- 3. pytest

def _pytest(pasta, *extra, timeout=None):
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *extra, str(pasta)]
    return subprocess.run(cmd, cwd=pasta, capture_output=True, text=True, timeout=timeout)


def _resultado_testes(pasta):
    """{nome_do_teste: passou} lido do relatorio junit do pytest."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        junit = Path(tmp) / "junit.xml"
        _pytest(pasta, f"--junitxml={junit}")
        if not junit.exists():
            return {}
        casos = ET.parse(junit).getroot().iter("testcase")
        return {c.get("name"): not any(f.tag in ("failure", "error", "skipped") for f in c)
                for c in casos}


# ---------------------------------------------------------------- 4. mutacao

_TROCA_CMP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE, ast.GtE: ast.Lt,
              ast.Gt: ast.LtE, ast.LtE: ast.Gt, ast.In: ast.NotIn, ast.NotIn: ast.In,
              ast.Is: ast.IsNot, ast.IsNot: ast.Is}
_TROCA_BIN = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult,
              ast.FloorDiv: ast.Mult, ast.Mod: ast.FloorDiv}
_TROCA_BOOL = {ast.And: ast.Or, ast.Or: ast.And}


class _Mutador(ast.NodeTransformer):
    """Percorre a arvore em ordem fixa e numera os pontos de mutacao.

    Com alvo=None so conta e descreve os pontos. Com alvo=k aplica apenas a
    k-esima mutacao. Os filhos sao sempre visitados antes do no, para a
    numeracao ser a mesma nas duas passadas.

    Regras: inverte comparacao (== por !=, < por >=, in por not in...),
    troca operador aritmetico (+ por -, * por /...), troca and por or,
    remove not, inverte True/False, soma 1 a numero, troca instrucao
    (atribuicao, chamada solta, return, raise) por pass.
    """

    def __init__(self, ini, fim, deslocamento, alvo=None):
        self.ini, self.fim, self.deslocamento, self.alvo = ini, fim, deslocamento, alvo
        self.pontos = []

    def _ponto(self, no, descricao):
        """Registra o ponto se estiver no trecho; True se e o ponto a mutar."""
        linha = getattr(no, "lineno", 0)
        if not self.ini <= linha <= self.fim:
            return False
        self.pontos.append(f"L{linha + self.deslocamento}:{no.col_offset} {descricao}")
        return len(self.pontos) - 1 == self.alvo

    def visit_Compare(self, no):
        self.generic_visit(no)
        for i, op in enumerate(no.ops):
            troca = _TROCA_CMP.get(type(op))
            if troca and self._ponto(no, f"{type(op).__name__}->{troca.__name__}"):
                no.ops[i] = troca()
        return no

    def _operador(self, no):
        troca = _TROCA_BIN.get(type(no.op))
        if troca and self._ponto(no, f"{type(no.op).__name__}->{troca.__name__}"):
            no.op = troca()

    def visit_BinOp(self, no):
        self.generic_visit(no)
        self._operador(no)
        return no

    def visit_BoolOp(self, no):
        self.generic_visit(no)
        troca = _TROCA_BOOL[type(no.op)]
        if self._ponto(no, f"{type(no.op).__name__}->{troca.__name__}"):
            no.op = troca()
        return no

    def visit_UnaryOp(self, no):
        self.generic_visit(no)
        if isinstance(no.op, ast.Not) and self._ponto(no, "remove not"):
            return no.operand
        return no

    def visit_Constant(self, no):
        if isinstance(no.value, bool):
            if self._ponto(no, f"{no.value}->{not no.value}"):
                return ast.copy_location(ast.Constant(not no.value), no)
        elif isinstance(no.value, (int, float)):
            if self._ponto(no, f"{no.value}->{no.value + 1}"):
                return ast.copy_location(ast.Constant(no.value + 1), no)
        return no

    def _apagar(self, no):
        if self._ponto(no, f"apaga {type(no).__name__}"):
            return ast.copy_location(ast.Pass(), no)
        return no

    def visit_AugAssign(self, no):
        self.generic_visit(no)
        self._operador(no)
        return self._apagar(no)

    def visit_Expr(self, no):
        self.generic_visit(no)
        if isinstance(no.value, ast.Constant) and isinstance(no.value.value, str):
            return no  # docstring
        return self._apagar(no)

    def _visitar_e_apagar(self, no):
        self.generic_visit(no)
        return self._apagar(no)

    visit_Assign = visit_AnnAssign = visit_Return = visit_Raise = _visitar_e_apagar


def _mutantes(fonte, ini, fim, deslocamento):
    """Lista (descricao, codigo) com um mutante por ponto do trecho."""
    contador = _Mutador(ini, fim, deslocamento)
    contador.visit(_parse(fonte))
    saida = []
    for k, descricao in enumerate(contador.pontos):
        arvore = _Mutador(ini, fim, deslocamento, alvo=k).visit(_parse(fonte))
        saida.append((descricao, ast.unparse(ast.fix_missing_locations(arvore))))
    return saida


def _rodar_mutante(codigo, nome_unidade, teste):
    """'morto', 'sobreviveu' ou 'timeout' (conta como morto)."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        Path(tmp, nome_unidade).write_text(codigo, encoding="utf-8")
        shutil.copy(teste, tmp)
        try:
            r = _pytest(Path(tmp), "-x", timeout=TIMEOUT_MUTANTE)
        except subprocess.TimeoutExpired:
            return "timeout"
    return "sobreviveu" if r.returncode == 0 else "morto"


def _mutacao(unidade, teste, ini, fim, deslocamento):
    """(ok, 'mortos/total', vivos, observacao)."""
    fonte = unidade.read_text(encoding="utf-8")
    # Base: a unidade reescrita pelo ast.unparse, sem mutacao, tem que passar.
    # Senao a reescrita (que perde comentarios) invalidaria a mutacao.
    base = _rodar_mutante(ast.unparse(_parse(fonte)), unidade.name, teste)
    if base != "sobreviveu":
        return False, "", [], "a unidade reescrita sem mutacao ja falha nos testes"
    mutantes = _mutantes(fonte, ini, fim, deslocamento)
    if not mutantes:
        return False, "0/0", [], "nenhum ponto de mutacao no trecho"
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        resultados = list(pool.map(lambda m: _rodar_mutante(m[1], unidade.name, teste), mutantes))
    vivos = [d for (d, _), r in zip(mutantes, resultados) if r == "sobreviveu"]
    mortos = len(mutantes) - len(vivos)
    return mortos >= 1, f"{mortos}/{len(mutantes)}", vivos, ""


# ---------------------------------------------------------------- 5 e 6

def _neutralidade(linhas, uini, ufim):
    achados = []
    for n, linha in enumerate(linhas, start=1):
        if uini <= n <= ufim:
            continue
        for m in PISTAS.finditer(linha):
            achados.append(f"L{n} '{m.group(0)}'")
    return achados


def _contrato(inst, unidade, origem_json):
    problemas = []
    arvore = _parse(unidade.read_text(encoding="utf-8"))
    doc = " ".join((ast.get_docstring(arvore) or "").split())  # ignora quebra de linha
    problemas += [f"docstring sem '{frase}'" for frase in CONTRATO if frase not in doc]
    if not any(isinstance(n, ast.FunctionDef) and n.name == "executar" for n in arvore.body):
        problemas.append("sem executar() no nivel do modulo")
    if not origem_json.exists():
        return problemas + ["sem origem.json"]
    origem = json.loads(origem_json.read_text(encoding="utf-8"))
    problemas += [f"origem.json sem '{c}'" for c in CAMPOS_ORIGEM if c not in origem]
    for campo in ("id", "smell", "arquivo"):
        if campo in origem and origem[campo] != inst[campo]:
            problemas.append(f"origem.json {campo}={origem[campo]!r}, selecao diz {inst[campo]!r}")
    return problemas


# ---------------------------------------------------------------- instancia

def checar(inst, com_mutacao=True):
    """Roda o checklist de uma instancia e devolve a linha da tabela."""
    linha = {c: "" for c in COLUNAS}
    linha.update(id=inst["id"], smell=inst["smell"],
                 data=datetime.date.today().isoformat(), ambiente=_ambiente())
    obs = []
    pasta, unidade, teste, origem_json = _caminhos(inst)
    if not unidade.exists():
        linha.update(aprovada="nao", observacoes=f"sem unidade em {unidade.relative_to(RAIZ)}")
        return linha, []

    origem = json.loads(origem_json.read_text(encoding="utf-8")) if origem_json.exists() else {}
    linhas_u = _ler_linhas(unidade)

    # 1. diff
    try:
        ini, fim, bloco = _trecho_original(inst, origem)
        achados = _localizar(bloco, linhas_u)
        if len(achados) == 1:
            uini, ufim = achados[0], achados[0] + len(bloco) - 1
            linha["diff"] = "ok"
        else:
            uini = None
            linha["diff"] = "falha"
            obs.append(f"trecho (linhas {ini}-{fim}) achado {len(achados)} vezes na unidade")
    except (ValueError, SyntaxError) as erro:
        uini = None
        linha["diff"] = "erro"
        obs.append(f"diff: {erro}")

    # 2. pysmell (precisa do trecho localizado)
    if uini is None:
        linha["pysmell"] = "n/a"
    else:
        orig_dentro, _ = _deteccoes(DATASET / inst["arquivo"], ini, fim)
        unid_dentro, unid_fora = _deteccoes(unidade, uini, ufim)
        esperadas = {int(n) - ini for n in inst["linhas"].split(";")}
        do_smell = {rel for s, rel, _ in orig_dentro if s == inst["smell"]}
        ok = orig_dentro == unid_dentro and not unid_fora and esperadas <= do_smell
        linha["pysmell"] = "ok" if ok else "falha"
        if orig_dentro != unid_dentro:
            obs.append(f"pysmell no trecho difere: original {orig_dentro}, unidade {unid_dentro}")
        if unid_fora:
            obs.append("pysmell fora do trecho: " + ", ".join(unid_fora))
        if not esperadas <= do_smell:
            obs.append(f"linhas da selecao sem deteccao {inst['smell']} no original")

    # 3. pytest
    if not teste.exists():
        linha["pytest"] = "falha"
        obs.append("sem arquivo de testes")
    else:
        testes = _resultado_testes(pasta)
        nomes = sorted(testes)
        prefixos_ok = (len(nomes) == 3 and
                       all(any(n.startswith(p) for n in nomes) for p in PREFIXOS_TESTE))
        passaram = sum(testes.values())
        linha["pytest"] = "ok" if prefixos_ok and passaram == 3 else "falha"
        if linha["pytest"] != "ok":
            obs.append(f"pytest: {passaram} de {len(nomes)} passaram; testes {nomes}")

    # 4. mutacao
    vivos = []
    if not com_mutacao:
        linha["mutacao"] = "pulada"
    elif uini is None or linha["pytest"] != "ok":
        linha["mutacao"] = "n/a"
    else:
        ok, placar, vivos, nota = _mutacao(unidade, teste, uini, ufim, ini - uini)
        linha.update(mutacao="ok" if ok else "falha", mutantes=placar,
                     mutantes_vivos=" | ".join(vivos))
        if nota:
            obs.append(f"mutacao: {nota}")

    # 5. neutralidade
    if uini is None:
        linha["neutralidade"] = "n/a"
    else:
        pistas = _neutralidade(linhas_u, uini, ufim)
        linha["neutralidade"] = "ok" if not pistas else "falha"
        if pistas:
            obs.append("pistas fora do trecho: " + ", ".join(pistas))

    # 6. contrato
    problemas = _contrato(inst, unidade, origem_json)
    linha["contrato"] = "ok" if not problemas else "falha"
    obs += problemas

    itens = ("diff", "pysmell", "pytest", "neutralidade", "contrato")
    aprovada = all(linha[i] == "ok" for i in itens) and linha["mutacao"] in ("ok", "pulada")
    linha["aprovada"] = "sim" if aprovada else "nao"
    linha["observacoes"] = " | ".join(obs)
    return linha, vivos


# ---------------------------------------------------------------- tabela

def _gravar(linhas_novas, ordem):
    existentes = {}
    if TABELA.exists():
        with open(TABELA, encoding="utf-8", newline="") as fh:
            existentes = {l["id"]: l for l in csv.DictReader(fh)}
    existentes.update({l["id"]: l for l in linhas_novas})
    with open(TABELA, "w", encoding="utf-8", newline="") as fh:
        escritor = csv.DictWriter(fh, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(existentes[i] for i in ordem if i in existentes)


def _resumo(linha):
    itens = [f"{c} {linha[c]}" for c in ("diff", "pysmell", "pytest", "neutralidade", "contrato")]
    mut = linha["mutacao"] + (f" ({linha['mutantes']})" if linha["mutantes"] else "")
    return f"{linha['id']:8} {' | '.join(itens)} | mutacao {mut}  => {linha['aprovada'].upper()}"


def main(argv=None):
    p = argparse.ArgumentParser(description="Checklist automatico da adaptacao das instancias.")
    p.add_argument("ids", nargs="*", help="ids das instancias (padrao: todas as que tem pasta)")
    p.add_argument("--sem-mutacao", action="store_true", help="pula a mutacao")
    args = p.parse_args(argv)

    selecao = _selecao()
    desconhecidos = [i for i in args.ids if i not in selecao]
    if desconhecidos:
        p.error(f"ids fora da selecao: {', '.join(desconhecidos)}")

    ids = args.ids or [i for i, inst in selecao.items() if _caminhos(inst)[0].exists()]
    linhas = []
    for i in ids:
        linha, vivos = checar(selecao[i], com_mutacao=not args.sem_mutacao)
        linhas.append(linha)
        print(_resumo(linha))
        if linha["observacoes"]:
            for nota in linha["observacoes"].split(" | "):
                print(f"         ! {nota}")
        for v in vivos:
            print(f"         mutante vivo: {v}")
    _gravar(linhas, list(selecao))

    todas = _pytest(INSTANCIAS)
    resumo = (todas.stdout.strip().splitlines() or ["(sem saida)"])[-1]
    print(f"\npytest instancias (todas juntas): {resumo}")
    print(f"tabela: {TABELA.relative_to(RAIZ)}")
    reprovadas = [l["id"] for l in linhas if l["aprovada"] != "sim"]
    if reprovadas:
        print(f"reprovadas: {', '.join(reprovadas)}")
    return 1 if reprovadas or todas.returncode != 0 else 0


if __name__ == "__main__":
    sys.exit(main())
