from Bybit._http_manager import HTTPManager
from Bybit.market import Market_client
from Bybit.trade import Trade_client
from Bybit.account import Account_client
from Bybit.margin import Margin_client


class BybitAPI:
    """
    A client for interacting with Bybit's API using composition.
    
    Subclients:
        - trade: Handles trading-related endpoints.
        - leverage: Handles spot leverage token-related endpoints.
        - market: Handles market data endpoints.
        - account: Handles account management endpoints.
    """

    def __init__(self, testnet=False, **kwargs):
        """
        Initialize the BybitAPI client.

        :param testnet: (bool) Whether to use the testnet environment.
        :param kwargs: Additional parameters to pass to the HTTPManager.
        """
        self.http_manager = HTTPManager(testnet=testnet, **kwargs)

        # Subclients
        self.trade = Trade_client(self.http_manager)
        self.leverage = Margin_client(self.http_manager)
        self.market = Market_client(self.http_manager)
        self.account = Account_client(self.http_manager)

    def __repr__(self):
        return f"BybitAPI(testnet={self.http_manager.testnet})"
