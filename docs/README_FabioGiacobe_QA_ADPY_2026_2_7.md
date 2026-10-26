# Instruções para execução — Mini-Projeto de Varejo

**Aluno:** Fabio Giacobe  
**Turma:** QA ADPY 2026/2 7

## Pré-requisitos

- Python 3.14 ou superior.
- O arquivo `base_varejo.csv`, disponível na [base Varejo do Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data), salvo em `packages/miniproject/data/raw/`.

## Executar pelo VS Code ou terminal

Abra a pasta raiz do repositório no VS Code. No terminal integrado, execute:

```bash
python -m pip install -r requirements.txt
python -u main.py
```

O programa carrega e prepara os dados e, em seguida, exibe um menu interativo.
Digite o número da análise desejada e siga as instruções exibidas no terminal.
Para finalizar, escolha **Sair**.

Para salvar a base limpa em CSV, selecione a opção **Exportar dados limpos**.
O arquivo será gravado em `packages/miniproject/data/processed/cleaned_data.csv`.