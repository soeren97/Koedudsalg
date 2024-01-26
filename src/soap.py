from datetime import datetime

from zeep import Client
import pandas as pd


class DanDomainSOAPHandler:
    def __init__(self, config):
        self.wsdl_url = "https://api.hostedshop.io/service.wsdl"
        self.username = config["Username"]
        self.password = config["Password"]

        self.client = Client(wsdl=self.wsdl_url)
        self.client.service.Solution_Connect(
            Username=self.username,
            Password=self.password,
        )

        self.specify_format()

    def specify_format(self):
        self.client.service.Order_SetFields(
            "Id, Status, Payment, Vat, Total, DateDelivered"
        )

    def reformat_soap_response(self, responce: list[dict]):
        flat_data = [
            {
                "Date": datetime.strptime(entry["DateDelivered"][:10], "%Y-%m-%d"),
                "Incl. vat": entry["Total"] * (1 + entry["Vat"]),
                "PaymentMethod": entry["Payment"]["Title"],
            }
            for entry in responce
        ]
        response_df = pd.DataFrame(flat_data)

        credit_card_df = response_df[
            response_df["PaymentMethod"] == "Kreditkortbetaling"
        ]
        card_terminal_df = response_df[response_df["PaymentMethod"] == "Kortterminal"]
        cash_df = response_df[response_df["PaymentMethod"] == "Kontant betaling"]

        return [card_terminal_df, credit_card_df, cash_df]

    # def sum_up_soap_responce(self, df_list: list[pd.DataFrame]):

    def make_soap_request(self, start_date, end_date):
        try:
            result = self.client.service.Order_GetByDate(
                Start=start_date,
                End=end_date,
                Status="8",
            )
            result_dfs = self.reformat_soap_response(result)
            sums = [values.groupby("Date")["Incl. vat"].sum() for values in result_dfs]
            return sums
        except Exception as e:
            print(f"Error making SOAP request: {e}")


if __name__ == "__main__":
    pass
