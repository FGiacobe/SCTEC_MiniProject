"""Use case functions for data processing and analysis."""

from collections.abc import Callable
from typing import Any

import pandas as pd
from packages.miniproject.src import config
from packages.miniproject.src.miniproject import extract
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


def get_ocurrences_by_gender(data: pd.DataFrame, column: str, year: int, n: int) -> dict[str, pd.Series | pd.DataFrame]:
    """Get the top occurrences by gender for a specific column and year.

    Args:
        data (pd.DataFrame): The input DataFrame.
        column (str): The column to analyze.
        year (int): The year to filter by.
        n (int): The number of top occurrences to return.

    Returns:
        dict[str, pd.Series | pd.DataFrame]: A dictionary containing the top occurrences by gender.

    Raises:
        ValueError: If the specified column is not found in the DataFrame.
    """
    if column not in data.columns:
        raise ValueError(f"A Coluna '{column}' não foi encontrada no DataFrame.")
    else:
        column = column.lower()

    if column == 'estado_civil':
        # Substituir os valores numéricos por rótulos de estado civil
        data[column] = data[column].map(
            {'1': 'Casado(a)', '2': 'Divorciado(a)', '3': 'Separado(a)', '4': 'Solteiro(a)', '5': 'Viúvo(a)'}
        )
    female_top = (
        data.query('genero == "F"')
        .groupby(by=[column])
        .size()
        .sort_values(ascending=False)
        .head(n)
        .reset_index(name='Total')
    )
    male_top = (
        data.query('genero == "M"')
        .groupby(by=[column])
        .size()
        .sort_values(ascending=False)
        .head(n)
        .reset_index(name='Total')
    )
    occurrences: dict[str, pd.Series | pd.DataFrame] = {
        f'top_n_{column}_por_genero_feminino': female_top,
        f'top_n_{column}_por_genero_masculino': male_top,
    }
    return occurrences


def get_statistical_summary(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Get descriptive statistics for a numeric DataFrame column.

    Args:
        data (pd.DataFrame): The input DataFrame.
        column (str): The column to analyze.

    Returns:
        pd.DataFrame: A one-row DataFrame with count, mean, median, standard
            deviation, mode, minimum, quartiles, and maximum.

    Raises:
        ValueError: If the specified column is not found in the DataFrame.
        ValueError: If the column is not numeric or contains no valid values.
    """
    if column not in data.columns:
        raise ValueError(f"A Coluna '{column}' não foi encontrada no DataFrame.")

    values = data[column]
    if not pd.api.types.is_numeric_dtype(values):
        return values.describe().to_frame().T

    values = values.dropna()
    if values.empty:
        raise ValueError(f"A Coluna '{column}' não possui valores numéricos válidos.")

    modes: list[object] = values.mode().tolist()
    statistics: dict[str, object] = {
        'Contagem': values.count(),
        'Média': values.mean(),
        'Mediana': values.median(),
        'Desvio padrão': values.std(),
        'Moda': modes,
        'Mínimo': values.min(),
        'Q1 (25%)': values.quantile(0.25),
        'Q2 (50%)': values.quantile(0.50),
        'Q3 (75%)': values.quantile(0.75),
        'Máximo': values.max(),
    }
    return pd.DataFrame([statistics])


def export_clean_data(df: pd.DataFrame) -> None:
    """Export the cleaned DataFrame to a CSV file."""
    file_name = 'cleaned_data.csv'
    file_path = config.PROCESSED_DATA_DIR / file_name

    df.to_csv(file_path, index=False)
    console.print(
        f'[bold green]Dados limpos exportados com sucesso para "{file_path.relative_to(config.BASE_DIR)}".[/bold green]'
    )


def run() -> pd.DataFrame:
    """Run the main data extraction and cleaning workflow.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df = extract.extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)
    df = remove_duplicates(df)
    df = remove_null_values(df, subset=['produto', 'categoria'])
    return df
