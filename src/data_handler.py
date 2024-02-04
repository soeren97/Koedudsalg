import pandas as pd

from src.soap import DanDomainSOAPHandler


def get_and_clean_data(
    config: dict,
    sort_by_order: bool = True,
) -> list[pd.DataFrame]:
    """downlaod and clean data.

    Args:
        config (dict): Config file containing login information and such.
        sort_by_order (bool, optional): Define sorting method. Defaults to True.

    Returns:
        list[pd.DataFrame]: Cleaned data.
    """
    sums = load_data(config)

    report = clean_data(sums, sort_by_order)
    return report


def clean_data(
    dataframe: list[pd.DataFrame],
    sort_by_order: bool,
) -> list[pd.DataFrame]:
    """Clean data.

    Args:
        sums (pd.DataFrame): Data summed up per day.

    Returns:
        pd.DataFrame: Cleaned data.
        sort_by_order (bool): Define sorting method.
    """
    sums = sum_up_data(dataframe, sort_by_order)

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
    dataframe = loader.make_soap_request(
        start_date=config["Start_date"],
        end_date=config["End_date"],
    )

    return dataframe


def sum_up_data(
    dataframe: list[pd.DataFrame],
    sort_by_order: bool,
) -> list[pd.DataFrame]:
    """Sum up the order data either by order or date.

    Args:
        dataframe (list[pd.DataFrame]): Order data
        sort_by_order (bool): Define sorting method.

    Returns:
        list[pd.DataFrame]: Summed up data.
    """
    if sort_by_order:
        pass
    else:
        for df in dataframe:
            df["Date"] = pd.to_datetime(
                df["Date"], format="%Y-%m-%d %H:%M:%S"
            ).dt.strftime("%Y-%m-%d")
    sums = [values.groupby("Date")["Incl. vat"].sum() for values in dataframe]

    return sums
