import tkinter as tk

from src.filehandling import save_dataframe, load_config
from src.plotting import get_all_plots
from src.data_handler import get_and_clean_data
from src.gui import DateRangeWindow


def main():
    """Create a report based on user input."""
    dd_config = load_config("config")

    report = get_and_clean_data(dd_config, sort_by_order=False)

    path = f"{report.index[0].strftime('%Y-%m-%d')}_to_{report.index[-1].strftime('%Y-%m-%d')}"

    save_dataframe(report, path)

    get_all_plots(report, path)


if __name__ == "__main__":
    # root = tk.Tk()
    # date_range_window = DateRangeWindow(root)
    # root.mainloop()
    main()
