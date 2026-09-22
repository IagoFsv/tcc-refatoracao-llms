# Refatoracao de code smells em Python por LLMs

Codigo do estudo empirico do TCC que avalia a qualidade das refatoracoes de
*code smells* em Python geradas por tres modelos de linguagem, de forma
comparativa. Os smells avaliados sao Long Method, Long Parameter List, Long
Lambda Function e Multiply-Nested Container.

## Modelos avaliados

Modelos acessados por API, em tier de acesso gratuito, para favorecer a
reprodutibilidade:

- Gemini `gemini-3.1-flash-lite` (tier gratuito do Google)
- Qwen `qwen/qwen3.6-27b` (tier gratuito via Groq)

Um terceiro modelo esta previsto. A temperatura é 0.5 para todos.

## Como o repositorio se mapeia na metodologia

| Etapa da metodologia            | Onde no repositorio                    |
|---------------------------------|----------------------------------------|
| Dataset de entrada              | `dados/dataset_zhang/` (baixar, ver abaixo) |
| Deteccao de smells              | `dados/pysmell/` (Pysmell portado)     |
| Selecao das instancias          | `dados/selecao/`                       |
| Unidades adaptadas + testes     | `instancias/` (por smell)              |
| Prompts (Role, Few-Shot, CoT)   | `prompts/`                             |
| Geracao (3 modelos x 3 exec.)   | `geracao/`, saidas em `resultados/geracoes/` |
| Validacao funcional (pytest)    | `resultados/validacao/`                |
| Metricas (Radon/Pylint/Pysmell) | `resultados/metricas/`                 |
| Analise comparativa             | `analise/`                             |

## Reproducao

O dataset de entrada nao acompanha o repositorio, por ser codigo de
terceiros. Baixe de <https://doi.org/10.5281/zenodo.13335000> e descompacte
em `dados/dataset_zhang/`, de forma que exista
`dados/dataset_zhang/dataset/files/`. Detalhes em `dados/pysmell/README.md`.

```bash
pip install -r requirements.txt
cp .env.example .env     # preencha com suas proprias chaves de API
python -m geracao.smoke_test --dry-run   # verifica a configuracao
python -m geracao.smoke_test             # testa as APIs configuradas
python -m dados.selecao.selecionar        # gera a lista de instancias da fase 1
```

As chaves de API nao acompanham o repositorio; cada pessoa usa as suas. Os
valores de metricas dependem das versoes das ferramentas, listadas em
`requirements.txt`; fixe-as com `pip freeze` para reproducao fiel.

Sobre determinismo: mesmo com parametros fixos, as APIs de LLM nao garantem
gerar saidas identicas em novas execucoes. Por isso todas as saidas brutas
ficam arquivadas em `resultados/geracoes/`, de forma imutavel; sao elas a
evidencia, e nao a promessa de regeracao.

## Proveniencia dos dados

As instancias de code smells derivam do conjunto de dados de Zhang et al.
(2024), adaptadas para unidades executaveis conforme descrito na monografia.

## Autoria do codigo

As unidades adaptadas e os exemplos de codigo foram elaborados pelo autor com
apoio de modelos de linguagem. As refatoracoes avaliadas em `resultados/` foram
geradas pelos tres modelos sob avaliacao, e ficam registradas com o modelo de
origem e os parametros usados.
