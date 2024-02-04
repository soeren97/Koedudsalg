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

    def reformat_soap_response(self, responce: list[dict]) -> list[pd.DataFrame]:
        flat_data = [
            {
                "Date": datetime.strptime(entry["DateDelivered"], "%Y-%m-%d %H:%M:%S"),
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

    def make_soap_request(self, start_date: str, end_date: str) -> list[pd.DataFrame]:
        """Preform SOAP request.

        Args:
            start_date (str): Date of earliest orders.
            end_date (str): Date of latest orders.

        Returns:
            pd.DataFrame: Orders.
        """
        try:
            result = self.client.service.Order_GetByDate(
                Start=start_date,
                End=end_date,
                Status="8",
            )
            result_dfs = self.reformat_soap_response(result)
            return result_dfs
        except Exception as e:
            print(f"Error making SOAP request: {e}")


if __name__ == "__main__":
    pass
