# Refatoracao de code smells em Python por LLMs

Codigo do estudo empirico do TCC que avalia a qualidade das refatoracoes de
*code smells* em Python geradas por tres modelos de linguagem locais, de forma
comparativa. Os smells avaliados sao Long Method (LM), Long Parameter List
(LPL), Long Lambda Function (LLF) e Multiply-Nested Container (MNC).

## Modelos avaliados

Tres modelos open-weight, um por fabricante, rodando localmente via
[Ollama](https://ollama.com) 0.33.2, todos Instruct e na mesma quantizacao
(Q4_K_M):

| Modelo | Tag no Ollama |
|---|---|
| Qwen2.5-Coder-7B-Instruct | `qwen2.5-coder:7b-instruct-q4_K_M` |
| DeepSeek-Coder-6.7B-Instruct | `deepseek-coder:6.7b-instruct-q4_K_M` |
| Llama 3 8B Instruct | `llama3:8b-instruct-q4_K_M` |

Parametros iguais para todos (`config.yaml`): temperatura 0,5, `num_ctx`
8192, `num_predict` 4096, `top_k` 0, `top_p` 1.0, `min_p` 0,
`repeat_penalty` 1.0 e seeds 42, 43 e 44 para as tres execucoes. O digest de
cada modelo esta fixado no `config.yaml`; o cliente aborta se o modelo
instalado for outro.

## Desenho

- **Instancias (fase 1):** os trechos do dataset de Zhang et al. (2024),
  agrupados pela funcao que contem o smell. Sao 65 instancias, 59 depois das
  exclusoes da adaptacao (LM 9, LPL 19, LLF 11, MNC 20). Motivos das
  exclusoes em `instancias/excluidas.csv`.
- **Prompts:** tres tecnicas (Role Prompting, Few-Shot, Chain-of-Thought),
  com o mesmo nucleo de tarefa e so a camada da tecnica variando.
- **Geracao:** 59 instancias x 3 modelos x 3 tecnicas x 3 execucoes =
  1.593 chamadas, cada uma em contexto novo.
- **Validacao:** cada refatoracao passa pelos testes pytest da instancia
  (preservou o comportamento?) e pelo Pysmell (removeu o smell?).
- **Metricas:** so nas refatoracoes que passaram: Radon (CC, MI), Pylint e
  Pysmell, no original e no refatorado.

## Como o repositorio se mapeia na metodologia

| Etapa da metodologia            | Onde no repositorio                    |
|---------------------------------|----------------------------------------|
| Dataset de entrada              | `dados/dataset_zhang/` (baixar, ver abaixo) |
| Deteccao de smells              | `dados/pysmell/` (Pysmell portado para Python 3) |
| Selecao das instancias          | `dados/selecao/`                       |
| Unidades adaptadas + testes     | `instancias/<SMELL>/<ID>/`             |
| Checklist das instancias        | `adaptacao/checklist.py`, `instancias/checklist.csv` |
| Janela de contexto              | `adaptacao/medir_janela.py`, `instancias/janela.csv` |
| Prompts (Role, Few-Shot, CoT)   | `prompts/`, montados por `geracao/prompts.py` |
| Geracao                         | `geracao/`, saidas em `resultados/geracoes/` |
| Extracao do codigo              | `geracao/extrair.py`, saida em `resultados/geracoes/<fase>/_extraidos/` |
| Validacao funcional e do smell  | `validacao/conferir.py`, `resultados/validacao/` |
| Metricas (Radon/Pylint/Pysmell) | `resultados/metricas/`                 |
| Analise comparativa             | `analise/`                             |

Cada instancia tem `<ID>.py` (a unidade, que e o que vai no prompt),
`test_<ID>.py` (tres testes: tipico, borda e invalido) e `origem.json`
(proveniencia e adaptacoes, nunca enviado ao modelo).

## Situacao

Fase 1: geracao concluida (1.593 registros). Proximos passos: extracao do
codigo, validacao (etapa 5), metricas e analise. A fase 2 (repositorios do
PyExamine, com deteccao pelo Pysmell portado) vem depois.

## Reproducao

Requisitos: Python 3.14 e o Ollama 0.33.2 com os tres modelos acima
baixados (`ollama pull <tag>`).

O dataset de entrada nao acompanha o repositorio, por ser codigo de
terceiros. Baixe de <https://doi.org/10.5281/zenodo.13335000> e descompacte
em `dados/dataset_zhang/`, de forma que exista
`dados/dataset_zhang/dataset/files/`. Detalhes em `dados/pysmell/README.md`.

```bash
pip install -r requirements.txt

python -m dados.pysmell.validar_porte      # confere o porte do Pysmell (83/83 trechos)
python -m dados.selecao.selecionar         # gera a lista de instancias da fase 1
python -m adaptacao.checklist              # checklist de todas as instancias
pytest instancias                          # testes de todas as instancias

python -m geracao.smoke_test --dry-run     # confere config, Ollama no ar e digests
python -m geracao.smoke_test               # uma chamada curta a cada modelo
python -m geracao.gerar --dry-run          # confere o ambiente e conta o que falta
python -m geracao.gerar                    # fase 1 inteira, retoma de onde parou
python -m geracao.extrair                  # extrai o codigo das respostas brutas

python -m validacao.conferir LLF-01 <arquivo>  # preservou? removeu o smell?
```

Os valores de metricas dependem das versoes das ferramentas, listadas em
`requirements.txt`; fixe-as com `pip freeze` para reproducao fiel.

Sobre determinismo: mesmo com seed e parametros fixos, a saida pode mudar
com outra versao do Ollama, outro driver ou outra GPU, e o DeepSeek roda
parte na CPU (cerca de 16%), que arredonda diferente da GPU. Por isso todas
as respostas brutas ficam arquivadas em `resultados/geracoes/`, de forma
imutavel, com o prompt completo, os parametros, o modelo servido (tag e
digest), a versao do Ollama e o uso de GPU. Sao elas a evidencia, e nao a
promessa de regeracao.

## Proveniencia dos dados

As instancias de code smells derivam do conjunto de dados de Zhang et al.
(2024), adaptadas para unidades executaveis conforme descrito na monografia.
Os exemplos do prompt Few-Shot sao de autoria propria.

## Autoria do codigo

As unidades adaptadas e os testes foram elaborados pelo autor com apoio de
modelos de linguagem. As refatoracoes avaliadas em `resultados/` foram
geradas exclusivamente pelos tres modelos sob avaliacao, e ficam registradas
com o modelo de origem e os parametros usados.
