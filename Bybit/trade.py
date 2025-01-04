from Bybit._http_manager import HTTPManager
from enum import Enum
import pandas as pd
from IPython.display import display_html



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

    def place_order(self, category, symbol, side, orderType, qty, **kwargs):
        """This method supports to create the order for Spot, Margin trading, USDT perpetual, USDC perpetual, USDC futures, Inverse Futures and Options.

        Supported order type (orderType):
            Limit order: orderType=Limit, it is necessary to specify order qty and price.
            Market order: orderType=Market, execute at the best price in the Bybit market until the transaction is completed. When selecting a market order, the "price" can be empty. In the futures trading system, in order to protect the serious slippage of the market order, the Bybit trading system will convert the market order into a limit order for matching. will be cancelled. The slippage threshold refers to the percentage that the order price deviates from the latest transaction price. The current threshold is set to 3% for BTC contracts and 5% for other contracts.

        Supported timeInForce strategy:
            GTC
            IOC
            FOK
            PostOnly: If the order would be filled immediately when submitted, it will be cancelled. The purpose of this is to protect your order during the submission process. If the matching system cannot entrust the order to the order book due to price changes on the market, it will be cancelled. For the PostOnly order type, the quantity that can be submitted in a single order is more than other types of orders, please refer to the parameter lotSizeFilter > postOnlyMaxOrderQty in the instruments-info endpoint.

        How to create conditional order:
            When submitting an order, if triggerPrice is set, the order will be automatically converted into a conditional order. In addition, the conditional order does not occupy the margin. If the margin is insufficient after the conditional order is triggered, the order will be cancelled.

        Take profit / Stop loss: You can set TP/SL while placing orders. Besides, you could modify the position's TP/SL.

        Order quantity: The quantity of perpetual contracts you are going to buy/sell. For the order quantity, Bybit only supports positive number at present.

        Order price: Place a limit order, this parameter is required. If you have position, the price should be higher than the liquidation price. For the minimum unit of the price change, please refer to the priceFilter > tickSize field in the instruments-info endpoint.

        orderLinkId: You can customize the active order ID. We can link this ID to the order ID in the system. Once the active order is successfully created, we will send the unique order ID in the system to you. Then, you can use this order ID to cancel active orders, and if both orderId and orderLinkId are entered in the parameter input, Bybit will prioritize the orderId to process the corresponding order. Meanwhile, your customized order ID should be no longer than 36 characters and should be unique.

        Open orders up limit:
            Perps & Futures:
                a) Each account can hold a maximum of 500 active orders simultaneously per symbol.
                b) conditional orders: each account can hold a maximum of 10 active orders simultaneously per symbol.
            Spot: 500 orders in total, including a maximum of 30 open TP/SL orders, a maximum of 30 open conditional orders for each symbol per account
            Option: a maximum of 50 open orders per account

        Rate limit:
            Please refer to rate limit table. If you need to raise the rate limit, please contact your client manager or submit an application via here

        Risk control limit notice:
            Bybit will monitor on your API requests. When the total number of orders of a single user (aggregated the number of orders across main account and sub-accounts) within a day (UTC 0 - UTC 24) exceeds a certain upper limit, the platform will reserve the right to remind, warn, and impose necessary restrictions. Customers who use API default to acceptance of these terms and have the obligation to cooperate with adjustments.
        
        Required args:
            category (string): Product type Unified account: linear, inverse, spot, option. Normal account: linear, inverse, spot. Please note that category is not involved with business logic
            symbol (string): Symbol name
            side (string): Buy, Sell
            orderType (string): Market, Limit
            qty (string): Order quantity
        
        https://bybit-exchange.github.io/docs/v5/order/create-order
        """
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["side"] = side
        kwargs["orderType"] = orderType
        kwargs["qty"] = qty
        print(kwargs)
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
    
    def get_open_orders(
            self,
            category,
            symbol=None,
            settle_coin=None,
            base_coin=None,
            order_id=None,
            order_link_id=None,
            max_pages=None,
            raw=False,
            return_list=False,
            **kwargs
        ):
            """
            Query unfilled or partially filled orders in real-time.
            To query older order records, please use the order history interface.

            Args:
                category (str): 
                    - Unified account: "spot", "linear", "option"
                    - Normal account: "linear", "inverse"
                symbol (str, optional): Only required if category != 'spot'. 
                    Depending on your usage, you could also provide `settle_coin` or `base_coin` instead.
                settle_coin (str, optional): Settlement coin (e.g., "USDT").
                base_coin (str, optional): Base coin (e.g., "BTC").
                order_id (str, optional): Specific order ID to query.
                order_link_id (str, optional): Client-generated order ID.
                max_pages (int, optional): If set, fetch multiple pages up to this limit.
                raw (bool, optional): If True, returns the raw Bybit API response. Defaults to False.
                return_list (bool, optional): If True, returns a list of orders instead 
                    of displaying them as a styled DataFrame. Defaults to False.
                **kwargs: Additional query parameters (e.g., "limit", etc.).

            Returns:
                dict: The raw API response if `raw` is True and `max_pages` is None.
                list: If `raw` is True and `max_pages` is set, returns paginated raw data.
                dict: An empty dict if there are no orders (and `raw` is False).
                list: If `return_list` is True, returns the processed open orders as a list of dicts.
                None: If neither `raw` nor `return_list` is True, displays a styled DataFrame in a Jupyter environment.
            """

            def is_not_zero(value):
                """Check if a value is numeric and not zero."""
                try:
                    num = float(value)
                    return num != 0
                except ValueError:
                    return False

            def format_with_spaces(value):
                """
                Format numeric values to have commas replaced by spaces, 
                e.g., 1,234.56 -> 1 234.56. Only applies if `value` is numeric.
                """
                try:
                    num = float(value)
                    # If the number is an integer, reduce it to int for display (e.g., 100.0 -> 100).
                    if num.is_integer():
                        num = int(num)

                    # If number is large, insert thousands separators (replacing commas with spaces).
                    if num > 99999:
                        formatted = f"{num:,}".replace(",", " ")
                    else:
                        formatted = str(num)
                except ValueError:
                    formatted = value
                return formatted

            def format_dashboard(df, red='Ask', green='Bid', lime='Value'):
                """
                Apply custom styling to a pandas DataFrame for display in a Jupyter environment.
                """
                def style_specific_cell(row):
                    styles = []
                    for col_name in row.keys():
                        if green in col_name:
                            styles.append(
                                'background-color: lightgreen; color: black; font-weight: bold;'
                            )
                        elif red in col_name:
                            styles.append(
                                'background-color: salmon; color: black; font-weight: bold;'
                            )
                        elif lime in col_name:
                            styles.append('background-color: black; color: lime')
                        else:
                            styles.append('background-color: black')
                    return styles

                styled = df.style.apply(style_specific_cell, axis=1)
                # Right-align columns
                styled = styled.set_properties(**{'text-align': 'right'})
                # Add a border and control table sizing
                styled = styled.set_table_attributes(
                    'style="font-size: 12px; border: 2px solid black;"'
                )

                styled = styled.format(format_with_spaces)

                header_styles = [
                    {
                        'selector': 'caption',
                        'props': [
                            ('color', 'white'),
                            ('font-size', '16px'),
                            ('font-weight', 'bold'),
                            ('text-align', 'center'),
                            ('caption-side', 'top')
                        ]
                    }
                ]
                styled = styled.set_table_styles(header_styles)

                return styled

            # Build the request parameters
            path = f"{self.endpoint}{Trade.GET_OPEN_ORDERS}"
            kwargs["category"] = category
            kwargs["symbol"] = symbol
            kwargs["settleCoin"] = settle_coin
            kwargs["baseCoin"] = base_coin
            kwargs["orderId"] = order_id
            kwargs["orderLinkId"] = order_link_id

            # If max_pages is set, use the paginated endpoint
            if max_pages:
                data_list, _ = self._http_manager._submit_paginated_request(
                    method="GET",
                    path=path,
                    query=kwargs,
                    auth=True,
                    max_pages=max_pages,
                )
            else:
                # Otherwise, make a single request
                response = self._http_manager._submit_request(
                    method="GET",
                    path=path,
                    query=kwargs,
                    auth=True,
                )
                # If raw is requested, return the entire response
                if raw:
                    return response

                data_list = response.get('result', {}).get('list', [])
                if not data_list:
                    # If the list is empty, return an empty dictionary
                    return {}

            # If raw was requested (and we had multiple pages), return the raw data_list
            if raw:
                return data_list

            # Filter and transform each order in data_list
            keys_to_keep = [
                'symbol', 'orderType', 'side', 'price', 'qty', 'leavesQty', 'isLeverage',
                'timeInForce', 'takeProfit', 'stopLoss', 'triggerPrice', 'tpLimitPrice',
                'slLimitPrice', 'orderStatus', 'triggerDirection', 'triggerBy',
                'orderLinkId', 'orderId', 'createdTime'
            ]

            for idx, item in enumerate(data_list):
                filtered = {k: item[k] for k in keys_to_keep if k in item}

                # Convert timestamp to human-readable
                if 'createdTime' in filtered:
                    filtered['createdTime'] = pd.to_datetime(
                        int(filtered['createdTime']), unit='ms'
                    ).strftime('%Y-%m-%d %H:%M:%S')

                # Take-profit logic
                if is_not_zero(filtered['takeProfit']) or is_not_zero(filtered['tpLimitPrice']):
                    filtered['takeProfit'] = (
                        f"{'limit' if is_not_zero(filtered['tpLimitPrice']) else 'market'}:\n \
                        {format_with_spaces(filtered['takeProfit']) if is_not_zero(filtered['takeProfit']) \
                        else format_with_spaces(filtered['tpLimitPrice'])}"
                    )
                else:
                    filtered['takeProfit'] = '-'
                
                filtered.pop('tpLimitPrice', None)

                # Stop-loss logic
                if is_not_zero(filtered['stopLoss']) or is_not_zero(filtered['slLimitPrice']):
                    filtered['stopLoss'] = (
                        f"{'limit' if is_not_zero(filtered['slLimitPrice']) else 'market'}:\n \
                        {format_with_spaces(filtered['stopLoss']) if is_not_zero(filtered['stopLoss']) \
                        else format_with_spaces(filtered['slLimitPrice'])}"
                    )
                else:
                    filtered['stopLoss'] = '-'
                
                filtered.pop('slLimitPrice', None)

                # Trigger price logic
                if is_not_zero(filtered['triggerPrice']):
                    filtered['triggerPrice'] = (
                        f"{'\u2191' if filtered['triggerDirection'] == '1' else '\u2193'} \
                        {filtered['orderStatus']} ({filtered['triggerBy']}):\n \
                        {format_with_spaces(filtered['triggerPrice'])}"
                    )
                else:
                    filtered['triggerPrice'] = '-'
                
                filtered.pop('triggerDirection', None)
                filtered.pop('orderStatus', None)
                filtered.pop('triggerBy', None)

                filtered['orderLinkId'] = f"link:\n{filtered['orderLinkId']}"
                filtered['orderId'] = f"id:\n{filtered['orderId']}"

                # If not spot, remove isLeverage
                if category != "spot":
                    filtered.pop('isLeverage', None)

                data_list[idx] = filtered

            # If returning a simple list is requested, return it
            if return_list:
                return data_list

            # Otherwise, build a DataFrame
            df = pd.DataFrame(data_list)
            # Rename 'leavesQty' to 'unfilledQty'
            if 'leavesQty' in df.columns:
                df.rename(columns={'leavesQty': 'unfilledQty'}, inplace=True)

            styled_df = format_dashboard(df).set_caption("Open Orders")
            html = styled_df._repr_html_()
            display_html(html, raw=True)
            return None














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
