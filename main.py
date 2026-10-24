import pandas as pd
from packages.miniproject.src import config
from packages.miniproject.src.miniproject import extract, views
from packages.miniproject.src.miniproject import use_case as uc


def run() -> None:
    df = extract.extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)

    views.run(df)


if __name__ == '__main__':
    run()
