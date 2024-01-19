import pandas as pd
import numpy as np

from src.clean_csv import clean_file, seperate_data
from src.filehandling import save_dataframe, load_data
from src.plotting import plot_by_day, plot_by_week, plot_by_month


def main():
    data = load_data()

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
        i.loc[:, "Date"] = pd.to_datetime(i["Date"], format="%d-%m-%Y").dt.date

    sums = [values.groupby("Date")["Incl. vat"].sum() for values in overviews]

    report = pd.concat(sums, axis=1).fillna(0)

    report.columns = ["Credit card payment", "Card terminal", "Cash payment"]

    report["Total"] = report.sum(axis=1)

    path = f"{report.index[0]}-{report.index[-1]}"

    save_dataframe(report, path)

    plot_by_day(report, path)

    plot_by_week(report, path)

    plot_by_month(report, path)


if __name__ == "__main__":
    main()
