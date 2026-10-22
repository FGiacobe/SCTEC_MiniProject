from time import sleep
from typing import cast

import pandas as pd
from packages.miniproject.src import config
from packages.miniproject.src.miniproject import extract, utils
from packages.miniproject.src.miniproject import use_case as uc
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

theme = Theme(
    {
        'title': 'bold white on slate_blue3',
        'header': 'bold slate_blue3',
        'column': 'bold steel_blue',
        'positive': 'deep_sky_blue1',
        'negative': 'red3',
    }
)
console = Console(theme=theme)


def status_view(process: list[str]):
    """Display the status of the data processing steps.

    Args:
        process (list[str]): A list of processing steps to display.
    """
    with console.status(
        '[title]  Carregando os dados...  [/title] ',
        spinner='aesthetic',
        spinner_style='cyan',
    ) as status:
        sleep(3)
        console.log('✅ [header]Dados carregados com sucesso![/header]')

        status.update(
            status=' [title]  Analisando os dados...  [/title] ',
            spinner='pong',
            spinner_style='cyan',
        )
        for step in process:
            sleep(1)
            console.log(f'✅ [header]Criando {step}...[/header]')

        print()

        status.update(
            status=' [title]  Preparando a exibição dos dados...  [/title] ',
            spinner='material',
            spinner_style='cyan',
        )
        sleep(5)


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
    nulls = info.get('null_values', {})
    nulls_total = utils.br_number(info.get('null_values_total', 0) * -1, decimals=0)
    pct_nulls = utils.br_number(info.get('pct_nulls', 0) * -1, decimals=2, pct=True)
    data_types = info.get('data_types', {})

    text_summary = (
        f'[bold]Colunas: [positive]{columns}[/positive]\t'
        f'Registros: {registers_no_duplicates} / {registers}\t'
        f'Duplicados: {duplicates} / {pct_duplicates}\t'
        f'Nulos: {nulls_total} / {pct_nulls}[/bold]\n\n'
        f'A base de dados possui [positive]13[/positive] colunas sendo [negative]3[/negative] removidas por estarem vazias resultando em [positive]{columns}[/positive] colunas válidas, possui [positive]{registers_no_duplicates}[/positive] registros válidos sendo removidos {duplicates} registros duplicados, possui {nulls_total} valores nulos.'
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
        )
    )
    # Print table rich console for nulls and data types
    table = Table(
        title='Valores Ausentes e Tipos de Dados',
        header_style='header',
        safe_box=True,
        min_width=120,
        title_style='title',
        show_lines=True,
    )
    table.add_column('Variavel', style='column')
    table.add_column('Tipo de Dado', justify='left')
    table.add_column('Valores Ausentes', justify='left')
    for col, value in dict(nulls).items():
        table.add_row(
            f'[bold]{str(col).upper()}[/bold]',
            f'[positive]{data_types[col]}[/positive]',
            f'{utils.br_number(value * -1, decimals=0)}',
        )
    console.print(table)


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
    pct_diff: str = utils.br_number((female - male) / ((female + male) / 2) * 100, 2, True)

    title = '[title]\tResumo de Compras por Gênero\t[/title]'
    text_summary = f'A análise de compras por gênero mostra a distribuição de compras entre clientes do sexo feminino com {utils.br_number(female, 0)} compras e o masculino com {utils.br_number(male, 0)} compras. Sendo o feminino predominante com uma diferença percentual de {pct_diff}. Com isso, podemos observar a tendência de maior participação feminina nas compras podendo influenciar estratégias de marketing e estoque. Por outro lado seria importante considerar ações para engajar o público masculino e equilibrar a participação nas compras.'

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


def run(data: pd.DataFrame) -> None:

    process = ['Resumo dos dados', 'Dados de compras por gênero']

    # status_view(process)
    resume_view(data)
    df_clean = uc.remove_duplicates(data)
    df_clean = uc.remove_null_values(df_clean, subset=['produto', 'categoria'])
    shopping_by_gender_view(df_clean)

    console.print('[bold green]✅ Análises carregadas com sucesso![/bold green]')


if __name__ == '__main__':
    df = extract.extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)
    run(df)
