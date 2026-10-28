# Mini-Projeto — Análise de Dados de Varejo

Análise exploratória da base de compras de varejo, desenvolvida em Python com
pandas. O projeto importa os dados, faz uma limpeza básica e oferece análises
interativas pelo terminal.

## Objetivos

- Inspecionar a estrutura, os tipos e a qualidade dos dados.
- Remover registros duplicados e registros sem produto ou categoria.
- Explorar padrões por gênero, categoria, produto e período.
- Resumir a distribuição do número de filhos dos clientes.
- Exportar uma cópia dos dados limpos para novas análises.

## Base de dados

Foi utilizada a base [Base Varejo](https://www.kaggle.com/datasets/namespaiva/base-varejo/data).
Coloque o arquivo `base_varejo.csv` em `data/raw/`. A leitura espera um CSV
separado por ponto e vírgula e considera as colunas selecionadas em
`src/config.py`.

As colunas usadas são:

| Coluna no projeto | Descrição |
| --- | --- |
| `data` | Data da compra |
| `compra_id` | Identificador da compra |
| `cliente_id` | Identificador do cliente |
| `genero` | Gênero do cliente |
| `estado_civil` | Estado civil do cliente |
| `n_filhos` | Número de filhos do cliente |
| `classe_social` | Segmentação socioeconômica |
| `produto_id` | Identificador do produto |
| `categoria` | Categoria do produto |
| `produto` | Nome do produto |

## Requisitos e execução

- Python 3.14 ou superior.
- Recomendo o uso do gerenciador de pacotes e ambientes virtuais (uv)[https://docs.astral.sh/uv/#installation]
- Dependências: pandas e Rich, listadas em `requirements.txt`.
- O arquivo de entrada `data/raw/base_varejo.csv`.

No terminal, a partir da raiz do repositório, instale as dependências e execute
o aplicativo:
Usando `pip`:
```bash
python -m pip install -r packages/miniproject/requirements.txt
python -m packages.miniproject.main
```

Usando `uv`:
```bash
uv run --all-packages miniproject
```

O programa prepara os dados e apresenta um menu interativo. Use as opções para
ver o resumo, analisar compras por gênero, explorar ocorrências por gênero ou
período, consultar as estatísticas descritivas de uma coluna ou exportar os
dados limpos. Para encerrar, escolha a opção de saída indicada no menu.

O CSV limpo é salvo em `data/processed/cleaned_data.csv` ao selecionar a opção
de exportação. A limpeza atualmente remove duplicatas e registros com produto e 
categoria ausentes. Optei por remover esses registros em vez de preenchê-los com 
valores padrão para evitar informações que não identifiquem as variáveis corretamente.

## Resultados e insights

Os números abaixo foram calculados a partir do arquivo
`data/processed/cleaned_data.csv` disponível neste projeto:

1. A base processada contém **730.219 registros**, 10 colunas, sem valores
   vazios e sem linhas integralmente duplicadas. O período registrado vai de
   **04/01/2019 a 08/12/2022**.
2. Na contagem de registros por gênero, **F** corresponde a 380.735 (52,14%)
   e **M** a 349.484 (47,86%). Essa comparação é de registros de compra, não
   necessariamente de clientes únicos.
3. **ALIMENTOS** é a categoria mais frequente, com 384.197 registros (52,61%).
   Em seguida aparecem HIGIENE, com 137.702 (18,86%), e LIMPEZA, com 128.632
   (17,62%).
4. Para `n_filhos`, os 730.219 registros têm média de **1,15**, mediana **0**,
   desvio padrão amostral **1,42**, moda **0**, mínimo **0**, máximo **4** e
   quartis **Q1 = 0**, **Q2 = 0** e **Q3 = 2**.
5. Na base bruta, foram identificados 3.650 valores ausentes em cada uma das
   colunas de categoria e nome do produto. Como o tratamento atual remove
   registros sem categoria ou produto, é importante considerar essa exclusão
   ao interpretar os resultados.

Os agrupamentos por gênero e categoria descrevem a participação nos registros
disponíveis; a base usada pelo projeto não contém valores monetários, portanto
essas contagens não devem ser interpretadas como faturamento.

## ETL e qualidade de dados

ETL significa **Extração, Transformação e Carga**. Neste projeto, a extração
consiste em ler o CSV e selecionar as colunas necessárias; a transformação
inclui a conversão da data e a remoção de duplicatas e de registros sem
produto ou categoria; a carga corresponde à exportação da base resultante
para CSV. Separar essas etapas torna o processo reproduzível e facilita
verificar de onde vêm os dados e como foram preparados.

Qualidade de dados não é apenas ausência de valores nulos. Também envolve
completude, consistência, validade, unicidade e adequação à análise. A decisão
de remover registros incompletos pode evitar análises de produto sem
identificação, mas reduz a quantidade de dados disponível e pode introduzir
viés se as ausências não forem aleatórias. Por isso, os dados brutos devem ser
preservados e as regras de tratamento documentadas.

