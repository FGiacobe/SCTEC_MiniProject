# Checklist do Mini-Projeto — Análise de Dados de Varejo

Use esta lista para acompanhar a execução do mini-projeto. Marque cada item somente quando estiver concluído e verificado.

## Sprint 1 — Preparação e importação dos dados

- [X] Baixar a base de varejo indicada no enunciado e identificar o arquivo CSV que será usado.
- [X] Salvar a base no projeto e confirmar o caminho do arquivo usado pelo script.
- [X] Preparar a execução no VS Code ou no Google Colab.
- [X] Criar ou revisar o script Python e importar as bibliotecas necessárias, incluindo pandas.
- [X] Ler os dados do CSV. Se a entrega seguir o critério de manipulação estruturada do enunciado, usar `read_csv`.
- [X] Exibir e conferir a quantidade de registros, os nomes das colunas e os tipos de dados.

## Sprint 2 — Inspeção e transformação dos dados

- [X] Inspecionar os dados e reportar pelo menos dois problemas encontrados, como valores nulos, duplicatas, categorias vazias ou datas inválidas.
- [X] Identificar os campos de texto, inteiros, decimais e datas que precisam de transformação.
- [X] Limpar strings e normalizar os valores necessários; usar expressões regulares quando fizer sentido.
- [X] Converter os campos numéricos para os tipos apropriados e tratar valores inválidos.
- [X] Converter a data da compra de texto para o tipo `datetime` e verificar se houve datas inválidas.
- [X] Validar a regra do identificador do número da compra e separar os registros conforme a regra definida para a base.

## Sprint 3 — Limpeza de nulos e duplicatas

- [X] Tratar categorias vazias preenchendo-as com `"Sem Categoria"`, conforme o critério de avaliação.
- [X] Avaliar os nulos das dimensões físicas, escolher como tratá-los e justificar a decisão no código ou na documentação.
- [X] Avaliar os demais valores nulos e justificar se serão removidos ou imputados.
- [X] Identificar e remover duplicatas relevantes, preservando registros válidos.
- [X] Conferir os dados após a limpeza e registrar possíveis problemas remanescentes.
- [X] Salvar ou disponibilizar a base limpa (`df_limpo`) como parte dos arquivos do projeto.

## Sprint 4 — Estatística descritiva e agrupamentos

- [ ] Calcular, para a coluna de número de filhos dos clientes, contagem, média, mediana, desvio padrão, moda, mínimo, máximo e quartis.
- [ ] Explorar pelo menos dois agrupamentos com `groupby()` ou `pivot_table()`, usando combinações relevantes para responder perguntas sobre compras ou vendas.
- [ ] Conferir se os resultados dos agrupamentos e das estatísticas são coerentes com os dados limpos.

## Sprint 5 — Relatório e documentação

- [ ] Exibir no terminal os contadores e resultados principais da análise.
- [ ] Escrever de 3 a 6 tópicos com os principais insights e eventuais problemas remanescentes na base.
- [ ] Documentar no `README.md` o objetivo do projeto, como executar o script e os insights obtidos.
- [ ] Incluir no `README.md` uma reflexão teórica sobre ETL e qualidade de dados.
- [ ] Criar o arquivo `README_NomeDoAluno_Turma.md` com instruções simples para executar a solução.
- [ ] Revisar se o código está comentado o suficiente para explicar cada bloco de lógica.

## Sprint 6 — Versionamento e entrega

- [ ] Organizar no repositório os arquivos da solução: script Python, documentação e base limpa (`df_limpo`).
- [ ] Criar um repositório público no GitHub da conta pessoal, seguindo o padrão `Miniprojeto_NomeAluno_Turma` (turma: `Analise_de_Dados_T1`).
- [ ] Enviar os arquivos ao GitHub em commits que demonstrem o progresso, em vez de concentrar todo o trabalho em um único commit final.
- [ ] Conferir que o repositório está público e que o README explica como executar o projeto.
- [ ] Testar a execução a partir dos arquivos organizados para confirmar que as instruções funcionam.
- [ ] Copiar o link do repositório e submetê-lo à tarefa **Módulo 1 - Mini-Projeto Avaliativo**, na semana 07 do AVA.
- [ ] Submeter o link até **26/10/2026 às 22h**.
