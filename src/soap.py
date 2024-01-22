import requests


class DanDomainHandler:
    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = None
        self.query = None
        self.variables = None

    def set_token(self, token: str) -> None:
        """Set the access token for the request.

        Args:
            token (str): Access token.
        """
        self.headers = token

    def set_query(self) -> None:
        """Set the query for the request."""
        self.query = """
            query Orders($startDate: String!, $endDate: String!) {
                orders(startDate: $startDate, endDate: $endDate) {
                    data {
                        id
                        orderDate
                    }
                }
            }
        """

    def set_variables(self, start_date: str, end_date: str) -> None:
        """Set the variables for the request.

        Args:
            start_date (str): Start date of request.
            end_date (str): End date of request.
        """
        self.variables = {"startDate": start_date, "endDate": end_date}

    def make_graphql_request(self):
        """
        Make a GraphQL request.

        Returns:
            dict: The JSON response from the GraphQL server.
        """
        payload = {"query": self.query, "variables": self.variables}
        response = requests.post(self.url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"GraphQL request failed with status code {response.status_code}: {response.text}"
            )


if __name__ == "__main__":
    pass
