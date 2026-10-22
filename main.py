import pandas as pd
from packages.miniproject.src import config
from packages.miniproject.src.miniproject import use_case as uc
from packages.miniproject.src.miniproject import views
from packages.miniproject.src.miniproject.extract import extract_raw_data


def run() -> None:
    df = extract_raw_data(file_name='base_varejo.csv', columns=config.SELECTED_COLUMNS)

    views.run(df)


if __name__ == '__main__':
    run()
