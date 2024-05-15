import os
import json

import pandas as pd
from datetime import datetime, timedelta


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


def save_dataframe(dataframe: list[pd.DataFrame], path: str) -> None:
    """Save dataframe.

    Args:
        dataframe (list[pd.DataFrame]): Dataframe to be saved.
        path (str): Path to folder where dataframe will be saved.
    """
    os.makedirs(f"Reports/{path}", exist_ok=True)
    dataframe.to_excel(f"Reports/{path}/spreadsheet.xlsx")


def change_date_today():
    # Get the current date and time
    current_datetime = datetime.now()

    # Calculate the date for yesterday
    yesterday = current_datetime - timedelta(days=1)

    # Get the earliest timestamp for yesterday (midnight)
    start_date = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)

    # # Get the latest timestamp for yesterday (23:59:59)
    end_date = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)

    config = load_config("config")
    config["Start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
    config["End_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S")

    save_config("config", config)


def change_date_year():
    # Get the current date and time
    current_datetime = datetime.now()

    # Get last year
    last_year = current_datetime - timedelta(days=365)

    # Get the earliest timestamp for last year
    start_date = datetime(last_year.year, 1, 1, 0, 0, 0)

    # # Get the latest timestamp for this year
    end_date = datetime(current_datetime.year, 12, 31, 23, 59, 59)

    config = load_config("config")
    config["Start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
    config["End_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S")

    save_config("config", config)


if __name__ == "__main__":
    pass
