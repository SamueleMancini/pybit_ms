from ._http_manager import HTTPManager
from .spot_leverage_token import SpotLeverageToken

class SpotLeverageHTTP:
    
    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

    def get_leveraged_token_info(self, **kwargs):
        """Query leverage token information

        https://bybit-exchange.github.io/docs/v5/lt/leverage-token-info
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotLeverageToken.GET_LEVERAGED_TOKEN_INFO}",
            query=kwargs,
        )

    def get_leveraged_token_market(self, **kwargs):
        """Get leverage token market information

        Required args:
            ltCoin (string): Abbreviation of the LT, such as BTC3L

        https://bybit-exchange.github.io/docs/v5/lt/leverage-token-reference
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotLeverageToken.GET_LEVERAGED_TOKEN_MARKET}",
            query=kwargs,
        )

    def purchase_leveraged_token(self, **kwargs):
        """Purchase levearge token

        Required args:
            ltCoin (string): Abbreviation of the LT, such as BTC3L
            ltAmount (string): Purchase amount

        https://bybit-exchange.github.io/docs/v5/lt/purchase
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotLeverageToken.PURCHASE}",
            query=kwargs,
            auth=True,
        )

    def redeem_leveraged_token(self, **kwargs):
        """Redeem leverage token

        Required args:
            ltCoin (string): Abbreviation of the LT, such as BTC3L
            quantity (string): Redeem quantity of LT

        https://bybit-exchange.github.io/docs/v5/lt/redeem
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotLeverageToken.REDEEM}",
            query=kwargs,
            auth=True,
        )

    def get_purchase_redemption_records(self, **kwargs):
        """Get purchase or redeem history

        https://bybit-exchange.github.io/docs/v5/lt/order-record
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotLeverageToken.GET_PURCHASE_REDEMPTION_RECORDS}",
            query=kwargs,
            auth=True,
        )
