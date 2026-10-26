import pandas as pd
from packages.miniproject.src import config

CAMINHO_CSV = f'{config.RAW_DATA_DIR}/base_varejo.csv'


class LimpezaDados:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.registros_iniciais = len(df)

    def remover_colunas_vazias(self):
        # Remove as colunas "Unnamed" (100% vazias) geradas pelos ";"
        # extras no fim das linhas do CSV
        self.df = self.df.dropna(axis=1, how='all')
        return self

    def remover_nulos(self):
        # Remove as linhas que tenham algum valor nulo (NaN)
        self.df = self.df.dropna()
        return self

    def remover_duplicados(self):
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        return self

    def executar(self):
        self.remover_colunas_vazias().remover_nulos().remover_duplicados()
        return self.df

    def salvar_csv(self, caminho: str):
        self.df.to_csv(caminho, sep=';', index=False)

    def mostrar_relatorio(self):
        print(f'Registros iniciais: {self.registros_iniciais}')
        print(f'Registros removidos: {self.registros_iniciais - len(self.df)}')
        print(f'Registros finais: {len(self.df)}')


if __name__ == '__main__':
    # Rodando este arquivo, a limpeza é aplicada e gravada dentro do próprio Base_varejo.csv

    limpeza = LimpezaDados(pd.read_csv(CAMINHO_CSV, sep=';'))
    limpeza.executar()
    limpeza.mostrar_relatorio()
    limpeza.salvar_csv(CAMINHO_CSV)
    print(f'Base limpa salva em: {CAMINHO_CSV}')
