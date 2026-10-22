# Mini Projeto - Varejo

## Análise Exploratória de Dados (AED) com Python

Este documento apresenta a análise exploratória de dados (AED) realizada no contexto do mini projeto de varejo, utilizando Python para explorar, visualizar e interpretar os dados disponíveis.

## Objetivos da AED

Os principais objetivos da análise exploratória de dados neste mini projeto de varejo incluem:

- Compreender a estrutura e a qualidade dos dados disponíveis.
- Identificar padrões, tendências e anomalias nos dados (valores nulos, tipos incorretos, duplicatas).
- Tratar dados inconsistentes, ausentes ou duplicados.
- Gerar insights que possam orientar decisões estratégicas no contexto do varejo (quem compra mais, quais categorias vendem mais, como variam as vendas ao longo do tempo).
- Preparar os dados para análises mais avançadas, como alimentar um dashboard ou gerar modelagem preditiva.

O objetivo educacional desta análise exploratória de dados é proporcionar aos participantes do mini projeto uma compreensão prática de como explorar, limpar e interpretar dados no contexto do varejo, desenvolvendo habilidades analíticas e de tomada de decisão baseadas em dados.

## Base de Dados

> Base de dados no Kaggle: [base-varejo.csv](https://www.kaggle.com/datasets/namespaiva/base-varejo/data)

### Descrição da Base de Dados

A base de dados possue 830.000 registros de compras em uma rede de supermercados no período de 2010 à 2022.

### Estrutura da Base de Dados


#### Resumo da Estrutura da Base de Dados

| DATA | CO_ID | CL_ID | CL_GENERO | CL_EC | CL_FHL | CL_SEG | PR_ID | PR_CAT | PR_NOME |
|------|-------|-------|-----------|-------|--------|--------|-------|--------|---------|
| 2010-01-01 | 1000 | 534 | M | Solteiro | Sem Filhos | A | 67 | Bebidas | Coca-Cola |
| 2010-01-01 | 1000 | 534 | F | Casado | 2 Filhos | B | 178 | Alimentos | Arroz |

Visão compacta da estrutura da base de dados `base_varejo.csv`.


O conjunto de dados inclui as seguintes categorias:

- **DATA:** Data em que a transação de compra foi realizada.
- **CO_ID:** Identificação única da compra (nota fiscal).
- **CL_ID:** Identificação única do cliente.
- **CL_GENERO:** Gênero (sexo biológico do cliente).
- **CL_EC:** Estado civil do cliente.
  - 1: Casado
  - 2: Divorciado
  - 3: Separado
  - 4: Solteiro
  - 5: Viúvo
- **CL_FHL:** Número de filhos do cliente.
- **CL_SEG:** Segmentação econômica do cliente (classe A, B ou C).
- **PR_ID:** Identificação única do produto (SKU).
- **PR_CAT:** Categoria do produto.
- **PR_NOME:** Nome do produto.

