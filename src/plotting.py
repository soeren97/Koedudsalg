import pandas as pd
import matplotlib.pyplot as plt

import os


def save_image(path: str) -> None:
    """Save plotted image.

    Args:
        path (str): path to folder where image will be saved.
    """
    plt.savefig(f"Reports/{path}.png")


def plot_by_day(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by day.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    dataframe["Total"].plot(style="-o", title="Daily sales")
    plt.ylabel("Sales Incl. vat [DKK]")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    save_image(f"{path}/daily")


def plot_by_week(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by week.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    dataframe["Total"].resample("W-Mon").sum().plot(style="-o", title="Weekly sales")
    plt.ylabel("Sales Incl. vat [DKK]")
    plt.xticks(rotation=30, ha="right")
    save_image(f"{path}/weekly")


def plot_by_month(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by week.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    dataframe["Total"].resample("M").sum().plot(style="-o", title="Monthly sales")
    plt.ylabel("Sales Incl. vat [DKK]")
    plt.xticks(rotation=30, ha="right")
    save_image(f"{path}/monthly")
