import pandas as pd


def squish_row(dataframe: pd.DataFrame, mask: pd.Series, n_squish: int) -> pd.DataFrame:
    """Shift rows that are skewed due to long item names.

    Args:
        dataframe (pd.DataFrame): Raw data from dandomain.
        mask (pd.Series): Mask to show what rows should be shifted.
        n_squish (int): Number of columns the masked rows should be shifted.

    Returns:
        pd.DataFrame: Shifted dataframe.
    """
    dataframe.loc[mask, dataframe.columns[n_squish]] = dataframe[mask][
        dataframe.columns[: 1 + n_squish]
    ].sum(axis=1)
    dataframe.loc[mask] = dataframe.loc[mask].shift(periods=-n_squish, axis="columns")

    return dataframe


def find_n_squishes(dataframe: pd.DataFrame) -> int:
    """Function to figure out number of times the raw dataframe should be shifted.

    Args:
        dataframe (pd.DataFrame): Raw data from dandomain.

    Returns:
        int: Max number of times the dataframes need to be shifted.
    """
    return len(dataframe.columns) - 10


def clean_file(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Shift rows that have been shifted due to long names.

    Args:
        dataframe (pd.DataFrame): Raw data from dandomain.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    n_squishes = find_n_squishes(dataframe)
    mask = dataframe["Employe"] == "DKK"
    dataframe = squish_row(dataframe, mask, 1)
    for i in range(n_squishes):
        mask = dataframe[dataframe.columns[9 + i]] == "DKK"
        dataframe = squish_row(dataframe, mask, i + 1)

    dataframe.drop(dataframe.columns[10:], axis=1, inplace=True)

    return dataframe


def seperate_data(dataframe: pd.DataFrame, categories: list[str]) -> list[pd.DataFrame]:
    """Seperate the dataframe into different payment methods.

    Args:
        dataframe (pd.DataFrame): Cleaned dataframe.
        categories (list[str]): List of payment methods

    Returns:
        list[pd.DataFrame]: Seperated dataframes.
    """
    seperated_df = {}
    for category in categories:
        index = dataframe[dataframe[dataframe.columns[0]] == category].index[0]
        seperated_df[category] = dataframe.loc[: index - 3]
        seperated_df[category].loc[:, "Incl. vat"] = pd.to_numeric(
            seperated_df[category]["Incl. vat"]
        )
        dataframe = dataframe.loc[index + 1 :]

    seperated_df["final"] = dataframe.iloc[:-1]
    seperated_df["final"].loc[:, "Incl. vat"] = pd.to_numeric(
        seperated_df["final"]["Incl. vat"]
    )

    return list(seperated_df.values())


def sum_up_csv(data):
    order_overview = data.head(10)
    order_overview = order_overview.drop(data.columns[6:], axis=1).drop(
        range(5), axis=0
    )

    overview_categories = order_overview[order_overview.columns[0]][2:-1].tolist()

    columns = [
        "Item",
        "Date",
        "Time",
        "Item number",
        "Amount",
        "Ex. vat",
        "Vat",
        "Incl. vat",
        "Currency",
        "Employe",
    ]

    column_mapping = dict(zip(data.columns[:10], columns))

    data.rename(columns=column_mapping, inplace=True)

    data = data.tail(-13)

    clean_data = clean_file(data)

    overviews = seperate_data(clean_data, overview_categories)

    for i in overviews:
        i.loc[:, "Date"] = pd.to_datetime(i["Date"], format="%d-%m-%Y")

    sums = [values.groupby("Date")["Incl. vat"].sum() for values in overviews]
    return sums


if __name__ == "__main__":
    pass
