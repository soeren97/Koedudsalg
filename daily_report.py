from src.filehandling import save_dataframe, load_config, change_date_today
from src.plotting import get_all_plots
from src.data_handler import get_and_clean_data


def main():
    """Create a daily report."""
    dd_config = load_config("config")

    change_date_today()

    report = get_and_clean_data(dd_config)

    path = f"{report.index[0].strftime('%Y-%m-%d')}_to_{report.index[-1].strftime('%Y-%m-%d')}"

    save_dataframe(report, path)

    get_all_plots(report, path)


if __name__ == "__main__":
    main()
