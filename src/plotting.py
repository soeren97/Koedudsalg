from datetime import timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.constants import PLOTTING_COLORS


def save_image(path: str, dataframe: pd.DataFrame) -> None:
    """Save plotted image.

    Args:
        path (str): path to folder where image will be saved.
        dataframe (pd.DateFrame): Data to be plotted.
    """
    plt.ylabel("Sales Incl. vat [DKK]")
    plt.tight_layout()
    plt.xlim(
        dataframe.index.min() - timedelta(hours=12),
        dataframe.index.max() + timedelta(hours=12),
    )
    plt.ylim(bottom=0)
    plt.legend()
    plt.savefig(f"Reports/{path}.png")
    plt.close()


def plot_weekend(dataframe: pd.DataFrame) -> None:
    """Show the weekend in a plot.

    Args:
        dataframe (pd.DataFrame): Data to be plotted.
        date_index (pd.Index, optional): Index in date format. Needed for bar chart. Defaults to None.
    """
    saturdays = [date for date in dataframe.index if date.weekday() == 5]

    for saturday in saturdays:
        plt.axvspan(
            saturday,
            saturday + np.timedelta64(2, "D"),
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

    plt.plot(
        card,
        label="Credit card",
        color=PLOTTING_COLORS[0],
        alpha=0.7,
    )
    plt.plot(
        terminal,
        label="Card terminal",
        color=PLOTTING_COLORS[1],
        alpha=0.7,
    )
    plt.plot(
        cash,
        label="Cash payment",
        color=PLOTTING_COLORS[2],
        alpha=0.7,
    )

    plt.fill_between(
        card.index,
        terminal,
        card,
        alpha=0.4,
        color=PLOTTING_COLORS[0],
        label=None,
    )
    plt.fill_between(
        card.index,
        cash,
        terminal,
        alpha=0.4,
        color=PLOTTING_COLORS[1],
        label=None,
    )
    plt.fill_between(
        card.index,
        0,
        cash,
        alpha=0.4,
        color=PLOTTING_COLORS[2],
        label=None,
    )


def plot_by_day(dataframe: pd.DataFrame, path: str) -> None:
    """Plot sales by day.

    Args:
        dataframe (pd.DataFrame): Daily sales.
        path (str): Path to folder where image will be saved.
    """
    if len(dataframe.index) < 3:
        return

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
        path (str): Path to folder where image will be saved.
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
        path (str): Path to folder where image will be saved.
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


def plot_bar_chart(dataframe: pd.DataFrame, path: str) -> None:
    """Plot a histogram of daily sales.

    Args:
        dataframe (pd.DataFrame): Data to be ploted.
        path (str): Path to folder where image will be saved
    """
    # if len(dataframe.index) < 3:
    #     return

    plt.figure(figsize=(10, 6))

    bar_spacing = timedelta(hours=3)

    # Create a bar chart for each column
    for i, col in enumerate(dataframe.columns):
        plt.bar(
            dataframe.index + i * bar_spacing - bar_spacing * 2,
            dataframe[col],
            width=0.1,
            label=col,
            alpha=0.7,
            color=PLOTTING_COLORS[i],
        )
        for j, value in enumerate(dataframe[col]):
            if value == 0:
                continue
            plt.text(
                dataframe.index[j] + i * bar_spacing,
                value + 1,  # Adjust the vertical position of the text as needed
                str(value),
                ha="center",
                rotation=30,
            )

    plt.xticks(
        ticks=dataframe.index,
        labels=dataframe.index.strftime("%Y/%m/%d"),
        rotation=30,
        ha="right",
    )

    plot_weekend(dataframe)

    save_image(f"{path}/bar_chart", dataframe)


if __name__ == "__main__":
    pass
