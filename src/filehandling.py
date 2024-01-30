import os
import json

import pandas as pd


def load_config(config_name: str) -> dict:
    """Load config.

    Args:
        config_name (str): Name of config file.

    Returns:
        dict: Config as dict.
    """
    with open(f"Config/{config_name}.json") as file:
        config = json.load(file)
    return config


def save_config(config_name: str, config: dict) -> None:
    """Save config.

    Args:
        config_name (str): Name of config file.
        config (dict): Config to be saved
    """
    with open(f"Config/{config_name}.json", "w") as file:
        json.dump(config, file, indent=4)


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


if __name__ == "__main__":
    pass
