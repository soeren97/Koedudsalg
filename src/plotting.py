from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


def save_image(path: str) -> None:
    """Save plotted image.

    Args:
        path (str): path to folder where image will be saved.
    """
    plt.ylabel("Sales Incl. vat [DKK]")
    plt.tight_layout()
    plt.ylim(bottom=0)
    plt.savefig(f"Reports/{path}.png")
    plt.close()


def plot_by_day(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by day.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    plt.figure(figsize=(10, 6))

    dataframe["Total"].plot(
        style="-o",
        title="Daily sales",
    )
    plt.xticks(
        ticks=dataframe.index,
        labels=dataframe.index.strftime("%Y/%m/%d"),
        rotation=30,
        ha="right",
    )
    save_image(f"{path}/daily")


def plot_by_week(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by week.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    weekly_data = dataframe.copy()
    weekly_data.index = weekly_data.index.strftime("%W")
    weekly_data = weekly_data.groupby("Date").sum()

    plt.figure(figsize=(10, 6))
    plt.plot(weekly_data["Total"], marker="o")
    plt.xlim(min(weekly_data.index), max(weekly_data.index))
    plt.xlabel("Week number")

    save_image(f"{path}/weekly")


def plot_by_month(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by week.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    monthly_data = dataframe.copy()
    monthly_data.index = monthly_data.index.strftime("%m")
    monthly_data = monthly_data.groupby("Date").sum()

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_data["Total"], marker="o")
    plt.xlim(min(monthly_data.index), max(monthly_data.index))
    plt.xlabel("Month")

    save_image(f"{path}/monthly")


if __name__ == "__main__":
    pass
