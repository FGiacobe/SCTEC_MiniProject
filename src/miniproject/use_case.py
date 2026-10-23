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
    max_date = data['data'].max().date().strftime('%d/%m/%Y')
    min_date = data['data'].min().date().strftime('%d/%m/%Y')
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
        'min_date': min_date,
        'max_date': max_date,
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


def get_occurrencies_by_month(data: pd.DataFrame, column: str, year: int) -> dict[int, int]:
    """Get the volume of products by month for a specific year.

    Args:
        data (pd.DataFrame): The input DataFrame.
        year (int): The year to filter by.
        column (str): The column to count occurrences for.

    Returns:
        dict[int, int]: The volume of products by month for the specified year.
    """
    volume_by_month = group_by_columns(data, group_columns=['data'], agg_column=column, agg_func='count').reset_index()
    volume_by_month = volume_by_month.assign(
        ano=pd.to_datetime(volume_by_month['data']).dt.year, mes=pd.to_datetime(volume_by_month['data']).dt.month
    )
    volume_by_month = volume_by_month.query('ano == @year')
    volume_by_month = volume_by_month.groupby(['mes']).agg({column: 'sum'}).to_dict()
    volume_by_month = volume_by_month[column]
    return volume_by_month


def get_ocurrences(data: pd.DataFrame) -> dict[str, pd.Series | dict[int, int]]:

    occurrences: dict[str, pd.Series | dict[int, int]] = {
        'top_n_products_by_female': top_n(data, column='produto', filter='F', n=3),
        'top_n_products_by_male': top_n(data, column='produto', filter='M', n=3),
        'products_by_month': get_occurrencies_by_month(data, column='produto', year=2020),
    }
    return occurrences


def run() -> pd.DataFrame:
    df = extract.extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)
    df = remove_duplicates(df)
    return df


if __name__ == '__main__':
    df = run()
    # product_by_gender = group_by_columns(df, group_columns=['genero', 'categoria'], agg_column='data', agg_func='count')
    # print(product_by_gender)

    # Como o volume de compras varia ao longo do tempo — por mês/ano.
    # sales_over_time = (
    #     group_by_columns(df, group_columns=['data'], agg_column='categoria', agg_func='count')
    #     .reset_index()
    #     .assign(ano=sales_over_time['data'].dt.year, mes=sales_over_time['data'].dt.month)
    #     .query('ano == 2020')
    # )
    # sales_over_time['ano'] = pd.to_datetime(sales_over_time['data']).dt.year
    # sales_over_time['mes'] = pd.to_datetime(sales_over_time['data']).dt.month
    # print(sales_over_time[sales_over_time['ano'] == 2020].groupby(['ano', 'mes']).agg({'produto': 'sum'}))

    volume_by_product = get_occurrencies_by_month(df, column='produto', year=2020)
    for mes, produto in volume_by_product.items():
        print({'mes': mes, 'produto': produto})
