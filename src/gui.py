import tkinter as tk

from src.filehandling import load_config, save_config, change_date_today


class DateRangeWindow:
    def __init__(self, master):
        self.master = master
        master.title("Date Range Input")

        master.geometry("400x200")

        # Entry widgets for start and end dates
        self.start_label = tk.Label(master, text="Start Date (YYYY-MM-DD):")
        self.start_label.pack()

        self.start_entry = tk.Entry(master)
        self.start_entry.pack()

        self.end_label = tk.Label(master, text="End Date (YYYY-MM-DD):")
        self.end_label.pack()

        self.end_entry = tk.Entry(master)
        self.end_entry.pack()

        # Button to perform an action with the date range
        self.date_button = tk.Button(
            master,
            text="Submit dates",
            command=self.get_dates,
        )

        self.date_button.pack()

        # Button to perform an action today
        self.daily_button = tk.Button(
            master,
            text="Daily report",
            command=self.daily_report,
        )

        self.daily_button.pack()

    def get_dates(self) -> None:
        """Get user input from the entry widgets."""
        start_date = self.start_entry.get()
        end_date = self.end_entry.get()

        config = load_config("config")
        config["Start_date"], config["End_date"] = start_date, end_date
        save_config("config", config)

        self.master.destroy()

    def daily_report(self) -> None:
        """Get daily report."""
        change_date_today()

        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    date_range_window = DateRangeWindow(root)
    root.mainloop()
