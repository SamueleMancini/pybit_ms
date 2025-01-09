from pybit_ms._http_manager import HTTPManager
from pybit_ms.data_layer.data_handler import DataHandler
from enum import Enum
import pandas as pd
import matplotlib.pyplot as plt



class Market(str, Enum):
    GET_SERVER_TIME = "/v5/market/time"
    GET_KLINE = "/v5/market/kline"
    GET_MARK_PRICE_KLINE = "/v5/market/mark-price-kline"
    GET_INDEX_PRICE_KLINE = "/v5/market/index-price-kline"
    GET_PREMIUM_INDEX_PRICE_KLINE = "/v5/market/premium-index-price-kline"
    GET_INSTRUMENTS_INFO = "/v5/market/instruments-info"
    GET_ORDERBOOK = "/v5/market/orderbook"
    GET_TICKERS = "/v5/market/tickers"
    GET_FUNDING_RATE_HISTORY = "/v5/market/funding/history"
    GET_PUBLIC_TRADING_HISTORY = "/v5/market/recent-trade"
    GET_OPEN_INTEREST = "/v5/market/open-interest"
    GET_HISTORICAL_VOLATILITY = "/v5/market/historical-volatility"
    GET_INSURANCE = "/v5/market/insurance"
    GET_RISK_LIMIT = "/v5/market/risk-limit"
    GET_OPTION_DELIVERY_PRICE = "/v5/market/delivery-price"
    GET_LONG_SHORT_RATIO = "/v5/market/account-ratio"

    

    def __str__(self) -> str:
        return self.value



