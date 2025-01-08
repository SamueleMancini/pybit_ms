from pybit_ms._http_manager import HTTPManager
from pybit_ms.market import Market_client
from pybit_ms.trade import Trade_client
from pybit_ms.account import Account_client
from pybit_ms.margin import Margin_client


class BybitAPI:
    """
    A client for interacting with Bybit's API using composition.
    
    Subclients:
        - trade: Handles trading-related endpoints.
        - leverage: Handles spot leverage token-related endpoints.
        - market: Handles market data endpoints.
        - account: Handles account management endpoints.
    """

    def __init__(self, api_key=None, api_secret=None, testnet=False, **kwargs):
        """
        Initialize the BybitAPI client.

        :param testnet: (bool) Whether to use the testnet environment.
        :param kwargs: Additional parameters to pass to the HTTPManager.
        """
        self.http_manager = HTTPManager(api_key=api_key, api_secret=api_secret, testnet=testnet, **kwargs)

        # Subclients
        self.trade = Trade_client(self.http_manager)
        self.leverage = Margin_client(self.http_manager)
        self.market = Market_client(self.http_manager)
        self.account = Account_client(self.http_manager)

    def __repr__(self):
        return f"BybitAPI(testnet={self.http_manager.testnet})"
