from Bybit._http_manager import HTTPManager
from enum import Enum


class Trade(str, Enum):
    PLACE_ORDER = "/v5/order/create"
    AMEND_ORDER = "/v5/order/amend"
    CANCEL_ORDER = "/v5/order/cancel"
    GET_OPEN_ORDERS = "/v5/order/realtime"
    CANCEL_ALL_ORDERS = "/v5/order/cancel-all"
    GET_ORDER_HISTORY = "/v5/order/history"
    BATCH_PLACE_ORDER = "/v5/order/create-batch"
    BATCH_AMEND_ORDER = "/v5/order/amend-batch"
    BATCH_CANCEL_ORDER = "/v5/order/cancel-batch"
    GET_BORROW_QUOTA = "/v5/order/spot-borrow-check"
    GET_POSITIONS = "/v5/position/list"
    SET_LEVERAGE = "/v5/position/set-leverage"
    SWITCH_MARGIN_MODE = "/v5/position/switch-isolated"
    SWITCH_POSITION_MODE = "/v5/position/switch-mode"
    SET_TRADING_STOP = "/v5/position/trading-stop"
    SET_AUTO_ADD_MARGIN = "/v5/position/set-auto-add-margin"
    GET_EXECUTIONS = "/v5/execution/list"
    GET_CLOSED_PNL = "/v5/position/closed-pnl"

    def __str__(self) -> str:
        return self.value


class Trade_client:
    
    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

    def place_order(self, **kwargs):
        """This method supports to create the order for spot, spot margin, linear perpetual, inverse futures and options.

        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic
            symbol (string): Symbol name
            side (string): Buy, Sell
            orderType (string): Market, Limit
            qty (string): Order quantity
        
        https://bybit-exchange.github.io/docs/v5/order/create-order
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

    def amend_order(self, **kwargs):
        """Unified account covers: Linear contract / Options
        Normal account covers: USDT perpetual / Inverse perpetual / Inverse futures

        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic
            symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/order/amend-order
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_order(self, **kwargs):
        """Unified account covers: Spot / Linear contract / Options
        Normal account covers: USDT perpetual / Inverse perpetual / Inverse futures

        Required args:
            category (string): Product type Unified account: spot, linear, optionNormal account: linear, inverse. Please note that category is not involved with business logic
            symbol (string): Symbol name
            orderId (string): Order ID. Either orderId or orderLinkId is required
            orderLinkId (string): User customised order ID. Either orderId or orderLinkId is required

        https://bybit-exchange.github.io/docs/v5/order/cancel-order
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.CANCEL_ORDER}",
            query=kwargs,
            auth=True,
        )
    
    def get_open_orders(self, max_pages=None, **kwargs):
        """
        Query unfilled or partially filled orders in real-time.
        To query older order records, please use the order history interface.

        Required args:
            category (string):
                - Unified account: "spot", "linear", "option"
                - Normal account: "linear", "inverse"
            (Please note that category is not involved with business logic.)

        https://bybit-exchange.github.io/docs/v5/order/open-order

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g., symbol, limit, etc.).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of open orders if max_pages is set.
        """
        path = f"{self.endpoint}{Trade.GET_OPEN_ORDERS}"

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

    def cancel_all_orders(self, **kwargs):
        """Cancel all open orders

        Required args:
            category (string): Product type
                Unified account: spot, linear, option
                Normal account: linear, inverse.

                Please note that category is not involved with business logic. If cancel all by baseCoin, it will cancel all linear & inverse orders

        https://bybit-exchange.github.io/docs/v5/order/cancel-all
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.CANCEL_ALL_ORDERS}",
            query=kwargs,
            auth=True,
        )
    
    def get_order_history(self, max_pages=None, **kwargs):
        """
        Query order history. As order creation/cancellation is asynchronous, the data returned from this endpoint may delay.
        If you want to get real-time order information, you could query this endpoint or rely on the websocket stream (recommended).

        Required args:
            category (string): Product type
                - Unified account: "spot", "linear", "option"
                - Normal account: "linear", "inverse"
            (Please note that category is not involved with business logic.)

        https://bybit-exchange.github.io/docs/v5/order/order-list

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g., symbol, limit, startTime, endTime, etc.).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of order history items if max_pages is set.
        """
        path = f"{self.endpoint}{Trade.GET_ORDER_HISTORY}"

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

    def place_batch_order(self, **kwargs):
        """Covers: Option (Unified Account)

        Required args:
            category (string): Product type. option
            request (array): Object
            > symbol (string): Symbol name
            > side (string): Buy, Sell
            > orderType (string): Market, Limit
            > qty (string): Order quantity

        https://bybit-exchange.github.io/docs/v5/order/batch-place
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

    def amend_batch_order(self, **kwargs):
        """Covers: Option (Unified Account)

        Required args:
            category (string): Product type. option
            request (array): Object
            > symbol (string): Symbol name
            > orderId (string): Order ID. Either orderId or orderLinkId is required
            > orderLinkId (string): User customised order ID. Either orderId or orderLinkId is required

        https://bybit-exchange.github.io/docs/v5/order/batch-amend
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

    def cancel_batch_order(self, **kwargs):
        """This endpoint allows you to cancel more than one open order in a single request.

        Required args:
            category (string): Product type. option
            request (array): Object
            > symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/order/batch-cancel
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_CANCEL_ORDER}",
            query=kwargs,
            auth=True,
        )

    def get_borrow_quota(self, **kwargs):
        """Query the available balance for Spot trading and Margin trading.

        Required args:
            category (string): Product type. spot
            symbol (string): Symbol name
            side (string): Transaction side. Buy,Sell

        https://bybit-exchange.github.io/docs/v5/order/spot-borrow-quota
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Trade.GET_BORROW_QUOTA}",
            query=kwargs,
            auth=True,
        )

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
        path = f"{self.endpoint}{Trade.GET_POSITIONS}"

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
            path=f"{self.endpoint}{Trade.SET_LEVERAGE}",
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
            path=f"{self.endpoint}{Trade.SWITCH_MARGIN_MODE}",
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
            path=f"{self.endpoint}{Trade.SWITCH_POSITION_MODE}",
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
            path=f"{self.endpoint}{Trade.SET_TRADING_STOP}",
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
            path=f"{self.endpoint}{Trade.SET_AUTO_ADD_MARGIN}",
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
        path = f"{self.endpoint}{Trade.GET_EXECUTIONS}"

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
        path = f"{self.endpoint}{Trade.GET_CLOSED_PNL}"

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