class Market_client:
    
    def __init__(self, http_manager: HTTPManager, data_handler: DataHandler):
        self._http_manager = http_manager
        self._data_handler = data_handler
        self.endpoint = http_manager.endpoint

    def get_server_time(self) -> dict:
        """
            https://bybit-exchange.github.io/docs/v5/market/time
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_SERVER_TIME}",
        )
    

    def get_kline(self, category: str, coin1: str, coin2: str, interval: str, save_csv=False, csv_filename=None, show_link=False, plot=False, raw=False, price_type="close", **kwargs) -> dict:
        """Query the kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type: spot,linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval.
            
        Args:
            save_csv (bool): If True, saves the Kline data as a CSV file.
            csv_filename (str): Name of the CSV file to save data.
            show_link (bool): If True, provides a link to the Bybit Kline page.
            plot(bool): If True, plots close price and volume for available data.
            raw (bool): If True, returns the raw API response, else formatted response (list of the price_type).
            price_type (str): Type of price to return in the formatted response. open, high, low, close
            **kwargs: Additional query parameters for the API request.

        https://bybit-exchange.github.io/docs/v5/market/kline
        """

        kwargs["category"] = category
        kwargs["symbol"] = coin1 + coin2
        kwargs["interval"] = interval

        response = self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_KLINE}",
            query=kwargs,
        )

        # Extract data
        kline_data = response.get('result', {}).get('list', [])

        if save_csv:
            keys = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover']
            kline_data = [{key: a[i] for i, key in enumerate(keys)} for a in kline_data]
            csv_filename = csv_filename or f"{kwargs.get('symbol')}_kline.csv"

            csv_filename = self._data_handler.store_to_csv(kline_data, csv_filename)

            print(f"Kline data saved to {csv_filename}")



        if show_link:
            symbol = kwargs.get('symbol', '')
            interval = kwargs.get('interval', '')
            print(f"View live Kline data for {symbol}: https://www.bybit.com/trade/{category}/{coin1}/{coin2}")


        
        if plot:
            df = pd.DataFrame(kline_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            # Convert columns to float for plotting
            df[['open', 'high', 'low', 'close', 'volume', 'turnover']] = df[['open', 'high', 'low', 'close', 'volume', 'turnover']].astype(float)

            fig, ax1 = plt.subplots(2, 1, figsize=(8, 6), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

            # Plot close price
            ax1[0].plot(df.index, df['close'], label='Close Price', color='blue')
            ax1[0].set_ylabel("Price (USDT)")
            ax1[0].set_title(f"Kline Data: Close Price & Volume")
            ax1[0].legend()

            # Plot volume
            ax1[1].bar(df.index, df['volume'], color='orange', alpha=0.7, label='Volume')
            ax1[1].set_ylabel("Volume")
            ax1[1].set_xlabel("Time")
            ax1[1].legend()

            plt.tight_layout()
            plt.show()

        if raw:
            return response
        else:
            mapping = {'open': 1, 'high': 2, 'low': 3, 'close': 4}
            return [row[mapping[price_type]] for row in response['result']['list']]
        

    def get_mark_price_kline(self, category: str, coin1: str, coin2: str, interval: str, save_csv=False, csv_filename=None, plot=False, raw=False, price_type="close",  **kwargs):
        """Query the mark price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W

        Args:
            save_csv (bool): If True, saves the Kline data as a CSV file.
            csv_filename (str): Name of the CSV file to save data.
            plot(bool): If True, plots close price and volume for available data.
            raw (bool): If True, returns the raw API response, else formatted response (list of the price_type).
            price_type (str): Type of price to return in the formatted response. open, high, low, close
            **kwargs: Additional query parameters for the API request.

        https://bybit-exchange.github.io/docs/v5/market/mark-kline
        """


        kwargs["category"] = category
        kwargs["symbol"] = coin1 + coin2
        kwargs["interval"] = interval

        response = self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_MARK_PRICE_KLINE}",
            query=kwargs,
        )

        # Extract data
        kline_data = response.get('result', {}).get('list', [])

        if save_csv:
            keys = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover']
            kline_data = [{key: a[i] for i, key in enumerate(keys)} for a in kline_data]
            csv_filename = csv_filename or f"{kwargs.get('symbol')}_mark_price_kline.csv"

            csv_filename = self._data_handler.store_to_csv(kline_data, csv_filename)

            print(f"Mark price kline data saved to {csv_filename}")


        
        if plot:
            kline_data = response['result']['list']
            df = pd.DataFrame(kline_data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            # Convert columns to float for plotting
            df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)

            fig, ax = plt.subplots(figsize=(8, 6))

            # Plot close price
            ax.plot(df.index, df['close'], label='Close Price', color='blue')
            ax.set_ylabel("Price (USDT)")
            ax.set_title(f"Mark Price Kline Data: Close Price")
            ax.legend()

            plt.tight_layout()
            plt.show()

        if raw:
            return response
        else:
            mapping = {'open': 1, 'high': 2, 'low': 3, 'close': 4}
            return [row[mapping[price_type]] for row in response['result']['list']]


    def get_index_price_kline(self, category: str, coin1: str, coin2: str, interval: str, save_csv=False, csv_filename=None, plot=False, raw=False, price_type="close", **kwargs):
        """Query the index price kline data. Charts are returned in groups based on the requested interval.

        Required args:
            category (string): Product type. linear,inverse
            symbol (string): Symbol name
            interval (string): Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W

        Args:
            save_csv (bool): If True, saves the Kline data as a CSV file.
            csv_filename (str): Name of the CSV file to save data.
            plot(bool): If True, plots close price and volume for available data.
            raw (bool): If True, returns the raw API response, else formatted response (list of the price_type).
            price_type (str): Type of price to return in the formatted response. open, high, low, close
            **kwargs: Additional query parameters for the API request.

        https://bybit-exchange.github.io/docs/v5/market/index-kline
        """

        kwargs["category"] = category
        kwargs["symbol"] = coin1 + coin2
        kwargs["interval"] = interval

        response = self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_INDEX_PRICE_KLINE}",
            query=kwargs,
        )

        # Extract data
        kline_data = response.get('result', {}).get('list', [])

        if save_csv:
            keys = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover']
            kline_data = [{key: a[i] for i, key in enumerate(keys)} for a in kline_data]
            csv_filename = csv_filename or f"{kwargs.get('symbol')}_index_price_kline.csv"

            csv_filename = self._data_handler.store_to_csv(kline_data, csv_filename)

            print(f"Index price kline data saved to {csv_filename}")



        if plot:
            kline_data = response['result']['list']
            df = pd.DataFrame(kline_data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            # Convert columns to float for plotting
            df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)

            fig, ax = plt.subplots(figsize=(8, 6))

            # Plot close price
            ax.plot(df.index, df['close'], label='Close Price', color='blue')
            ax.set_ylabel("Price (USDT)")
            ax.set_title(f"Index Price Kline Data: Close Price")
            ax.legend()

            plt.tight_layout()
            plt.show()

        if raw:
            return response
        else:
            mapping = {'open': 1, 'high': 2, 'low': 3, 'close': 4}
            return [row[mapping[price_type]] for row in response['result']['list']]


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

    
    def get_orderbook(
        self,
        category: str,
        symbol: str,
        limit: int = 20,
        raw: bool = False,
        return_list: bool = False,
        **kwargs
        ) -> dict | None:
        """
        Query the current order book for a given symbol on Bybit. 

        Args:
            category (str): Product type, e.g., "spot", "linear", "inverse", or "option".
            symbol (str): Symbol name (e.g., "BTCUSDT").
            limit (int, optional): Number of price levels to retrieve. Defaults to 20.
                - spot: [1, 200].
                - linear&inverse: [1, 500].
                - option: [1, 25].
            raw (bool, optional): If True, returns the raw API response (dict). Defaults to False.
            return_list (bool, optional): If True (and `raw=False`), returns a dict containing
                lists of bids and asks. Defaults to False.
            **kwargs: Additional parameters recognized by Bybit's API.

        Returns:
            dict | None:
                - If `raw=True`, returns the raw API response (dict).
                - If `raw=False` and `return_list=True`, returns a dict with "bids" and "asks" keys.
                - Otherwise, displays a styled HTML DataFrame and returns None.

        Notes:
            - For more details, see Bybit's documentation:
              https://bybit-exchange.github.io/docs/v5/market/orderbook
        """ 

        # Build and Send the Request
        
        path = f"{self.endpoint}{Market.GET_ORDERBOOK}"
        kwargs['category'] = category
        kwargs['symbol'] = symbol
        kwargs['limit'] = limit

        response = self._http_manager._submit_request(
            method="GET",
            path=path,
            query=kwargs,
        )

        # If raw output is requested, return the entire response
        if raw:
            return response

        data_list = response.get('result', {})
        if not data_list:
            # If there's no data, return an empty dict
            return {}

        if return_list:
            # Return just the bids and asks as lists
            return {
                "bids": [data_list.get("b", [])],
                "asks": [data_list.get("a", [])]
            }

        # 4Format Data for Display
        asks = data_list.get("a", [])
        bids = data_list.get("b", [])

        # Determine the maximum length for alignment
        max_len = max(len(asks), len(bids))

        # Pad whichever list is shorter with '-' to align them
        asks += [['-', '-']] * (max_len - len(asks))
        bids += [['-', '-']] * (max_len - len(bids))

        df = pd.DataFrame({
            "bid_volume": [bid[1] for bid in bids],
            "bid_price": [bid[0] for bid in bids],
            "ask_price": [ask[0] for ask in asks],
            "ask_volume": [ask[1] for ask in asks],
        })

        self._data_handler.format_and_display(df, data_list.get("s", ''))
        return None

    
    def get_tickers(self, category, symbol, only_ticker=False, raw=False, return_list=False, **kwargs):
        """
        Query the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.

        Args:
            category (str): Product type. One of "spot", "linear", "inverse", "option".
            symbol (str): Symbol name (e.g., "BTCUSDT"), uppercase only.
            only_ticker (bool, optional): If True, return only the ticker price. Defaults to False.
            raw (bool, optional): If True, return the raw request response. Defaults to False.
            return_list (bool, optional): If True, returns a list of market data. Defaults to False
            **kwargs: Additional query parameters to be sent to the API.

        Returns:
            float: If only_ticker is True, returns the last price as a float.
            dict: If raw is True, returns either the full API response or the list of selected fields (as a dict).
            None: If neither only_ticker nor raw is True, displays formatted HTML output and returns None.

        Note:
            https://bybit-exchange.github.io/docs/v5/market/tickers
        """
        # Set required query parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol

        response = self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_TICKERS}",
            query=kwargs,
        )
 
        data = response.get('result', {}).get('list', [])
        if not data:
            # If the list is empty for some reason, return an empty dictionary
            return {}

        data_list = data[0]

        # If only_ticker is True, return just the float price
        if only_ticker:
            return float(data_list['lastPrice'])

        # If raw is True, return the entire response
        if raw:
            return response
        
        data_list['time'] = response.get('time', '-')

        keys_to_keep = ['lastPrice', 'bid1Price', 'bid1Size', 'ask1Price', 'ask1Size', 'highPrice24h', 'lowPrice24h', 'volume24h', 'time']
        data_list = {k: data_list[k] for k in keys_to_keep if k in data_list}

        

        self._data_handler.format_time(resp=data_list, key='time', form='%H:%M:%S')
        
        if return_list:
            return data_list

        df = pd.DataFrame([data_list])

        self._data_handler.format_and_display(df, "Market Data")
        return None


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

    
