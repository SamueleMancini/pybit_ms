from ._http_manager import HTTPManager
from .market import Market

class MarketHTTP:
    
    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

    def get_server_time(self) -> dict:
        """
            https://bybit-exchange.github.io/docs/v5/market/time
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_SERVER_TIME}",
        )

    def get_kline(self, **kwargs) -> dict:
        """Query the kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type: spot,linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval.

        https://bybit-exchange.github.io/docs/v5/market/kline
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_KLINE}",
            query=kwargs,
        )

    def get_mark_price_kline(self, **kwargs):
        """Query the mark price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W

        https://bybit-exchange.github.io/docs/v5/market/mark-kline
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_MARK_PRICE_KLINE}",
            query=kwargs,
        )

    def get_index_price_kline(self, **kwargs):
        """Query the index price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W

        https://bybit-exchange.github.io/docs/v5/market/index-kline
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_INDEX_PRICE_KLINE}",
            query=kwargs,
        )

    def get_premium_index_price_kline(self, **kwargs):
        """Retrieve the premium index price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear
            symbol (string): Symbol name
            interval (string): Kline interval

        https://bybit-exchange.github.io/docs/v5/market/preimum-index-kline
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_PREMIUM_INDEX_PRICE_KLINE}",
            query=kwargs,
        )

    def get_instruments_info(self, max_pages=None, **kwargs):
        """
        Query a list of instruments of online trading pair.

        Required args:
            category (string): Product type. e.g. "spot", "linear", "inverse", or "option"

        https://bybit-exchange.github.io/docs/v5/market/instrument

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (like limit, baseCoin, etc.).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A list combining items from each page if max_pages is provided.
        """
        path = f"{self.endpoint}{Market.GET_INSTRUMENTS_INFO}"

        if max_pages:
            # Multi-page fetch
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=False,
                max_pages=max_pages,
            )
        else:
            # Single-page fetch
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
            )

    def get_orderbook(self, **kwargs):
        """Query orderbook data

        Required args:
            category (string): Product type. spot, linear, inverse, option
            symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/market/orderbook
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_ORDERBOOK}",
            query=kwargs,
        )

    def get_tickers(self, **kwargs):
        """Query the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.

        Required args:
            category (string): Product type. spot,linear,inverse,option
        
        https://bybit-exchange.github.io/docs/v5/market/tickers
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_TICKERS}",
            query=kwargs,
        )

    def get_funding_rate_history(self, **kwargs):
        """
        Query historical funding rate. Each symbol has a different funding interval.
        For example, if the interval is 8 hours and the current time is UTC 12, then it returns the last funding rate, which settled at UTC 8.
        To query the funding rate interval, please refer to instruments-info.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/market/history-fund-rate
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_FUNDING_RATE_HISTORY}",
            query=kwargs,
        )

    def get_public_trade_history(self, **kwargs):
        """Query recent public trading data in Bybit.

        Required args:
            category (string): Product type. spot,linear,inverse,option
            symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/market/recent-trade
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_PUBLIC_TRADING_HISTORY}",
            query=kwargs,
        )

    def get_open_interest(self, max_pages=None, **kwargs):
        """
        Get open interest of each symbol.

        Required args:
            category (string): Product type. e.g., "linear", "inverse"
            symbol (string): Symbol name (e.g., "BTCUSDT")
            intervalTime (string): Interval. e.g., "5min", "15min", "30min", "1h", "4h", "1d"

        https://bybit-exchange.github.io/docs/v5/market/open-interest

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (e.g., limit, startTime, endTime, etc.).
        :return:
            - A single Bybit response dict if max_pages is None
            - A combined list of open-interest records (from each page) if max_pages is set
        """
        path = f"{self.endpoint}{Market.GET_OPEN_INTEREST}"

        if max_pages:
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=False,  # Typically market endpoints don't require auth
                max_pages=max_pages
            )
        else:
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
            )

    def get_historical_volatility(self, **kwargs):
        """Query option historical volatility

        Required args:
            category (string): Product type. option

        https://bybit-exchange.github.io/docs/v5/market/iv
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_HISTORICAL_VOLATILITY}",
            query=kwargs,
        )

    def get_insurance(self, **kwargs):
        """
        Query Bybit insurance pool data (BTC/USDT/USDC etc).
        The data is updated every 24 hours.

        https://bybit-exchange.github.io/docs/v5/market/insurance
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_INSURANCE}",
            query=kwargs,
        )
    
    def get_risk_limit(self, max_pages=None, **kwargs):
        """
        Query risk limit of futures.
        
        https://bybit-exchange.github.io/docs/v5/market/risk-limit

        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (e.g. category, symbol, limit).
        :return:
            - A single-page response dict if max_pages is None
            - A combined list if max_pages is specified
        """
        path = f"{self.endpoint}{Market.GET_RISK_LIMIT}"

        if max_pages:
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=False,   # Typically public market data
                max_pages=max_pages,
            )
        else:
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
            )

    def get_option_delivery_price(self, max_pages=None, **kwargs):
        """
        Get the delivery price for options.

        Required args:
            category (string): Product type. e.g., 'option'
        
        https://bybit-exchange.github.io/docs/v5/market/delivery-price

        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (e.g. symbol, limit, startTime, endTime).
        :return:
            - Single-page dict if max_pages is None
            - Combined list from all pages if max_pages is set
        """
        path = f"{self.endpoint}{Market.GET_OPTION_DELIVERY_PRICE}"

        if max_pages:
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=False,
                max_pages=max_pages,
            )
        else:
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
            )

    def get_long_short_ratio(self, max_pages=None, **kwargs):
        """
        Query long-short ratio data.

        Required args:
            category (string): Product type. e.g., 'linear' (USDT Perp), 'inverse'
            symbol (string): Symbol name

        https://bybit-exchange.github.io/docs/v5/market/long-short-ratio
        
        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (symbol, limit, intervalTime, etc.).
        :return:
            - A single response dict if max_pages=None
            - A combined list if max_pages is set
        """
        path = f"{self.endpoint}{Market.GET_LONG_SHORT_RATIO}"

        if max_pages:
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=False,  # Typically no auth for market data
                max_pages=max_pages,
            )
        else:
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
            )
