from pybit_ms._http_manager import HTTPManager
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


    def place_order(
        self,
        category: str,
        symbol: str,
        side: str,
        order_type: str,
        qty: str,
        price: str = None,
        time_in_force: str = None,
        market_unit: str = "baseCoin",
        is_leverage: int = 0,
        trigger_price: str = None,
        trigger_by: str = None,
        position_idx: int = None,
        order_link_id: str = None,
        take_profit: str = None,
        stop_loss: str = None,
        tp_trigger_by: str = None,
        trigger_direction: int = None,
        sl_trigger_by: str = None,
        tp_limit_price: str = None,
        sl_limit_price: str = None,
        tp_order_type: str = None,
        sl_order_type: str = None,
        tpsl_mode: str = None,
        reduce_only: bool = False,
        raw: bool = False,
        **kwargs
    ) -> str:
        """
        Create an order for Spot, Margin, Perpetual (USDT/USDC/Inverse), Futures, or Options.

        Supported order types:
            - Limit order (`order_type="Limit"`): specify order quantity and price.
            - Market order (`order_type="Market"`): executes at the best price until filled.
              In Bybit, large market orders are internally converted to limit orders at a 
              certain slippage threshold to protect users from excessive slippage.
        
        Supported `timeInForce` strategies:
            - GTC (Good Till Cancelled)
            - IOC (Immediate or Cancel)
            - FOK (Fill or Kill)
            - PostOnly (ensures the order doesn't immediately match; canceled otherwise)

        Conditional orders (only for linear contracts):
            - If `trigger_price` is set, the order becomes a conditional order. 
            - Conditional orders do not occupy margin until triggered.

        Take profit / Stop loss:
            - Set `take_profit` and/or `stop_loss` at time of order placement.
            - Optionally configure limit-based TP/SL with `tp_limit_price`/`sl_limit_price`.

        Order quantity & price:
            - `qty` must be a positive number (string format accepted by Bybit).
            - If placing a limit order, `price` is required unless using a market order.
            - The price must respect the instrument's tick size (see `priceFilter` in instruments info).

        Rate limit & risk control:
            - Bybit imposes daily and per-symbol limits on open orders, conditional orders,
              and total order counts. Exceeding these may result in warnings or restrictions.

        Args:
            category (str): Product type. Unified account: "linear", "inverse", "spot", "option".
                Normal account: "linear", "inverse", "spot".
            symbol (str): Symbol name (e.g., "BTCUSDT").
            side (str): "Buy" or "Sell".
            order_type (str): "Market" or "Limit".
            qty (str): Quantity to trade (as a string; Bybit accepts string inputs).
            price (str, optional): Price for limit orders. Defaults to None.
            time_in_force (str, optional): One of "GTC", "IOC", "FOK", "PostOnly". 
                If None, defaults to "IOC" for Market and "GTC" for Limit orders.
            market_unit (str, optional): If placing a spot trade, 
                "baseCoin" (quantity is in base asset units) or 
                "quoteCoin" (quantity is in quote asset units). Defaults to "baseCoin".
            is_leverage (int, optional): Leverage flag. 0 for off, 1 for on. Defaults to 0.
            trigger_price (str, optional): Price at which a conditional (stop) order should trigger.
            trigger_by (str, optional): Mechanism for triggering (e.g., "LastPrice", "MarkPrice").
            position_idx (int, optional): Position index for multi-position mode. 
                1 for one-way, 2/3 for hedge mode.
            order_link_id (str, optional): Custom client-defined order ID. 
                Maximum length is 36 characters.
            take_profit (str, optional): TP price. If set, a TP order will be placed.
            stop_loss (str, optional): SL price. If set, an SL order will be placed.
            tp_trigger_by (str, optional): Price mechanism for triggering take profit.
            sl_trigger_by (str, optional): Price mechanism for triggering stop loss.
            tp_limit_price (str, optional): TP limit price if `tp_order_type="Limit"`.
            sl_limit_price (str, optional): SL limit price if `sl_order_type="Limit"`.
            tp_order_type (str, optional): "Market" or "Limit" for the TP order type.
            sl_order_type (str, optional): "Market" or "Limit" for the SL order type.
            tpsl_mode (str, optional): E.g., "Full" or "Partial" for TP/SL behavior.
            reduce_only (bool, optional): Whether the order should only reduce a position. 
                Defaults to False.
            raw (bool, optional): If True, return raw Bybit API response (dict). 
                Otherwise, return a string with the order ID or link ID. Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API (e.g., "orderIv" for options).

        Returns:
            str | dict:
                - If `raw=True`, returns the raw response (dict).
                - Otherwise, returns a string:
                  - If `order_link_id` is provided, returns `"orderLinkId: <...>"`
                  - Otherwise, returns `"orderId: <...>"`.

        Note:
            https://bybit-exchange.github.io/docs/v5/order/create-order
        """
        # If no time_in_force was provided, choose defaults based on order_type
        if time_in_force is None:
            if order_type.lower() == 'market':
                time_in_force = 'IOC'
            else:
                time_in_force = 'GTC'

        # Build the payload
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["side"] = side
        kwargs["orderType"] = order_type
        kwargs["qty"] = qty
        kwargs["price"] = price
        kwargs["timeInForce"] = time_in_force
        kwargs["marketUnit"] = market_unit
        kwargs["isLeverage"] = is_leverage
        kwargs["triggerPrice"] = trigger_price
        kwargs["triggerBy"] = trigger_by
        kwargs["triggerDirection"] = trigger_direction
        kwargs["positionIdx"] = position_idx
        kwargs["orderLinkId"] = order_link_id
        kwargs["takeProfit"] = take_profit
        kwargs["stopLoss"] = stop_loss
        kwargs["tpTriggerBy"] = tp_trigger_by
        kwargs["slTriggerBy"] = sl_trigger_by
        kwargs["tpLimitPrice"] = tp_limit_price
        kwargs["slLimitPrice"] = sl_limit_price
        kwargs["tpOrderType"] = tp_order_type
        kwargs["slOrderType"] = sl_order_type
        kwargs["tpslMode"] = tpsl_mode
        kwargs["reduceOnly"] = reduce_only

        # Send the request
        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return raw response if requested
        if raw:
            return response

        # If order_link_id was provided, return that
        if order_link_id is not None:
            link_id = response.get('result', {}).get('orderLinkId', [])
            return f"orderLinkId: {link_id}"

        # Otherwise, return system-generated order ID
        order_id = response.get('result', {}).get('orderId', [])
        return f"orderId: {order_id}"


    def place_spot_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        qty: str,
        price: str = None,
        category: str = "spot",
        time_in_force: str = None,
        market_unit: str = "baseCoin",
        is_leverage: int = 0,
        order_link_id: str = None,
        take_profit: str = None,
        stop_loss: str = None,
        tp_limit_price: str = None,
        sl_limit_price: str = None,
        tp_order_type: str = None,
        sl_order_type: str = None,
        raw: bool = False,
        **kwargs
    ) -> str:
        """
        Place a spot order (Market or Limit) on Bybit. Optionally configure 
        margin, take-profit/stop-loss and additional parameters.

        Args:
            symbol (str): Symbol name, e.g., "BTCUSDT".
            side (str): "Buy" or "Sell".
            order_type (str): "Market" or "Limit".
            qty (str): Order quantity as a string (Bybit expects string inputs).
            price (str, optional): Limit price. Required if `order_type="Limit"`.
                                  Defaults to None.
            category (str, optional): Product category. By default "spot".
            time_in_force (str, optional): Order execution constraint. One of:
                "GTC", "IOC", "FOK", "PostOnly". If None, defaults to:
                - "IOC" if `order_type="Market"`
                - "GTC" otherwise.
            market_unit (str, optional): If placing a spot trade, indicates the unit
                of quantity ("baseCoin" or "quoteCoin"). Defaults to "baseCoin".
            is_leverage (int, optional): Leverage flag (0 for off, 1 for on). Defaults to 0.
            order_link_id (str, optional): Custom client-defined order ID.
            take_profit (str, optional): If set, places a take profit (market or limit) order.
            stop_loss (str, optional): If set, places a stop loss (market or limit) order.
            tp_limit_price (str, optional): Limit price for TP if `tp_order_type="Limit"`.
            sl_limit_price (str, optional): Limit price for SL if `sl_order_type="Limit"`.
            tp_order_type (str, optional): "Market" or "Limit" for TP order type.
            sl_order_type (str, optional): "Market" or "Limit" for SL order type.
            raw (bool, optional): If True, return the raw response (dict).
            **kwargs: Additional parameters for Bybit's API.

        Returns:
            str | dict:
                - If `raw=True`, returns the raw API response (dict).
                - Otherwise, returns a string describing either:
                  "orderLinkId: <...>" or "orderId: <...>" based on
                  whether `order_link_id` was provided.
        
        Notes:
              https://bybit-exchange.github.io/docs/v5/order/create-order
        """

        # Assign a default time_in_force if not provided
        if time_in_force is None:
            if order_type.lower() == 'market':
                time_in_force = 'IOC'
            else:
                time_in_force = 'GTC'

        # Build request parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["side"] = side
        kwargs["orderType"] = order_type
        kwargs["qty"] = qty
        kwargs["price"] = price
        kwargs["timeInForce"] = time_in_force
        kwargs["marketUnit"] = market_unit
        kwargs["isLeverage"] = is_leverage
        kwargs["orderLinkId"] = order_link_id
        kwargs["takeProfit"] = take_profit
        kwargs["stopLoss"] = stop_loss
        kwargs["tpLimitPrice"] = tp_limit_price
        kwargs["slLimitPrice"] = sl_limit_price
        kwargs["tpOrderType"] = tp_order_type
        kwargs["slOrderType"] = sl_order_type

        # Submit the order
        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return raw response if requested
        if raw:
            return response

        # If orderLinkId was provided, return a corresponding message
        if order_link_id is not None:
            return f"orderLinkId: {response.get('result', {}).get('orderLinkId', [])}"

        # Otherwise, return the system-generated orderId
        return f"orderId: {response.get('result', {}).get('orderId', [])}"
    

    def place_futures_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        qty: str,
        price: str = None,
        category: str = "linear",
        time_in_force: str = None,
        market_unit: str = "baseCoin",
        position_idx: int = None,
        order_link_id: str = None,
        take_profit: str = None,
        stop_loss: str = None,
        tp_trigger_by: str = None,
        sl_trigger_by: str = None,
        tp_limit_price: str = None,
        sl_limit_price: str = None,
        tp_order_type: str = None,
        sl_order_type: str = None,
        tpsl_mode: str = None,
        raw: bool = False,
        **kwargs
    ) -> str:
        """
        Place a futures order (Linear or otherwise) on Bybit.

        Args:
            symbol (str): Symbol name (e.g., "BTCUSDT").
            side (str): "Buy" or "Sell".
            order_type (str): "Market" or "Limit".
            qty (str): Order quantity (as a string; Bybit expects string inputs).
            price (str, optional): Limit price for a limit order. Defaults to None.
            category (str, optional): Product category, "linear" by default.
            time_in_force (str, optional): One of "GTC", "IOC", "FOK", "PostOnly".
                If None, defaults to "IOC" for market orders, "GTC" otherwise.
            market_unit (str, optional): Either "baseCoin" or "quoteCoin" to denote
                how quantity is specified. Defaults to "baseCoin".
            position_idx (int, optional): Position index if in hedge mode 
                (1 for one-way, 2/3 for hedge side). Defaults to None.
            order_link_id (str, optional): User-defined unique identifier for the order
                (max length 36 characters). Defaults to None.
            take_profit (str, optional): Take profit price if desired. Defaults to None.
            stop_loss (str, optional): Stop loss price if desired. Defaults to None.
            tp_trigger_by (str, optional): Trigger price mechanism for TP ("LastPrice", "MarkPrice", etc.).
            sl_trigger_by (str, optional): Trigger price mechanism for SL ("LastPrice", "MarkPrice", etc.).
            tp_limit_price (str, optional): If `tp_order_type="Limit"`, specify this limit price. 
            sl_limit_price (str, optional): If `sl_order_type="Limit"`, specify this limit price.
            tp_order_type (str, optional): "Market" or "Limit" for the take profit order.
            sl_order_type (str, optional): "Market" or "Limit" for the stop loss order.
            tpsl_mode (str, optional): "Full" or "Partial" to describe the position-close mode.
            raw (bool, optional): If True, returns the raw response (dict). Otherwise, returns 
                a string indicating orderId or orderLinkId.
            **kwargs: Any additional parameters supported by Bybit's API.

        Returns:
            str | dict:
                - If `raw=True`, returns the raw API response (dict).
                - Otherwise, a string either:
                  "orderLinkId: <...>" (if `order_link_id` is provided) or
                  "orderId: <...>" (Bybit's system-generated order ID).

        Notes:
              https://bybit-exchange.github.io/docs/v5/order/create-order
        """

        # Set a default time_in_force if not provided
        if time_in_force is None:
            if order_type.lower() == 'market':
                time_in_force = 'IOC'
            else:
                time_in_force = 'GTC'

        # Build the request parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["side"] = side
        kwargs["orderType"] = order_type
        kwargs["qty"] = qty
        kwargs["price"] = price
        kwargs["timeInForce"] = time_in_force
        kwargs["marketUnit"] = market_unit
        kwargs["positionIdx"] = position_idx
        kwargs["orderLinkId"] = order_link_id
        kwargs["takeProfit"] = take_profit
        kwargs["stopLoss"] = stop_loss
        kwargs["tpTriggerBy"] = tp_trigger_by
        kwargs["slTriggerBy"] = sl_trigger_by
        kwargs["tpLimitPrice"] = tp_limit_price
        kwargs["slLimitPrice"] = sl_limit_price
        kwargs["tpOrderType"] = tp_order_type
        kwargs["slOrderType"] = sl_order_type
        kwargs["tpslMode"] = tpsl_mode

        # Send the request
        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return the raw response if requested
        if raw:
            return response

        # If an orderLinkId was provided, return that
        if order_link_id is not None:
            return f"orderLinkId: {response.get('result', {}).get('orderLinkId', [])}"

        # Otherwise, return the system-generated orderId
        return f"orderId: {response.get('result', {}).get('orderId', [])}"
    

    def place_conditional_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        qty: str,
        price: str = None,
        category: str = "linear",
        time_in_force: str = None,
        market_unit: str = "baseCoin",
        trigger_price: str = None,
        trigger_by: str = None,
        trigger_direction: int = None,
        position_idx: int = None,
        order_link_id: str = None,
        take_profit: str = None,
        stop_loss: str = None,
        tp_trigger_by: str = None,
        sl_trigger_by: str = None,
        tp_limit_price: str = None,
        sl_limit_price: str = None,
        tp_order_type: str = None,
        sl_order_type: str = None,
        tpsl_mode: str = None,
        raw: bool = False,
        **kwargs
    ) -> str:
        """
        Place a conditional (stop) order on Bybit (only for `category="linear"`).

        Args:
            symbol (str): Symbol name, e.g., "BTCUSDT".
            side (str): "Buy" or "Sell".
            order_type (str): "Market" or "Limit".
            qty (str): Order quantity (as a string; Bybit expects string inputs).
            price (str, optional): Price for limit orders. Defaults to None.
            category (str, optional): Product category. Defaults to "linear".
            time_in_force (str, optional): One of "GTC", "IOC", "FOK", "PostOnly".
                Defaults to "IOC" for `order_type="Market"`, otherwise "GTC".
            market_unit (str, optional): Either "baseCoin" or "quoteCoin" 
                to denote how quantity is specified. Defaults to "baseCoin".
            trigger_price (str): Price at which the conditional order is triggered.
            trigger_by (str): Mechanism to determine the trigger price (e.g., "MarkPrice", "LastPrice").
            trigger_direction (int): Used to identify the expected direction of the conditional order.
                1: triggered when market price rises to triggerPrice
                2: triggered when market price falls to triggerPrice
            position_idx (int, optional): Position index if in hedge mode (1 for one-way, 2/3 for hedge side).
            order_link_id (str, optional): User-defined unique identifier for the order 
                (max length 36 characters).
            take_profit (str, optional): TP price if desired (set `tpsl_mode` accordingly).
            stop_loss (str, optional): SL price if desired (set `tpsl_mode` accordingly).
            tp_trigger_by (str, optional): Which price to follow for triggering TP ("LastPrice", "MarkPrice").
            sl_trigger_by (str, optional): Which price to follow for triggering SL ("LastPrice", "MarkPrice").
            tp_limit_price (str, optional): Limit price for TP if `tp_order_type="Limit"`.
            sl_limit_price (str, optional): Limit price for SL if `sl_order_type="Limit"`.
            tp_order_type (str, optional): "Market" or "Limit" for the TP order.
            sl_order_type (str, optional): "Market" or "Limit" for the SL order.
            tpsl_mode (str, optional): "Full" or "Partial". "Full" typically for a market-based TP/SL.
            raw (bool, optional): If True, returns the raw API response (dict). Otherwise, a string 
                indicating order ID or link ID. Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API.

        Returns:
            str | dict:
                - If `raw=True`, returns the raw API response (dict).
                - Otherwise, returns either:
                  "orderLinkId: <...>" if `order_link_id` is provided,
                  or "orderId: <...>" if the system-generated order ID is used.

        Notes:
            - Conditional orders do not occupy margin until triggered.
              https://bybit-exchange.github.io/docs/v5/order/create-order
        """

        # Determine a default time_in_force if not provided
        if time_in_force is None:
            if order_type.lower() == 'market':
                time_in_force = 'IOC'
            else:
                time_in_force = 'GTC'

        # Build the request parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["side"] = side
        kwargs["orderType"] = order_type
        kwargs["qty"] = qty
        kwargs["price"] = price
        kwargs["timeInForce"] = time_in_force
        kwargs["marketUnit"] = market_unit
        kwargs["triggerPrice"] = trigger_price
        kwargs["triggerBy"] = trigger_by
        kwargs["triggerDirection"] = trigger_direction
        kwargs["positionIdx"] = position_idx
        kwargs["orderLinkId"] = order_link_id
        kwargs["takeProfit"] = take_profit
        kwargs["stopLoss"] = stop_loss
        kwargs["tpTriggerBy"] = tp_trigger_by
        kwargs["slTriggerBy"] = sl_trigger_by
        kwargs["tpLimitPrice"] = tp_limit_price
        kwargs["slLimitPrice"] = sl_limit_price
        kwargs["tpOrderType"] = tp_order_type
        kwargs["slOrderType"] = sl_order_type
        kwargs["tpslMode"] = tpsl_mode

        # Send the request
        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return the raw response if requested
        if raw:
            return response

        # If an orderLinkId was provided, return that
        if order_link_id is not None:
            return f"orderLinkId: {response.get('result', {}).get('orderLinkId', [])}"

        # Otherwise, return the system-generated orderId
        return f"orderId: {response.get('result', {}).get('orderId', [])}"
    

    def close_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        qty: str,
        price: str = None,
        category: str = "linear",
        time_in_force: str = None,
        market_unit: str = "baseCoin",
        order_link_id: str = None,
        reduce_only: bool = True,
        raw: bool = False,
        **kwargs
    ) -> str:
        """
        Close an open futures position on Bybit (only for `category="linear"`).

        Args:
            symbol (str): Symbol name (e.g., "BTCUSDT").
            side (str): "Buy" or "Sell".
            order_type (str): "Market" or "Limit".
            qty (str): Quantity of the position to close, as a string.
            price (str, optional): Limit price if `order_type="Limit"`. 
                Defaults to None (not needed for market orders).
            category (str, optional): Product category, defaults to "linear".
            time_in_force (str, optional): One of "GTC", "IOC", "FOK", or "PostOnly".
                If None, defaults to "IOC" if `order_type="market"`, else "GTC".
            market_unit (str, optional): "baseCoin" or "quoteCoin". Defaults to "baseCoin".
            order_link_id (str, optional): User-defined custom order ID. Defaults to None.
            reduce_only (bool, optional): Whether the order should only reduce a position. 
                Defaults to True.
            raw (bool, optional): If True, returns the full Bybit response (dict). 
                Otherwise, returns a string with the order ID or link ID. Defaults to False.
            **kwargs: Additional query parameters recognized by Bybit's API.

        Returns:
            str | dict:
                - If `raw=True`, returns the raw API response (dict).
                - Otherwise, returns a string:
                  - "orderLinkId: <...>" if `order_link_id` is provided, or
                  - "orderId: <...>" if using the system-generated order ID.

        Notes:
              https://bybit-exchange.github.io/docs/v5/order/create-order
        """

        # Decide on time_in_force if not provided
        if time_in_force is None:
            if order_type.lower() == 'market':
                time_in_force = 'IOC'
            else:
                time_in_force = 'GTC'

        # Build the request parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["side"] = side
        kwargs["orderType"] = order_type
        kwargs["qty"] = qty
        kwargs["price"] = price
        kwargs["timeInForce"] = time_in_force
        kwargs["marketUnit"] = market_unit
        kwargs["orderLinkId"] = order_link_id
        kwargs["reduceOnly"] = reduce_only

        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

        if raw:
            return response

        if order_link_id is not None:
            return f"orderLinkId: {response.get('result', {}).get('orderLinkId', [])}"

        return f"orderId: {response.get('result', {}).get('orderId', [])}"
    

    def amend_order(
        self,
        category: str,
        symbol: str,
        qty: str = None,
        price: str = None,
        trigger_price: str = None,
        trigger_by: str = None,
        order_link_id: str = None,
        order_id: str = None,
        take_profit: str = None,
        stop_loss: str = None,
        tp_trigger_by: str = None,
        sl_trigger_by: str = None,
        tp_limit_price: str = None,
        sl_limit_price: str = None,
        tpsl_mode: str = None,
        raw: bool = False,
        **kwargs
    ) -> str | dict:
        """
        Amend or modify an existing active or conditional order on Bybit.

        This endpoint supports:
          - Unified accounts: spot, linear, option
          - Normal accounts: linear, inverse

        Either `order_id` or `order_link_id` must be provided to identify the order.

        Args:
            category (str): Product type, such as "spot", "linear", "inverse", or "option".
            symbol (str): Symbol name, e.g., "BTCUSDT".
            qty (str, optional): New quantity to update (in string format for Bybit).
            price (str, optional): New price if adjusting a limit order. Defaults to None.
            trigger_price (str, optional): New trigger price if this is a conditional order. Defaults to None.
            trigger_by (str, optional): Mechanism for triggering (e.g., "LastPrice", "MarkPrice"). Defaults to None.
            order_link_id (str, optional): User-defined ID if the order was placed via a custom ID. Defaults to None.
            order_id (str, optional): Bybit system-generated order ID to amend. Defaults to None.
            take_profit (str, optional): Updated take profit price. Defaults to None.
            stop_loss (str, optional): Updated stop loss price. Defaults to None.
            tp_trigger_by (str, optional): Trigger mechanism for take profit. Defaults to None.
            sl_trigger_by (str, optional): Trigger mechanism for stop loss. Defaults to None.
            tp_limit_price (str, optional): Limit price for TP if `tp_order_type="Limit"`. Defaults to None.
            sl_limit_price (str, optional): Limit price for SL if `sl_order_type="Limit"`. Defaults to None.
            tpsl_mode (str, optional): "Full" or "Partial" to describe position-close mode. Defaults to None.
            raw (bool, optional): If True, returns the raw API response (dict). Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API.

        Returns:
            str | dict:
                - If `raw=True`, returns the raw API response (dict).
                - Otherwise, returns a string:
                  - "orderLinkId: <...>" if `order_link_id` was used,
                  - "orderId: <...>" otherwise.

        Note:
            - For more details, see:
              https://bybit-exchange.github.io/docs/v5/order/amend-order
        """

        # Build the request parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["qty"] = qty
        kwargs["price"] = price
        kwargs["triggerPrice"] = trigger_price
        kwargs["triggerBy"] = trigger_by
        kwargs["orderLinkId"] = order_link_id
        kwargs["orderId"] = order_id
        kwargs["takeProfit"] = take_profit
        kwargs["stopLoss"] = stop_loss
        kwargs["tpTriggerBy"] = tp_trigger_by
        kwargs["slTriggerBy"] = sl_trigger_by
        kwargs["tpLimitPrice"] = tp_limit_price
        kwargs["slLimitPrice"] = sl_limit_price
        kwargs["tpslMode"] = tpsl_mode

        # Send the request
        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return raw response if requested
        if raw:
            return response

        # If order_link_id was provided, return that
        if order_link_id is not None:
            updated_link_id = response.get('result', {}).get('orderLinkId', [])
            return f"orderLinkId: {updated_link_id}"

        # Otherwise, return the system-generated order ID
        updated_order_id = response.get('result', {}).get('orderId', [])
        return f"orderId: {updated_order_id}"
    

    def cancel_order(
        self,
        category: str,
        symbol: str,
        order_id: str = None,
        order_link_id: str = None,
        raw: bool = False,
        **kwargs
    ) -> str:
        """
        Cancel an active (or conditional) order on Bybit.

        This method supports:
            - Unified accounts (spot, linear, option)
            - Normal accounts (linear, inverse)
        
        Either `order_id` or `order_link_id` must be provided.

        Args:
            category (str): Product type (e.g., "spot", "linear", "inverse", "option").
                - Unified account: "spot", "linear", "option"
                - Normal account: "linear", "inverse"
            symbol (str): Symbol name (e.g., "BTCUSDT").
            order_id (str, optional): Bybit system-generated order ID. 
                Provide if you don't have `order_link_id`. Defaults to None.
            order_link_id (str, optional): User-defined order ID. 
                Provide if you don't have `order_id`. Defaults to None.
            raw (bool, optional): If True, returns the raw response (dict). Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API.

        Returns:
            str | dict:
                - If `raw=True`, returns the entire Bybit response (dict).
                - Otherwise, returns a string that includes either
                  "orderLinkId: <...>    CANCELLED" or 
                  "orderId: <...>    CANCELLED", depending on which
                  identifier was used.

        Raises:
            InvalidRequestError: If neither `order_id` nor `order_link_id` is provided.

        Note:
            For more details, see:
            https://bybit-exchange.github.io/docs/v5/order/cancel-order
        """

        # Build the request parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["orderId"] = order_id
        kwargs["orderLinkId"] = order_link_id

        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.CANCEL_ORDER}",
            query=kwargs,
            auth=True,
        )

        # If raw response is requested, return the full dictionary
        if raw:
            return response

        # If an order_link_id was provided, return a "CANCELLED" message with it
        if order_link_id is not None:
            cancelled_link_id = response.get("result", {}).get("orderLinkId", [])
            return f"orderLinkId: {cancelled_link_id}    CANCELLED"

        # Otherwise, return a "CANCELLED" message with the system-generated order ID
        cancelled_order_id = response.get("result", {}).get("orderId", [])
        return f"orderId: {cancelled_order_id}    CANCELLED"

    
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
        
        Note:
            https://bybit-exchange.github.io/docs/v5/order/open-order
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
            data_list = self._http_manager._submit_paginated_request(
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
                try:
                    filtered['createdTime'] = pd.to_datetime(
                        int(filtered['createdTime']), unit='ms'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    filtered['createdTime'] = '-'

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


    def cancel_all_orders(
        self,
        category: str,
        symbol: str = None,
        base_coin: str = None,
        settle_coin: str = None,
        raw: bool = False,
        **kwargs
    ) -> list | dict:
        """
        Cancel all open orders for a specified category and symbol on Bybit.

        This method supports:
            - Unified accounts: spot, linear, option
            - Normal accounts: linear, inverse

        Notes:
            - If cancelling all by `base_coin`/`settle_coin`, it will cancel all linear and inverse orders.
            - The `symbol` parameter is typically required unless you are cancelling by `base_coin`/`settle_coin`.
            - If `raw=True`, the raw JSON response is returned directly.

        Args:
            category (str): Product type ("spot", "linear", "inverse", "option").
                Note that category does not affect business logic directly, 
                but is required by the Bybit API.
            symbol (str): Symbol name, e.g. "BTCUSDT".
            base_coin (str, optional): Base coin (e.g. "BTC" for linear or inverse).
            settle_coin (str, optional): Settlement coin (e.g. "USDT" for linear).
            raw (bool, optional): If True, returns the raw response (dict).
                Otherwise, returns a list of order IDs that were cancelled.
                Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API.

        Returns:
            list | dict:
                - If `raw=True`, returns a dictionary containing the full Bybit response.
                - Otherwise, returns a list of string order IDs that were cancelled.

        Notes:
            https://bybit-exchange.github.io/docs/v5/order/cancel-all
        """

        # Prepare query parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["baseCoin"] = base_coin
        kwargs["settleCoin"] = settle_coin

        # Submit the cancellation request
        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.CANCEL_ALL_ORDERS}",
            query=kwargs,
            auth=True,
        )

        # If raw output is requested, return the entire response
        if raw:
            return response
        
        # Otherwise, parse the cancelled orders list
        cancelled_list = response.get("result", {}).get("list", [])
        return [item.get('orderId') for item in cancelled_list]


    def get_order_history(
        self,
        category: str,
        symbol: str = None,
        settle_coin: str = None,
        base_coin: str = None,
        order_id: str = None,
        order_link_id: str = None,
        order_status: str = None,
        start_time: str = None,
        end_time: str = None,
        max_pages: int = None,
        raw: bool = False,
        return_list: bool = False,
        **kwargs
    ) -> dict | list | None:
        """
        Query your order history from Bybit.

        This method can retrieve historical order data for a given product category
        (e.g. "spot", "linear", "inverse", "option"). As order creation/cancellation is
        asynchronous, there might be a slight delay in the data returned from this endpoint.

        Args:
            category (str):
                - For Unified accounts: "spot", "linear", "option"
                - For Normal accounts: "linear", "inverse"
            symbol (str, optional): Symbol name (e.g., "BTCUSDT"). Defaults to None.
            settle_coin (str, optional): Settlement coin (e.g., "USDT"). Defaults to None.
            base_coin (str, optional): Base coin (e.g., "BTC"). Defaults to None.
            order_id (str, optional): Specific order ID to filter results. Defaults to None.
            order_link_id (str, optional): Custom client-defined order ID to filter. Defaults to None.
            order_status (str, optional): Filter results by order status (e.g., "Filled", "Cancelled"). Defaults to None.
            start_time (str, optional): Date (%Y-%m-%d %H:%M:%S). Will be converted internally to ms.
                Defaults to None.
            end_time (str, optional): Date (%Y-%m-%d %H:%M:%S). . Will be converted internally to ms.
                Defaults to None.
            max_pages (int, optional): If set, fetch multiple pages up to this limit. Defaults to None.
            raw (bool, optional): 
                - If True and `max_pages` is None, returns the raw dict response.
                - If True and `max_pages` is set, returns a combined list of raw data from multiple pages.
                Defaults to False.
            return_list (bool, optional):
                - If True (and data is not raw), returns a list of processed records.
                - Otherwise, displays a styled HTML DataFrame and returns None.
                Defaults to False.
            **kwargs: Additional query parameters (e.g., `limit`, etc.) recognized by Bybit.

        Returns:
            dict | list | None:
                - If `max_pages` is None and `raw=True`, returns a raw dict response from Bybit.
                - If `max_pages` is set and `raw=True`, returns a combined list of raw records.
                - If neither `raw` nor `max_pages` are set, but data is present:
                  displays a styled HTML DataFrame of the order history and returns None.
                - If `return_list` is True, returns a list of processed dictionary records.
                - Returns an empty dict if there is no data and `raw=False`.

        Notes:
            https://bybit-exchange.github.io/docs/v5/order/order-list
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
            Format numeric values to replace commas with spaces, e.g., 1,234.56 -> 1 234.56.
            Only applies if `value` is numeric.
            """
            try:
                num = float(value)
                # If the number is an integer, display as integer (e.g., 100.0 -> 100)
                if num.is_integer():
                    num = int(num)
                # Insert thousands separators (spaces) for large numbers
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
                        styles.append('background-color: lightgreen; color: black; font-weight: bold;')
                    elif red in col_name:
                        styles.append('background-color: salmon; color: black; font-weight: bold;')
                    elif lime in col_name:
                        styles.append('background-color: black; color: lime')
                    else:
                        styles.append('background-color: black')
                return styles

            styled = df.style.apply(style_specific_cell, axis=1)
            # Right-align columns
            styled = styled.set_properties(**{'text-align': 'right'})
            # Add a border and adjust table style
            styled = styled.set_table_attributes('style="font-size: 12px; border: 2px solid black;"')
            # Numeric formatting
            styled = styled.format(format_with_spaces)

            # Header styles
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

        # Convert start_time / end_time if provided
        if start_time is not None:
            start_timestamp = pd.to_datetime(start_time)
            start_time = int(start_timestamp.timestamp() * 1000)

        if end_time is not None:
            end_timestamp = pd.to_datetime(end_time)
            end_time = int(end_timestamp.timestamp() * 1000)

        # Build request parameters
        path = f"{self.endpoint}{Trade.GET_ORDER_HISTORY}"
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["settleCoin"] = settle_coin
        kwargs["baseCoin"] = base_coin
        kwargs["orderId"] = order_id
        kwargs["orderLinkId"] = order_link_id
        kwargs["orderStatus"] = order_status
        kwargs["startTime"] = start_time
        kwargs["endTime"] = end_time

        # If max_pages is set, use the paginated endpoint
        if max_pages is not None:
            data_list = self._http_manager._submit_paginated_request(
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

            # Return raw if needed
            if raw:
                return response

            data_list = response.get('result', {}).get('list', [])
            if not data_list:
                # Return empty dict if no data
                return {}

        # If raw is requested (and multiple pages potentially fetched), return the raw data_list
        if raw:
            return data_list

        # Filter and transform each item in data_list
        keys_to_keep = [
            'symbol', 'orderType', 'timeInForce', 'orderStatus', 'side', 'isLeverage',
            'price', 'avgPrice', 'qty', 'cumExecQty', 'leavesQty', 'cumExecFee',
            'takeProfit', 'stopLoss', 'tpLimitPrice', 'slLimitPrice',
            'triggerPrice', 'triggerBy', 'triggerDirection',
            'orderLinkId', 'orderId', 'createdTime'
        ]

        for idx, item in enumerate(data_list):
            filtered = {k: item[k] for k in keys_to_keep if k in item}

            # Convert createdTime to readable format
            if 'createdTime' in filtered:
                try:
                    filtered['createdTime'] = pd.to_datetime(
                        int(filtered['createdTime']), unit='ms'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    filtered['createdTime'] = '-'

            # Combine orderStatus, orderType, timeInForce into a single field
            if (
                'orderStatus' in filtered and
                'orderType' in filtered and
                'timeInForce' in filtered
            ):
                filtered['orderType'] = f"{filtered['orderStatus']} ({filtered['orderType']}, {filtered['timeInForce']})"
            filtered.pop('timeInForce', None)

            # Replace numeric zeros with '-'
            if not is_not_zero(filtered.get('price', 0)):
                filtered['price'] = '-'
            if not is_not_zero(filtered.get('isLeverage', 0)):
                filtered['isLeverage'] = '-'
            if not is_not_zero(filtered.get('cumExecQty', 0)):
                filtered['cumExecQty'] = '-'
            if not is_not_zero(filtered.get('avgPrice', 0)):
                filtered['avgPrice'] = '-'
            if not is_not_zero(filtered.get('cumExecFee', 0)):
                filtered['cumExecFee'] = '-'
            if not is_not_zero(filtered.get('leavesQty', 0)):
                filtered['leavesQty'] = '-'

            # Take-profit logic
            tp_price = filtered.get('takeProfit', 0)
            tp_limit = filtered.get('tpLimitPrice', 0)
            if is_not_zero(tp_price) or is_not_zero(tp_limit):
                filtered['takeProfit'] = (
                    f"{'limit' if is_not_zero(tp_limit) else 'market'}:\n \
                    {format_with_spaces(tp_price) if is_not_zero(tp_price) else format_with_spaces(tp_limit)}"
                )
            else:
                filtered['takeProfit'] = '-'
            filtered.pop('tpLimitPrice', None)

            # Stop-loss logic
            sl_price = filtered.get('stopLoss', 0)
            sl_limit = filtered.get('slLimitPrice', 0)
            if is_not_zero(sl_price) or is_not_zero(sl_limit):
                filtered['stopLoss'] = (
                    f"{'limit' if is_not_zero(sl_limit) else 'market'}:\n \
                    {format_with_spaces(sl_price) if is_not_zero(sl_price) else format_with_spaces(sl_limit)}"
                )
            else:
                filtered['stopLoss'] = '-'
            filtered.pop('slLimitPrice', None)

            # Trigger price logic
            trig_price = filtered.get('triggerPrice', 0)
            if is_not_zero(trig_price):
                arrow = '↑' if filtered.get('triggerDirection') == '1' else '↓'
                trig_by = filtered.get('triggerBy', '-')
                status = filtered.get('orderStatus', '-')
                trig_formatted = format_with_spaces(trig_price)
                filtered['triggerPrice'] = f"{arrow} {status} ({trig_by}):\n{trig_formatted}"
            else:
                filtered['triggerPrice'] = '-'

            filtered.pop('triggerDirection', None)
            filtered.pop('orderStatus', None)
            filtered.pop('triggerBy', None)

            if 'orderLinkId' in filtered:
                filtered['orderLinkId'] = f"link:\n{filtered['orderLinkId']}"
            if 'orderId' in filtered:
                filtered['orderId'] = f"id:\n{filtered['orderId']}"
            if category == "linear":
                filtered.pop('isLeverage', None)

            data_list[idx] = filtered

        # Decide on return format
        if return_list:
            return data_list

        df = pd.DataFrame(data_list)

        # Rename columns for clarity
        if 'leavesQty' in df.columns:
            df.rename(
                columns={
                    'orderType': 'order',
                    'avgPrice': 'avgExecPrice'
                },
                inplace=True
            )

        styled_df = format_dashboard(df).set_caption("Order History")
        html = styled_df._repr_html_()
        display_html(html, raw=True)

        return None


    def place_batch_order(
        self,
        category: str,
        orders: list[dict],
        raw: bool = False,
        **kwargs
    ) -> list | dict:
        """
        Place multiple orders in a single request.

        This endpoint supports creating several orders at once for a given product category.

        Args:
            category (str): Product type (e.g., "linear", "inverse", "spot", "option").
            orders (list[dict]): A list of dictionaries where each dictionary represents one order.
                Required fields per order dictionary:
                  - symbol (str): Symbol name (e.g., "BTCUSDT").
                  - side (str): "Buy" or "Sell".
                  - orderType (str): "Limit" or "Market".
                  - qty (str): Order quantity.
                Optional fields:
                  - price (str): Required if `orderType="Limit"`.
                  - timeInForce (str): One of "GTC", "IOC", "FOK", or "PostOnly".
                  - reduceOnly (bool): Whether the order is reduce-only.
                  - closeOnTrigger (bool): Whether to close the position on trigger.
                  - orderLinkId (str): Custom client-defined order ID.
            raw (bool, optional): If True, returns the raw Bybit API response (dict).
                Otherwise, returns a list of order IDs or link IDs. Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API.

        Returns:
            list | dict:
                - If `raw=True`, returns the raw API response (dict).
                - Otherwise, returns a list of either `orderLinkId` or `orderId`
                  for each successfully placed order.

        Notes:
            https://bybit-exchange.github.io/docs/v5/order/batch-place
        """

        kwargs["category"] = category
        kwargs["request"] = orders

        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_PLACE_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return raw response if requested
        if raw:
            return response

        # Extract the list of orders from the response
        order_list = response.get('result', {}).get('list', [])
        success_list = []
        for order in order_list:
            # Check if a custom link ID (orderLinkId) was provided; otherwise, use the orderId
            link_id = order.get('orderLinkId', '') or order.get('orderId', '')
            success_list.append(link_id)

        return success_list
    

    def amend_batch_order(
        self,
        category: str,
        orders: list[dict],
        raw: bool = False,
        **kwargs
    ) -> list | dict:
        """
        Batch amend (modify) multiple existing orders in a single request.

        This endpoint currently covers:
            - Options (Unified Accounts)

        Args:
            category (str): Product type, e.g., "option".
            orders (list[dict]): A list of dictionaries, where each dictionary defines
                the parameters for one existing order to amend.  
                Required fields for each order include:
                  - "symbol" (str): Symbol name (e.g., "BTCUSDT").
                  - "orderId" (str) or "orderLinkId" (str): 
                    Either the system-generated orderId or the custom-defined orderLinkId. 
                    At least one is required to identify the order.
                Optional fields can include other amendable parameters (e.g., "price", "qty", etc.).
            raw (bool, optional): If True, returns the raw Bybit API response (dict). 
                Otherwise, returns a list of IDs (either orderLinkId or orderId). Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API.

        Returns:
            list | dict:
                - If `raw=True`, returns the raw API response (dict).
                - Otherwise, returns a list of identifiers (orderLinkId if present, 
                  otherwise orderId) for each amended order.

        Nores:
            https://bybit-exchange.github.io/docs/v5/order/batch-amend
        """

        kwargs["category"] = category
        kwargs["request"] = orders

        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return raw response if requested
        if raw:
            return response

        # Extract the list of orders from the response
        order_list = response.get("result", {}).get("list", [])
        success_list = []
        for order in order_list:
            # Check if a custom link ID (orderLinkId) was provided; otherwise, use orderId
            link_id = order.get("orderLinkId", "") or order.get("orderId", "")
            success_list.append(link_id)

        return success_list


    def cancel_batch_order(
            self,
            category: str,
            orders: list[dict],
            raw: bool = False,
            **kwargs
    ) -> list | dict:

        """This endpoint allows you to cancel more than one open order in a single request.

        Required args:
            category (string): Product type. option
            request (array): Object
            > symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/order/batch-cancel
        """

        kwargs["category"] = category
        kwargs["request"] = orders

        response = self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Trade.BATCH_AMEND_ORDER}",
            query=kwargs,
            auth=True,
        )

        # Return raw response if requested
        if raw:
            return response

        # Extract the list of orders from the response
        order_list = response.get("result", {}).get("list", [])
        success_list = []
        for order in order_list:
            # Check if a custom link ID (orderLinkId) was provided; otherwise, use orderId
            link_id = order.get("orderLinkId", "") or order.get("orderId", "")
            success_list.append(link_id)

        return success_list


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


    def get_positions(
        self,
        category,
        symbol=None,
        settle_coin=None,
        base_coin=None,
        max_pages=None,
        raw=False,
        return_list=False,
        **kwargs
    ):
        """
        Query real-time position data (e.g., position size, cumulative realized PNL).

        Args:
            category (str): 
                - Unified account: "linear", "option"
                - Normal account: "linear", "inverse"
            symbol (str, optional): Symbol name, e.g., "BTCUSDT" (uppercase).
            settle_coin (str, optional): Settlement coin, e.g., "USDT" or "BTC".
            base_coin (str, optional): Base coin, e.g., "BTC".
            max_pages (int, optional): If set, fetch multiple pages up to this limit.
            raw (bool, optional): If True, return the raw API response.
            return_list (bool, optional): If True, return a combined list from all pages.
            **kwargs: Additional query parameters (e.g. `limit`, `symbol`, `baseCoin`).

        Returns:
            dict | list | None:
                - If `max_pages` is None and `raw=True`, returns the raw response dict.
                - If `max_pages` is set and `raw=True`, returns a combined list (raw data).
                - If `max_pages` is None and `raw=False`, returns a dict if empty, or displays
                  a styled HTML DataFrame of positions if not empty.
                - If `return_list` is True, returns the combined list of positions (rather than a DataFrame).
                - Otherwise, displays the styled HTML DataFrame in a Jupyter environment and returns None.

        Note:
            For more information, see:
            https://bybit-exchange.github.io/docs/v5/position
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
            Format numeric values to replace commas with spaces, e.g., 1,234.56 -> 1 234.56.
            Only applies if `value` is numeric.
            """
            try:
                num = float(value)
                # If the number is an integer, display it as integer (e.g., 100.0 -> 100).
                if num.is_integer():
                    num = int(num)

                # Insert thousands separators (replacing commas with spaces) if num is large.
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

            # Right-align all columns
            styled = styled.set_properties(**{'text-align': 'right'})

            # Add a border and control table sizing
            styled = styled.set_table_attributes(
                'style="font-size: 12px; border: 2px solid black;"'
            )

            # Apply numeric formatting
            styled = styled.format(format_with_spaces)

            # Apply custom header styles
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
        path = f"{self.endpoint}{Trade.GET_POSITIONS}"
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["settleCoin"] = settle_coin
        kwargs["baseCoin"] = base_coin

        # If max_pages is set, use the paginated endpoint
        if max_pages is not None:
            data_list = self._http_manager._submit_paginated_request(
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

            # If raw is requested, return the entire response as-is
            if raw:
                return response

            data_list = response.get('result', {}).get('list', [])
            if not data_list:
                # If the list is empty, return an empty dictionary
                return {}

        # If raw was requested (and multiple pages were fetched), return the raw data_list
        if raw:
            return data_list

        # Filter and transform each item in data_list
        keys_to_keep = [
            'symbol', 'side', 'avgPrice', 'size', 'leverage', 'tradeMode',
            'liqPrice', 'unrealisedPnl', 'curRealisedPnl',
            'takeProfit', 'stopLoss', 'positionIM',
            'positionBalance', 'positionMM', 'createdTime'
        ]

        for idx, item in enumerate(data_list):
            filtered = {k: item[k] for k in keys_to_keep if k in item}

            # Convert timestamp to human-readable format
            if 'createdTime' in filtered:
                try:
                    filtered['createdTime'] = pd.to_datetime(
                        int(filtered['createdTime']), unit='ms'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    filtered['createdTime'] = '-'

            # Combine tradeMode and leverage
            if 'tradeMode' in filtered and 'leverage' in filtered:
                mode_str = 'isolated' if filtered['tradeMode'] else 'cross'
                filtered['leverage'] = f"{mode_str}: {filtered['leverage']}X"
            filtered.pop('tradeMode', None)

            if not is_not_zero(filtered.get('takeProfit', 0)):
                filtered['takeProfit'] = '-'
            if not is_not_zero(filtered.get('stopLoss', 0)):
                filtered['stopLoss'] = '-'

            data_list[idx] = filtered

        # Return a Python list of positions
        if return_list:
            return data_list

        # Otherwise, build a DataFrame and display it
        df = pd.DataFrame(data_list)

        # Rename 'positionBalance' to 'currentMargin'
        if 'positionBalance' in df.columns:
            df.rename(columns={'positionBalance': 'currentMargin'}, inplace=True)

        styled_df = format_dashboard(df).set_caption("Open Positions")
        html = styled_df._repr_html_()
        display_html(html, raw=True)
        return None


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


    def get_executions(self,
        category,
        symbol=None,
        base_coin=None,
        execution_type=None,
        order_id=None,
        order_link_id=None,
        max_pages=None,
        raw=False,
        return_list=False,
        **kwargs
    ):
        """
        Query the user's execution records, sorted by `execTime` in descending order.
        For Classic spot, they are sorted by `execId` in descending order.

        Args:
            category (str):
                - Unified account: "spot", "linear", "inverse", "option"
                - Normal account: "spot", "linear", "inverse"
            symbol (str, optional): Symbol name, e.g., "BTCUSDT" (uppercase).
            base_coin (str, optional): Base coin, e.g., "BTC".
            execution_type (str, optional): Filter by execution type, e.g., "Trade" or "Funding".
            order_id (str, optional): Filter by a specific order ID.
            order_link_id (str, optional): Filter by a client-provided order ID.
            max_pages (int, optional): If provided, fetch multiple pages up to this limit.
            raw (bool, optional): If True, returns the raw JSON response (for either single or multiple pages).
            return_list (bool, optional): If True, returns a combined list of execution records.
            **kwargs: Additional query parameters (e.g., symbol, startTime, endTime, limit).

        Returns:
            dict | list | None: 
                - If `raw=True` and `max_pages` is None, returns the raw dict response from Bybit.
                - If `raw=True` and `max_pages` is provided, returns a raw list of pages combined.
                - If `max_pages=None` and `raw=False`, returns a dict if no records, or displays 
                  a styled HTML DataFrame of execution records.
                - If `return_list=True` and there are multiple pages, returns a combined Python list.
                - Otherwise, displays the styled HTML DataFrame and returns None.

        Note:
            For a more thorough explanation, refer to:
            https://bybit-exchange.github.io/docs/v5/order/execution
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
            e.g., 1,234.56 -> 1 234.56.
            Only applies if `value` is numeric.
            """
            try:
                num = float(value)
                # If the number is an integer, display it as an integer (e.g., 100.0 -> 100).
                if num.is_integer():
                    num = int(num)

                # Insert thousands separators (replacing commas with spaces) if num is large.
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

            # Numeric formatting
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
        path = f"{self.endpoint}{Trade.GET_EXECUTIONS}"
        kwargs["category"] = category
        kwargs["symbol"] = symbol
        kwargs["baseCoin"] = base_coin
        kwargs["execType"] = execution_type
        kwargs["orderId"] = order_id
        kwargs["orderLinkId"] = order_link_id

        # If max_pages is set, use the paginated endpoint
        if max_pages is not None:
            data_list = self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
                max_pages=max_pages
            )
        else:
            # Else, make a single request
            response = self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
            )

            # If raw response is requested, return it directly
            if raw:
                return response

            data_list = response.get('result', {}).get('list', [])
            if not data_list:
                # If the list is empty, return an empty dictionary
                return {}

        # If raw is requested (and we had multiple pages), return the combined data_list
        if raw:
            return data_list

        # Filter and transform each item in data_list
        keys_to_keep = [
            'symbol', 'orderType', 'execType', 'side', 'execPrice', 'orderQty',
            'execQty', 'leavesQty', 'closedSize', 'execFee', 'feeCurrency',
            'orderLinkId', 'orderId', 'execTime'
        ]

        for idx, item in enumerate(data_list):
            filtered = {k: item[k] for k in keys_to_keep if k in item}

            # Convert timestamp to human-readable format if present
            if 'execTime' in filtered:
                try:
                    filtered['execTime'] = pd.to_datetime(
                        int(filtered['execTime']), unit='ms'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    filtered['execTime'] = '-'

            # Combine execType and orderType
            if 'execType' in filtered and 'orderType' in filtered:
                filtered['execType'] = f"{filtered['execType']} ({filtered['orderType']})"
            filtered.pop('orderType', None)

            # Show "-" if leavesQty or closedSize is zero
            if not is_not_zero(filtered.get('leavesQty', 0)):
                filtered['leavesQty'] = '-'
            if not is_not_zero(filtered.get('closedSize', 0)):
                filtered['closedSize'] = '-'

            # Format the execFee
            if 'execFee' in filtered and 'feeCurrency' in filtered:
                try:
                    exec_fee_val = float(filtered['execFee'])
                    filtered['execFee'] = f"{exec_fee_val:.4f} {filtered['feeCurrency']}"
                except (ValueError, TypeError):
                    filtered['execFee'] = f"0.0000 {filtered['feeCurrency']}"
            filtered.pop('feeCurrency', None)

            if 'orderLinkId' in filtered:
                filtered['orderLinkId'] = f"link:\n{filtered['orderLinkId']}"
            if 'orderId' in filtered:
                filtered['orderId'] = f"id:\n{filtered['orderId']}"

            data_list[idx] = filtered

        # Decide on return format
        if return_list:
            return data_list

        df = pd.DataFrame(data_list)

        # Rename 'leavesQty' to 'unfilledQty' for clarity
        if 'leavesQty' in df.columns:
            df.rename(columns={'leavesQty': 'unfilledQty'}, inplace=True)

        styled_df = format_dashboard(df).set_caption("Executed Orders")
        html = styled_df._repr_html_()
        display_html(html, raw=True)
        return None
    

    def get_closed_pnl(
        self,
        category: str,
        symbol: str = None,
        start_time: str = None,
        end_time: str = None,
        max_pages: int = None,
        raw: bool = False,
        return_list: bool = False,
        **kwargs
    ) -> dict | list | None:
        """
        Query a user's closed profit and loss (PnL) records, sorted by `createdTime` in descending order.

        Args:
            category (str):
                - For Unified accounts: "linear"
                - For Normal accounts: "linear", "inverse"
            symbol (str, optional): Symbol name (e.g., "BTCUSDT"). Defaults to None.
            start_time (str, optional): Date (%Y-%m-%d %H:%M:%S). Will be converted internally to ms.
                Defaults to None.
            end_time (str, optional): Date (%Y-%m-%d %H:%M:%S). . Will be converted internally to ms.
                Defaults to None.
            max_pages (int, optional): If set, will fetch multiple pages up to this limit. Defaults to None.
            raw (bool, optional): 
                - If `max_pages` is None and `raw=True`, returns the raw response dict.
                - If `max_pages` is set and `raw=True`, returns a combined list of raw records.
                Defaults to False.
            return_list (bool, optional): 
                - If True, returns a processed list of PnL records (and does not display a styled DataFrame).
                - If False, displays a styled DataFrame of the data in a Jupyter environment and returns None.
                Defaults to False.
            **kwargs: Additional query parameters recognized by Bybit (e.g., limit).

        Returns:
            dict | list | None:
                - If `max_pages` is None and `raw=True`, returns a raw dict of the API response.
                - If `max_pages` is set and `raw=True`, returns a combined list of raw records.
                - If `return_list=True`, returns a processed list of dictionaries.
                - Otherwise, displays a styled HTML DataFrame of the results and returns None.
                - Returns an empty dict if no data is found and neither `raw` nor `return_list` is requested.

        Notes:
            - For more details, see:
              https://bybit-exchange.github.io/docs/v5/position/close-pnl
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
            Format numeric values by replacing commas with spaces, e.g., 1,234.56 -> 1 234.56.
            Only applies if `value` is numeric.
            """
            try:
                num = float(value)
                # If the number is an integer, display it as an integer (e.g., 100.0 -> 100).
                if num.is_integer():
                    num = int(num)
                # For large numbers, use thousands separators (spaces).
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
                        styles.append('background-color: lightgreen; color: black; font-weight: bold;')
                    elif red in col_name:
                        styles.append('background-color: salmon; color: black; font-weight: bold;')
                    elif lime in col_name:
                        styles.append('background-color: black; color: lime')
                    else:
                        styles.append('background-color: black')
                return styles

            styled = df.style.apply(style_specific_cell, axis=1)
            # Right-align columns
            styled = styled.set_properties(**{'text-align': 'right'})
            # Add a border and adjust the table style
            styled = styled.set_table_attributes('style="font-size: 12px; border: 2px solid black;"')
            # Numeric formatting
            styled = styled.format(format_with_spaces)

            # Header styles
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

        # Convert start_time / end_time if provided
        if start_time is not None:
            start_timestamp = pd.to_datetime(start_time)
            start_time = int(start_timestamp.timestamp() * 1000)

        if end_time is not None:
            end_timestamp = pd.to_datetime(end_time)
            end_time = int(end_timestamp.timestamp() * 1000)

        # Build the request parameters
        path = f"{self.endpoint}{Trade.GET_CLOSED_PNL}"
        kwargs['category'] = category
        kwargs['symbol'] = symbol
        kwargs['startTime'] = start_time
        kwargs['endTime'] = end_time

        # If max_pages is set, use the paginated endpoint
        if max_pages is not None:
            data_list = self._http_manager._submit_paginated_request(
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
            # Return raw response if requested
            if raw:
                return response

            data_list = response.get('result', {}).get('list', [])
            if not data_list:
                # Return an empty dict if no data
                return {}

        # If raw is requested (and multiple pages were fetched), return the raw combined data
        if raw:
            return data_list

        # Filter and transform each item in data_list
        keys_to_keep = [
            'symbol', 'orderType', 'execType', 'side', 'leverage', 'orderPrice',
            'avgEntryPrice', 'avgExitPrice', 'qty', 'closedSize', 'closedPnl',
            'fillCount', 'orderId', 'createdTime'
        ]

        for idx, item in enumerate(data_list):
            filtered = {k: item[k] for k in keys_to_keep if k in item}

            # Convert createdTime to a human-readable format
            if 'createdTime' in filtered:
                try:
                    filtered['createdTime'] = pd.to_datetime(
                        int(filtered['createdTime']), unit='ms'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    filtered['createdTime'] = '-'

            # Combine execType and orderType into a single field
            if 'execType' in filtered and 'orderType' in filtered:
                filtered['orderType'] = f"{filtered['execType']} ({filtered['orderType']})"
            filtered.pop('execType', None)

            # Replace numeric zeros with '-'
            if not is_not_zero(filtered.get('orderPrice', 0)):
                filtered['orderPrice'] = '-'
            if not is_not_zero(filtered.get('leverage', 0)):
                filtered['leverage'] = '-'

            if 'orderId' in filtered:
                filtered['orderId'] = f"id:\n{filtered['orderId']}"

            data_list[idx] = filtered

        # Decide on return format
        if return_list:
            return data_list

        df = pd.DataFrame(data_list)
        styled_df = format_dashboard(df).set_caption("Closed P&L")
        html = styled_df._repr_html_()
        display_html(html, raw=True)

        return None
