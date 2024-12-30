from ._http_manager import HTTPManager
from ._market import MarketHTTP
from ._trade import TradeHTTP
from ._account import AccountHTTP
from ._spot_leverage_token import SpotLeverageHTTP


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
        self.trade = TradeHTTP(self.http_manager)
        self.leverage = SpotLeverageHTTP(self.http_manager)
        self.market = MarketHTTP(self.http_manager)
        self.account = AccountHTTP(self.http_manager)

    def __repr__(self):
        return f"BybitAPI(testnet={self.http_manager.testnet})"
