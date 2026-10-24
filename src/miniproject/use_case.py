"""Use case functions for data processing and analysis."""

from collections.abc import Callable
from typing import Any

import pandas as pd
from packages.miniproject.src import config
from packages.miniproject.src.miniproject import extract, utils
from rich.console import Console

console = Console()


def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with duplicate rows removed.
    """
    data.drop_duplicates(inplace=True)
    return data


def remove_null_values(data: pd.DataFrame, subset: list[str]) -> pd.DataFrame:
    """Remove rows with null values from the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.
        subset (list[str]): List of columns with null values

    Returns:
        pd.DataFrame: The DataFrame with rows containing null values removed.
    """
    data.dropna(subset=subset, inplace=True)
    return data


def get_data_info(data: pd.DataFrame) -> dict[str, Any]:
    """Get information about the DataFrame including duplicates, nulls, and data types.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        dict[str, Any]: A dictionary containing information about the DataFrame.
    """
    total_registers = data.shape[0]
    columns = data.shape[1]
    max_date = data['data'].max().date().strftime('%d/%m/%Y')
    min_date = data['data'].min().date().strftime('%d/%m/%Y')
    duplicates = data.duplicated().sum()
    null_values = data.isnull().sum()
    null_values_total = null_values.max()
    non_duplicates = total_registers - (duplicates + null_values_total)
    pct_duplicates = duplicates / total_registers * 100
    pct_nulls = null_values_total / total_registers * 100
    types_nulls = pd.DataFrame(
        {
            'Atributo': list(null_values.index),
            'Tipo de Dado': [data.dtypes[col] for col in null_values.index],
            'Nulos': list(null_values),
        }
    )

    return {
        'registers': total_registers,
        'duplicates': duplicates,
        'drop_duplicates': non_duplicates,
        'columns': columns,
        'pct_duplicates': pct_duplicates,
        'null_values': null_values,
        'null_values_total': null_values_total,
        'pct_nulls': pct_nulls,
        'min_date': min_date,
        'max_date': max_date,
        'types_nulls': types_nulls,
    }


def get_statistical_summary(data: pd.DataFrame, column: str) -> dict[str, int | float]:
    """Get statistical summary for a specific column in the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.
        column (str): The column to summarize.

    Returns:
        dict[str, int | float]: A dictionary containing statistical summary.
    """
    statistics: dict[str, int | float] = {
        'count': int(data[column].count()),
        'mean': round(float(data[column].mean()), 2),
        'median': round(float(data[column].median()), 2),
        'std': round(float(data[column].std()), 2),
        'min': int(data[column].min()),
        'max': int(data[column].max()),
    }
    return statistics


def group_by_columns(
    data: pd.DataFrame,
    group_columns: list[str],
    agg_column: str,
    agg_func: Callable[..., Any] | str,
) -> pd.DataFrame:
    """Groups the DataFrame by the specified columns and applies an aggregation function.

    Args:
        data (pd.DataFrame): The input DataFrame.
        group_columns (list[str]): The columns to group by.
        agg_column (str): The column to aggregate.
        agg_func (Callable[..., Any] | str): The aggregation function to apply.

    Returns:
        pd.DataFrame: The grouped and aggregated DataFrame.
    """
    if not agg_column:
        df = data.groupby(group_columns).agg(agg_func)
    else:
        df = data.groupby(group_columns).agg({agg_column: agg_func})

    return df


def top_n(data: pd.DataFrame, column: str, filter: str | None = None, n: int = 3) -> pd.Series:
    """Get the top N values for a specific column in the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.
        column (str): The column to get top N values from.
        filter (str | None, optional): The filter to apply on the column. Defaults to None.
        n (int, optional): The number of top values to return. Defaults to 3.

    Returns:
        pd.Series: The top N values for the specified column.
    """
    if filter:
        return data.get(column, pd.Series()).get(filter, pd.Series()).sort_values(ascending=False).head(n)
    return data.get(column, pd.Series()).sort_values(ascending=False).head(n)


def get_occurrencies_by_period(data: pd.DataFrame, column: str, year: int | None = None) -> pd.DataFrame:
    """Get the volume of products by month for a specific year.

    Args:
        data (pd.DataFrame): The input DataFrame.
        year (int | None, optional): The year to filter by. Defaults to None.
        column (str): The column to count occurrences for.

    Returns:
        pd.DataFrame: The volume of products by month for the specified year.
    """
    occurrencies_by_period = group_by_columns(data, group_columns=['data'], agg_column=column, agg_func='count')
    occurrencies_by_period = occurrencies_by_period.assign(
        Ano=pd.to_datetime(occurrencies_by_period.index).year,
        Ordem=pd.to_datetime(occurrencies_by_period.index).month,
        Mes=pd.to_datetime(occurrencies_by_period.index).month_name(locale='pt_BR').str[:3],
    )
    if year is None:
        occurrencies_by_period = occurrencies_by_period.groupby(['Ano']).agg({column: 'sum'}).reset_index()
    else:
        occurrencies_by_period = occurrencies_by_period.query('Ano == @year')
        occurrencies_by_period = occurrencies_by_period.groupby(['Ordem', 'Mes']).agg({column: 'sum'}).reset_index()

    occurrencies_total: float = occurrencies_by_period[column].sum()
    occurrencies_by_period['Grafico'] = occurrencies_by_period[column] / occurrencies_total * 100
    occurrencies_by_period['Dif_Pct'] = occurrencies_by_period[column].pct_change() * 100
    occurrencies_by_period.fillna({'Dif_Pct': 0}, inplace=True)

    return occurrencies_by_period


def get_ocurrences(data: pd.DataFrame, column: str, year: int) -> dict[str, pd.Series | pd.DataFrame]:

    occurrences: dict[str, pd.Series | pd.DataFrame] = {
        'top_three_attributes_by_female': top_n(data, column=column, filter='F', n=3),
        'top_three_attributes_by_male': top_n(data, column=column, filter='M', n=3),
        'attributes_by_period': get_occurrencies_by_period(data, column=column, year=year),
    }
    return occurrences


def run() -> pd.DataFrame:
    df = extract.extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)
    df = remove_duplicates(df)
    return df


if __name__ == '__main__':
    df = run()

    occurrences_by_product = get_occurrencies_by_period(df, column='produto', year=2020)
    occurrences_by_product.dtypes
    occurrences_by_category = get_occurrencies_by_period(df, column='categoria', year=2022)

    info = get_data_info(df)
    info.get('null_values')
    nulls_df = info.get('types_nulls', pd.DataFrame())

    utils.print_table(
        data=nulls_df, title='Valores Ausentes e Tipos de Dados', columns=['Atributo', 'Tipo de Dado', 'Nulos']
    )
