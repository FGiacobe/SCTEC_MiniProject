"""Module for extracting raw data from CSV files."""

from pathlib import Path

import pandas as pd
from packages.miniproject.src import config


def extract_raw_data(file_name: str, columns: dict[str, tuple[str, ...]]) -> pd.DataFrame:
    """Extract raw data from a CSV file and return it as a pandas DataFrame.

    Args:
        file_name (str): The name of the CSV file to extract.
        columns (dict[str, tuple[str, ...]]): A dictionary mapping column keys to their names and types.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the extracted raw data.
    """
    file_path: Path = config.RAW_DATA_DIR / file_name
    cols = list(columns.keys())
    cols_names: dict[str, str] = {col: name for col, (name, _) in columns.items()}
    cols_types: dict[str, str] = {col: typ for col, (_, typ) in columns.items() if typ != 'datetime64[ns]'}

    df = pd.read_csv(
        file_path,
        sep=';',
        usecols=cols,
        dtype=cols_types,
        date_format='%d/%m/%Y',
        parse_dates=['DATA'],
        na_values='#N/D',
    )
    df.rename(columns=cols_names, inplace=True)

    return df


if __name__ == '__main__':
    df_test = extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)
    print(df_test.head())
    print(df_test.isnull().sum())
