import os

import pandas as pd


def load_dataframe(path: str) -> pd.DataFrame:
    """Load dataframe from csv.

    Args:
        path (str): path to dataframe.

    Returns:
        pd.DataFrame: Read dataframe
    """
    return pd.read_csv(
        "Data/Månedsrapport webshop december 2023.csv", encoding="iso 8859-10", sep=";"
    )


def save_dataframe(dataframe: pd.DataFrame, path: str) -> None:
    """Save dataframe.

    Args:
        dataframe (pd.DataFrame): Dataframe to be saved.
        path (str): Path to folder where dataframe will be saved.
    """
    os.makedirs(f"Reports/{path}", exist_ok=True)
    dataframe.to_csv(f"Reports/{path}/spreadsheet.csv")
