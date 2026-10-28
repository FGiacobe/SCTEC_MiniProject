"""Main script for running the data extraction and analysis workflow."""

from packages.miniproject.src import config
from packages.miniproject.src.miniproject import extract, views


def run() -> None:
    """Run the main data extraction and analysis workflow."""
    df = extract.extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)

    views.run(df)


if __name__ == '__main__':
    run()
