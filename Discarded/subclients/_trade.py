from ._http_manager import HTTPManager
from .trade import Trade


class TradeHTTP:
    
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
