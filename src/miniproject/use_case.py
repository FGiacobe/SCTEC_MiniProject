from collections.abc import Callable
from typing import Any

import pandas as pd
from packages.miniproject.src import config
from packages.miniproject.src.miniproject import extract


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
    duplicates = data.duplicated().sum()
    null_values = data.isnull().sum()
    null_values_total = null_values.max()
    non_duplicates = total_registers - (duplicates + null_values_total)
    pct_duplicates = duplicates / total_registers * 100
    pct_nulls = null_values_total / total_registers * 100
    data_types = dict(data.dtypes)

    return {
        'registers': total_registers,
        'duplicates': duplicates,
        'drop_duplicates': non_duplicates,
        'columns': columns,
        'pct_duplicates': pct_duplicates,
        'null_values': null_values,
        'null_values_total': null_values_total,
        'pct_nulls': pct_nulls,
        'data_types': data_types,
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
        df (pd.DataFrame): The input DataFrame.
        group_columns (list[str]): The columns to group by.
        agg_column (str): The column to aggregate.
        agg_func (Callable[..., Any] | str): The aggregation function to apply.

    Returns:
        pd.DataFrame: The grouped and aggregated DataFrame.
    """
    if not agg_column:
        df = data.groupby(group_columns).agg(agg_func)
    df = data.groupby(group_columns).agg({agg_column: agg_func})

    return df


def run() -> pd.DataFrame:
    df = extract.extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)
    df = remove_duplicates(df)
    return df


if __name__ == '__main__':
    df = run()
    product_by_gender = group_by_columns(
        df, group_columns=['genero', 'categoria'], agg_column='genero', agg_func='count'
    )
    print(product_by_gender)

    # 730219
    # remove_null_values(df, subset=["produto", "categoria"])
    # df.drop(df[df["produto"] == "#N/D"].index, inplace=True)
