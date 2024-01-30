import pandas as pd
import numpy as np
import tkinter as tk

from src.clean_csv import sum_up_csv
from src.filehandling import load_dataframe, save_dataframe, load_config
from src.plotting import plot_by_day, plot_by_week, plot_by_month
from src.soap import DanDomainSOAPHandler
from src.gui import DateRangeWindow

USE_SOAP = True


def main():
    if USE_SOAP:
        dd_config = load_config("config")
        loader = DanDomainSOAPHandler(dd_config)
        sums = loader.make_soap_request(
            start_date=dd_config["Start_date"],
            end_date=dd_config["End_date"],
        )

    else:
        data = load_dataframe("Data/Månedsrapport webshop december 2023.csv")

        sums = sum_up_csv(data)

    report = pd.concat(sums, axis=1).fillna(0)

    report.columns = ["Credit card payment", "Card terminal", "Cash payment"]

    report["Total"] = report.sum(axis=1)

    path = f"{report.index[0].strftime('%Y-%m-%d')}_to_{report.index[-1].strftime('%Y-%m-%d')}"

    save_dataframe(report, path)

    plot_by_day(report, path)

    plot_by_week(report, path)

    plot_by_month(report, path)


if __name__ == "__main__":
    root = tk.Tk()
    date_range_window = DateRangeWindow(root)
    root.mainloop()
    main()
