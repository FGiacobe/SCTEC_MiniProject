"""Views for displaying data processing and analysis results."""

from collections.abc import Callable
from time import sleep
from typing import cast

import pandas as pd
from packages.miniproject.src import config
from packages.miniproject.src.miniproject import use_case as uc
from packages.miniproject.src.miniproject import utils
from rich.console import Console
from rich.panel import Panel

console = Console(theme=config.THEME)


def status_view(data: pd.DataFrame) -> pd.DataFrame:
    """Clean the input data while displaying the status of each processing step.

    Args:
        data (pd.DataFrame): The extracted data to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_clean = data.copy()

    with console.status(
        '[title]  Carregando os dados...  [/title] ',
        spinner='aesthetic',
        spinner_style='cyan',
    ) as status:
        sleep(4)
        status.update(status='[title] Removendo registros duplicados... [/title]')
        sleep(2)
        df_clean = uc.remove_duplicates(df_clean)
        console.log('✅ [header]Registros duplicados removidos![/header]')

        status.update(status='[title] Removendo registros sem produto ou categoria... [/title]')
        sleep(2)
        df_clean = uc.remove_null_values(
            df_clean,
            subset=['produto', 'categoria'],
        )
        console.log('✅ [header]Valores nulos relevantes removidos![/header]\n\n')

    return df_clean


def resume_view(data: pd.DataFrame) -> None:
    """Display a summary view of the DataFrame.

    Displays information including column count, record count, duplicates,
    null values, and data types.

    Args:
    data (pd.DataFrame): The input DataFrame to summarize.
    """
    info = uc.get_data_info(data)
    columns = info.get('columns', 0)
    registers = utils.br_number(info.get('registers', 0), decimals=0)
    registers_no_duplicates = utils.br_number(info.get('drop_duplicates', 0), decimals=0)
    duplicates = utils.br_number(info.get('duplicates', 0) * -1, decimals=0)
    pct_duplicates = utils.br_number(info.get('pct_duplicates', 0) * -1, decimals=2, pct=True)
    nulls_total = utils.br_number(info.get('null_values_total', 0) * -1, decimals=0)
    pct_nulls = utils.br_number(info.get('pct_nulls', 0) * -1, decimals=2, pct=True)
    types_nulls = info.get('types_nulls', pd.DataFrame())
    min_date = info.get('min_date', None)
    max_date = info.get('max_date', None)

    text_summary = (
        f'[bold]Colunas: [positive]{columns}[/positive]\t'
        f'Registros: {registers_no_duplicates} / {registers}\t'
        f'Duplicados: {duplicates} / {pct_duplicates}\t'
        f'Nulos: {nulls_total} / {pct_nulls}[/bold]\n\n'
        f'A base de dados possui [positive]13[/positive] colunas sendo [negative]3[/negative] removidas por estarem vazias resultando em [positive]{columns}[/positive] colunas válidas, possui [positive]{registers_no_duplicates}[/positive] registros válidos, foram removidos {duplicates} registros duplicados e {nulls_total} valores nulos. Janela de dados [positive]{min_date}[/positive] -> [positive]{max_date}[/positive]. Optou-se por remover os valores nulos de produtos e categorias que eram relevantes para a análise, garantindo a integridade dos dados restantes.'
    )

    title = '[title]\tResumo dos Dados\t[/title]'

    console.print(
        Panel(
            text_summary,
            title=title,
            expand=True,
            safe_box=True,
            width=120,
            padding=(1, 3),
        ),
        justify='full',
    )
    # Print table rich console for nulls and data types
    cols = ['Atributo', 'Tipo de Dado', 'Nulos']
    utils.print_table(data=types_nulls, title='Valores Ausentes e Tipos de Dados', columns=cols)


def shopping_by_gender_view(data: pd.DataFrame) -> None:
    """Display a view of shopping data grouped by gender.

    Args:
        data (pd.DataFrame): The input DataFrame containing shopping data.
    """
    shopping_by_gender = uc.group_by_columns(
        data,
        group_columns=['genero'],
        agg_column='genero',
        agg_func='count',
    )
    female: int = cast(int, shopping_by_gender.loc['F', 'genero'])
    male: int = cast(int, shopping_by_gender.loc['M', 'genero'])
    total: int = female + male
    pct_female: float = female / total * 100
    pct_male: float = male / total * 100
    pct_diff: str = utils.br_number((female - male) / ((female + male) / 2) * 100, 2, True)

    title = '[title]\tResumo de Compras por Gênero\t[/title]'
    text_summary = f"""[bold]Comparas por gênero:[/bold]
    [bold]- Feminino\t:[/bold] [positive]{'░' * int(pct_female)} {pct_female:.2f}%[/positive]
    [bold]- Masculino\t:[/bold] [positive]{'░' * int(pct_male)} {pct_male:.2f}%[/positive]
    A análise de compras por gênero mostra a distribuição de compras entre clientes do sexo feminino com {utils.br_number(female, 0)} compras e o masculino com {utils.br_number(male, 0)} compras. Sendo o feminino predominante com uma diferença percentual simétrica de {pct_diff}. Com isso, podemos observar a tendência de maior participação feminina nas compras podendo influenciar estratégias de marketing e estoque. Por outro lado seria importante considerar ações para engajar o público masculino e equilibrar a participação nas compras."""

    console.print(
        Panel(
            text_summary,
            title=title,
            expand=True,
            width=120,
            padding=(1, 3),
        ),
        justify='full',
    )


def occurrences_by_gender_view(data: pd.DataFrame, column: str, year: int, n: int) -> None:
    """Display a view of products grouped by gender.

    Args:
        data (pd.DataFrame): The input DataFrame containing shopping data.
        column (str): The column to analyze.
        year (int): The year to filter by.
        n (int): The number of top occurrences to display.
    """
    occurrences = uc.get_ocurrences_by_gender(
        data,
        column=column,
        year=year,
        n=n,
    )
    for key, value in occurrences.items():
        title = key.replace('_', ' ').title()
        utils.print_table(
            data=value,
            title=title,
            columns=value.columns.tolist()
            if isinstance(value, pd.DataFrame)
            else pd.DataFrame([value]).columns.tolist(),
        )


def occurrences_by_period_view(data: pd.DataFrame, column: str, year: int) -> None:
    """Display a view of occurrences by period for a specific column and year.

    Args:
        data (pd.DataFrame): The input DataFrame containing shopping data.
        column (str): The column to analyze.
        year (int): The year to filter by.
    """
    occurrences = uc.get_occurrencies_by_period(data, column=column, year=year)
    title = f'{column.replace("_", " ").title()} por período no ano {year}'
    utils.print_table(data=occurrences, title=title, columns=occurrences.columns.tolist())


def statistical_by_column_view(data: pd.DataFrame, column: str) -> None:
    """Display a statistical summary for a specific column.

    Args:
        data (pd.DataFrame): The input DataFrame containing shopping data.
        column (str): The column to analyze.
    """
    statistical_summary = uc.get_statistical_summary(data, column=column)
    utils.print_table(
        data=statistical_summary,
        title=f'Estatísticas para {column}',
        columns=statistical_summary.columns.tolist(),
    )


def run(data: pd.DataFrame) -> None:
    """Run the main analysis workflow."""
    df_clean = status_view(data)

    def run_occurrences_by_gender() -> None:
        column = input(f'Informe a coluna para análise {data.columns.tolist()}: ')
        year = int(input('Informe o ano: '))
        n = int(input('Informe o número de ocorrências (n): '))
        occurrences_by_gender_view(df_clean, column=column, year=year, n=n)

    def run_occurrences_by_period() -> None:
        column = input(f'Informe a coluna para análise {data.columns.tolist()}: ')
        year = int(input('Informe o ano: '))
        occurrences_by_period_view(df_clean, column=column, year=year)

    def run_statistical_by_column() -> None:
        column = input(f'Informe a coluna para análise {data.columns.tolist()}: ')
        statistical_by_column_view(df_clean, column=column)

    options: dict[str, Callable[[], None]] = {
        '1': lambda: resume_view(data),
        '2': lambda: shopping_by_gender_view(df_clean),
        '3': run_occurrences_by_gender,
        '4': run_occurrences_by_period,
        '5': run_statistical_by_column,
        '6': lambda: uc.export_clean_data(df_clean),
    }

    while True:
        console.print(
            """[bold blue]Escolha uma opção para análise:[/bold blue]
            1. Resumo dos dados
            2. Dados de compras por gênero
            3. Ocorrências por gênero
            4. Ocorrências por ano
            5. Estatísticas por coluna
            6. Exportar dados limpos (csv)
            7. Sair
            """
        )
        option = input('Escolha uma opção: ')

        if option == '7':
            console.print('[bold green]Encerrando as análises.[/bold green]')
            break
        if option not in options:
            console.print('[bold red]Opção inválida. Tente novamente.[/bold red]')
            continue

        options[option]()
        console.print('[bold green]✅ Análise carregada com sucesso![/bold green]')
