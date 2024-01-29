from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def save_image(path: str, dataframe: pd.DataFrame) -> None:
    """Save plotted image.

    Args:
        path (str): path to folder where image will be saved.
        dataframe (pd.DateFrame): Data to be plotted.
    """
    plt.ylabel("Sales Incl. vat [DKK]")
    plt.tight_layout()
    plt.xlim(dataframe.index.min(), dataframe.index.max())
    plt.ylim(bottom=0)
    plt.legend()
    plt.savefig(f"Reports/{path}.png")
    plt.close()


def plot_weekend(dataframe: pd.DataFrame) -> None:
    """Show the weekend in a plot.

    Args:
        dataframe (pd.DataFrame): Data to be plotted.
    """
    saturdays = [date for date in dataframe.index if date.weekday() in [5, 6]]

    for saturday in saturdays:
        plt.axvspan(
            saturday,
            saturday + np.timedelta64(1, "D"),
            color="gray",
            alpha=0.3,
        )


def plot_by_payment(dataframe: pd.DataFrame) -> None:
    """Plot the different payment methods, in a plot addetively.

    Args:
        dataframe (pd.DataFrame): Dataframe to be plotted.
    """
    cash = dataframe["Cash payment"].copy()
    terminal = dataframe["Card terminal"] + cash
    card = dataframe["Credit card payment"] + terminal

    card_color = "blue"
    terminal_color = "green"
    cash_color = "orange"

    plt.plot(card, label="Credit card", color=card_color)
    plt.plot(terminal, label="Card terminal", color=terminal_color)
    plt.plot(cash, label="Cash payment", color=cash_color)

    plt.fill_between(
        card.index,
        0,
        cash,
        alpha=0.4,
        color=cash_color,
        label=None,
    )
    plt.fill_between(
        card.index,
        cash,
        terminal,
        alpha=0.4,
        color=terminal_color,
        label=None,
    )
    plt.fill_between(
        card.index,
        terminal,
        card,
        alpha=0.4,
        color=card_color,
        label=None,
    )


def plot_by_day(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by day.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """

    plt.figure(figsize=(10, 6))

    plot_weekend(dataframe)

    plot_by_payment(dataframe)

    plt.xticks(
        ticks=dataframe.index,
        labels=dataframe.index.strftime("%Y/%m/%d"),
        rotation=30,
        ha="right",
    )
    save_image(f"{path}/daily", dataframe)


def plot_by_week(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by week.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    weekly_data = dataframe.copy()
    weekly_data.index = weekly_data.index.strftime("%W")
    weekly_data = weekly_data.groupby("Date").sum()

    if len(weekly_data.index) < 3:
        return

    plt.figure(figsize=(10, 6))
    plot_by_payment(weekly_data)
    plt.xlabel("Week number")

    save_image(f"{path}/weekly", weekly_data)


def plot_by_month(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by week.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved
    """
    monthly_data = dataframe.copy()
    monthly_data.index = monthly_data.index.strftime("%m")
    monthly_data = monthly_data.groupby("Date").sum()

    if len(monthly_data.index) < 3:
        return

    plt.figure(figsize=(10, 6))
    plot_by_payment(monthly_data)
    plt.xlabel("Month")

    save_image(f"{path}/monthly", monthly_data)


if __name__ == "__main__":
    pass
