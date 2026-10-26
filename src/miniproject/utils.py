"""Utility functions for the miniproject package."""

import numpy as np
import pandas as pd
from packages.miniproject.src import config
from rich.console import Console
from rich.table import Table

console = Console(theme=config.THEME)


def pos_neg_view(number: float | str, pct: bool = False) -> str:
    """Return a string with positive or negative styling based on the number.

    Args:
        number (int | float | str): The number to style.
        pct (bool): If true include the sufix '%' at number.

    Returns:
        str: The styled number as a string.
    """
    if not isinstance(number, str):
        number = str(number)
    if '-' not in number:
        return f'[positive]{number + "%" if pct else number}[/positive]'
    return f'[negative]{number + "%" if pct else number}[/negative]'


def br_number(number: float | int, decimals: int = 2, pct: bool = False) -> str:
    """Format a number according to Brazilian conventions.

    Args:
        number (float | str): The number to be formatted.
        decimals (int): The number of decimal places to format the number with. Default is 2.
        pct (bool): If true include the sufix '%' at number. Default is False.

    Returns:
        str: The formatted number as a string with thousands separator. Example: 1.234.567,89
    """
    # Deve coverter formatos como "1234567,59" para "1.234.567,59" ou "1234567.59" para "1.234.567,59"
    # if isinstance(number, str):
    #     number = number.replace(',', '.')
    #     number = float(number)
    formatted_number = f'{number:,.{decimals}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return pos_neg_view(formatted_number, pct=pct)


def graphic_bar(value: float, max_value: int = 100, char: str = '░') -> str:
    """Generate a simple text-based graphic bar for a given value.

    Args:
        value (float): The value to represent with the bar.
        max_value (int, optional): The maximum value for scaling the bar. Defaults to 100.
        char (str, optional): The character to use for the bar. Defaults to '░'.

    Returns:
        str: The graphic bar as a string.
    """
    n = int(max(0, min(value, 100)) / 100 * max_value)
    bars = char * n
    return bars


def format_tables(col: str, value: str | float | int) -> str:
    """Format a value for display in tables based on its column type.

    If define a column as 'Grafico', it will generate a graphic bar for the value.

    Args:
        col (str): The column name.
        value (str | float | int): The value to format.

    Returns:
        str: The formatted value as a string.
    """
    if col.lower().strip() == 'grafico':
        return graphic_bar(float(value))
    if isinstance(value, (float, np.floating)):
        return br_number(value, decimals=2)
    if isinstance(value, (int, np.integer)):
        return br_number(value, decimals=0)
    return str(value).strip().title()


def print_table(data: pd.DataFrame | pd.Series, title: str, columns: list[str]):
    """Print a formatted table with the given title and columns.

    Args:
        data (pd.DataFrame): The data to display in the table.
        title (str): The title of the table.
        columns (list[str]): The columns to include in the table.
    """
    table = Table(
        title=title,
        header_style='header',
        safe_box=True,
        min_width=120,
        title_style='title',
        show_lines=True,
    )
    for col in columns:
        table.add_column(col.strip().title())
    for _, row in data.iterrows():
        table.add_row(*[format_tables(col, row[col]) for col in columns])
    console.print(table)
