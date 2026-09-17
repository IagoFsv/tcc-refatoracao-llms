# Pysmell portado para Python 3

Detector de code smells Python de Chen et al., usado por Zhang et al. (2024)
para montar o dataset deste estudo e usado aqui em dois momentos do pipeline:
para detectar as instancias adicionais nos repositorios do PyExamine e para
checar, na etapa de metricas, se o smell saiu do codigo refatorado.

## Origem

- Repositorio: <https://github.com/chenzhifei731/Pysmell>
- Commit: `233afebac24c910be89d065ffa661ec72458a62c` (06/07/2018)
- Arquivos de origem: `pysmell/detection/astChecker.py` (metricas) e
  `pysmell/detection/detector.py` (limiares)

## Por que portar

O original e Python 2 e nao roda no ambiente do estudo. Mesmo com Python 2
instalado ele nao serviria: o dataset do Zhang et al. e Python 3, e o parser
do Python 2 nao le f-string. O original tambem nao tem linha de comando, e um
script que le CSVs de metricas ja gerados.

As mudancas do porte estao listadas no cabecalho de `astChecker.py` e em
`compat.py`. Sao poucas e nenhuma toca a logica de metricas nem os limiares.

Duas armadilhas, ja resolvidas, que reaparecem se alguem "modernizar" o codigo:

1. **Nao troque `astunparse` por `ast.unparse`.** O `astunparse` poe
   parenteses em toda lambda aninhada e o `ast.unparse` nao. Isso encurta a
   metrica NOC e faz perder instancias de Long Lambda Function (com
   `ast.unparse`, 4 das 11 LLF do Zhang deixam de ser detectadas).
2. **Nao renomeie `visit_TryExcept` para `visit_Try`.** No Python 3 o no se
   chama `ast.Try`, entao esse visitante nunca dispara, e e isso que se quer:
   o metodo original nao chama `generic_visit` no fluxo normal, entao
   renomear faz o detector pular o corpo de todo bloco `try` e perder
   instancias (ex.: `Natsar-main/modules/tele.py`).

## Estrategia de limiares

O Pysmell tem tres conjuntos de limiares. Este estudo usa **Tuning Machine**,
a mesma do Zhang et al. (secao 3.1 do artigo), que e a de maior precisao
segundo Chen et al. (2018). Os tres conjuntos estao em `detectar.py` e podem
ser escolhidos com `--estrategia`, mas o padrao e `tuning` e a metodologia
deste estudo so vale com ele.

## Validacao

O dataset do Zhang et al. NAO e versionado neste repositorio (e codigo de
terceiros; ver `.gitignore`). Baixe do Zenodo e descompacte em
`dados/dataset_zhang/`, de modo que exista
`dados/dataset_zhang/dataset/files/`:

- <https://doi.org/10.5281/zenodo.13335000>

`validar_porte.py` roda o porte sobre os 311 arquivos do dataset do Zhang e
compara com `results of RQ1.xlsx` e com os numeros do artigo:

```bash
python -m dados.pysmell.validar_porte
```

Resultado atual (Python 3.14.6, astunparse 1.6.3):

| | Artigo | Porte |
|---|---|---|
| Arquivos .py | 311 | 311 |
| Trechos do Zhang reproduzidos (4 smells) | 83 | **83** |
| Deteccoes em Repositories (10 smells) | 57 | **57** |
| Deteccoes em Code (10 smells) | 630 | 394 |

Os 83 trechos e o total de Repositories batem exato. A diferenca em Code
continua sem explicacao e nao afeta a amostra: as 45 instancias do Zhang sob
o rotulo Code foram todas reproduzidas. Uma parte pode vir dos 3 arquivos que
nao parseiam no Python 3 (`Code/main-3.py`, `Repositories/machine.py`,
`Repositories/sokoban.py`), nenhum deles com instancia no dataset. Outra
hipotese, nao verificada, e a pasta ter 138 arquivos em Code e 173 em
Repositories, enquanto o artigo diz 140 e 171 (o total de 311 bate).

Rode de novo se mexer em `astChecker.py`, `compat.py` ou `detectar.py`. O
script sai com codigo 1 se algum trecho do Zhang deixar de ser reproduzido.

## Uso

```bash
# smells do estudo (LM, LPL, LLF, MNC), estrategia tuning
python -m dados.pysmell.detectar caminho/do/codigo.py
python -m dados.pysmell.detectar pasta/ --saida resultado.csv

# os 10 smells do Chen et al.
python -m dados.pysmell.detectar pasta/ --todos

# inclui medidas abaixo do limiar (comparar original com refatorado)
python -m dados.pysmell.detectar arquivo.py --metricas
```

Como biblioteca:

```python
from dados.pysmell.detectar import detectar_arquivo, medir_arquivo
```

## Arquivos

- `astChecker.py` - porte do extrator de metricas (visitantes de AST).
- `compat.py` - shim do astunparse e lista de tipos de AST do Python 2.
- `detectar.py` - limiares do `detector.py` original + linha de comando.
- `validar_porte.py` - confere o porte contra o dataset do Zhang.
- `_xlsx.py` - leitor minimo de .xlsx, so para ler as planilhas do Zhang.
