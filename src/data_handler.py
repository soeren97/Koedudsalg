import pandas as pd

from src.soap import DanDomainSOAPHandler


def get_and_clean_data(config: dict) -> pd.DataFrame:
    """downlaod and clean data.

    Args:
        config (dict): Config file containing login information and such.

    Returns:
        pd.DataFrame: Cleaned data.
    """
    sums = load_data(config)

    report = clean_data(sums)
    return report


def clean_data(sums: pd.DataFrame) -> pd.DataFrame:
    """Clean data.

    Args:
        sums (pd.DataFrame): Data summed up per day.

    Returns:
        pd.DataFrame: Cleaned data.
    """
    report = pd.concat(sums, axis=1).fillna(0)

    report.columns = ["Credit card payment", "Card terminal", "Cash payment"]

    report["Total"] = report.sum(axis=1)
    return report


def load_data(config: dict) -> pd.DataFrame:
    """Downlaod data using SOAP call.

    Args:
        config (dict): Config file containing login information and such.

    Returns:
        pd.DataFrame: Data summed up per day.
    """
    loader = DanDomainSOAPHandler(config)
    sums = loader.make_soap_request(
        start_date=config["Start_date"],
        end_date=config["End_date"],
    )

    return sums
