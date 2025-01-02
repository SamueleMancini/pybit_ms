from ._http_manager import HTTPManager
from .position import Position


class PositionHTTP:

    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

    def get_positions(self, max_pages=None, **kwargs):
        """
        Query real-time position data, such as position size, cumulative realized PNL.

        Required args:
            category (string): Product type
                - Unified account: "linear", "option"
                - Normal account: "linear", "inverse"
            (Please note that category is not involved with business logic per the docs.)

        https://bybit-exchange.github.io/docs/v5/position

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g. limit, symbol, baseCoin, etc.).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of positions (across all pages) if max_pages is set.
        """
        path = f"{self.endpoint}{Position.GET_POSITIONS}"

        if max_pages:
            # Multi-page fetch
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
                max_pages=max_pages,
            )
        else:
            # Single-page fetch
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
            )

    def set_leverage(self, **kwargs):
        """Set the leverage

        Required args:
            category (string): Product type
                Unified account: linear
                Normal account: linear, inverse.

                Please note that category is not involved with business logic
            symbol (string): Symbol name
            buyLeverage (string): [0, max leverage of corresponding risk limit].
                Note: Under one-way mode, buyLeverage must be the same as sellLeverage
            sellLeverage (string): [0, max leverage of corresponding risk limit].
                Note: Under one-way mode, buyLeverage must be the same as sellLeverage

        https://bybit-exchange.github.io/docs/v5/position/leverage
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_LEVERAGE}",
            query=kwargs,
            auth=True,
        )

    def switch_margin_mode(self, **kwargs):
        """Select cross margin mode or isolated margin mode

        Required args:
            category (string): Product type. linear,inverse

                Please note that category is not involved with business logicUnified account is not applicable
            symbol (string): Symbol name
            tradeMode (integer): 0: cross margin. 1: isolated margin
            buyLeverage (string): The value must be equal to sellLeverage value
            sellLeverage (string): The value must be equal to buyLeverage value

        https://bybit-exchange.github.io/docs/v5/position/cross-isolate
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SWITCH_MARGIN_MODE}",
            query=kwargs,
            auth=True,
        )

    def switch_position_mode(self, **kwargs):
        """
        It supports to switch the position mode for USDT perpetual and Inverse futures.
        If you are in one-way Mode, you can only open one position on Buy or Sell side.
        If you are in hedge mode, you can open both Buy and Sell side positions simultaneously.

        Required args:
            category (string): Product type. linear,inverse

                Please note that category is not involved with business logicUnified account is not applicable

        https://bybit-exchange.github.io/docs/v5/position/position-mode
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SWITCH_POSITION_MODE}",
            query=kwargs,
            auth=True,
        )

    def set_trading_stop(self, **kwargs):
        """Set the take profit, stop loss or trailing stop for the position.

        Required args:
            category (string): Product type
                Unified account: linear
                Normal account: linear, inverse.

                Please note that category is not involved with business logic
            symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/position/trading-stop
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_TRADING_STOP}",
            query=kwargs,
            auth=True,
        )

    def set_auto_add_margin(self, **kwargs):
        """Turn on/off auto-add-margin for isolated margin position

        Required args:
            category (string): Product type. linear
            symbol (string): Symbol name
            autoAddMargin (integer): Turn on/off. 0: off. 1: on

        https://bybit-exchange.github.io/docs/v5/position/add-margin
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Position.SET_AUTO_ADD_MARGIN}",
            query=kwargs,
            auth=True,
        )
    
    def get_executions(self, max_pages=None, **kwargs):
        """
        Query users' execution records, sorted by execTime in descending order.

        Required args:
            category (string):
                - Unified account: "spot", "linear", "option"
                - Normal account: "linear", "inverse"

        https://bybit-exchange.github.io/docs/v5/order/execution

        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g., symbol, startTime, endTime, limit).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of execution records if max_pages is specified.
        """
        path = f"{self.endpoint}{Position.GET_EXECUTIONS}"

        if max_pages:
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
                max_pages=max_pages,
            )
        else:
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
            )

    def get_closed_pnl(self, max_pages=None, **kwargs):
        """
        Query user's closed profit and loss records.
        The results are sorted by createdTime in descending order.

        Required args:
            category (string):
                - Unified account: "linear"
                - Normal account: "linear", "inverse"

        https://bybit-exchange.github.io/docs/v5/position/close-pnl

        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g., symbol, startTime, endTime, limit).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of PnL records if max_pages is specified.
        """
        path = f"{self.endpoint}{Position.GET_CLOSED_PNL}"

        if max_pages:
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,  # Requires authentication
                max_pages=max_pages,
            )
        else:
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
            )
