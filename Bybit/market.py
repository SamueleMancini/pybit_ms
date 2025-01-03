from Bybit._http_manager import HTTPManager
from enum import Enum
import pandas as pd
from IPython.display import display_html


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
    
    
    def get_tickers(self, category, symbol, only_ticker=False, raw=False, **kwargs):
        """
        Query the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.

        Args:
            category (str): Product type. One of "spot", "linear", "inverse", "option".
            symbol (str): Symbol name (e.g., "BTCUSDT"), uppercase only.
            only_ticker (bool, optional): If True, return only the ticker price. Defaults to False.
            raw (bool, optional): If True, return the raw request response. Defaults to False.
            **kwargs: Additional query parameters to be sent to the API.

        Returns:
            float: If only_ticker is True, returns the last price as a float.
            dict: If raw is True, returns the full API response (as a dict).
            None: If neither only_ticker nor raw is True, displays formatted HTML output and returns None.

        Note:
            If `retCode` in the response is non-zero, returns an empty DataFrame.
            https://bybit-exchange.github.io/docs/v5/market/tickers
        """

        def format_dashboard(df):
            """
            Apply custom styling to a pandas DataFrame for display in a Jupyter environment.
            """
            def style_specific_cell(x):
                styles = []
                for col_name in x.keys():
                    if 'Bid' in col_name:
                        styles.append('background-color: lightgreen; '
                                      'color: black; font-weight: bold;')
                    elif 'Ask' in col_name:
                        styles.append('background-color: salmon; '
                                      'color: black; font-weight: bold;')
                    elif 'Value' in col_name:
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

            def format_with_spaces(value):
                """Format numeric values to have commas replaced by spaces, e.g. 1,234.56 -> 1 234.56."""
                try:
                    num = float(value)
                    if num.is_integer():
                        num = int(num)
                    formatted = f"{num:,}".replace(",", " ")
                    
                except ValueError:
                    formatted = value
                return formatted

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

        # Set required query parameters
        kwargs["category"] = category
        kwargs["symbol"] = symbol

        response = self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Market.GET_TICKERS}",
            query=kwargs,
        )

        # Check API response
        if response['retCode'] == 0:
            data_list = response.get('result', {}).get('list', [])
            if not data_list:
                # If the list is empty for some reason, return an empty DataFrame
                return pd.DataFrame()

            data = data_list[0]

            # If only_ticker is True, return just the float price
            if only_ticker:
                return float(data['lastPrice'])

            # If raw is True, return the entire response
            if raw:
                return response

            # Convert timestamp to a human-readable format
            # (Check if 'time' key exists to avoid KeyError in unpredictable responses)
            if 'time' in response:
                data['time'] = pd.to_datetime(response['time'], unit='ms').strftime('%H:%M:%S')
            else:
                data['time'] = 'N/A'

            # Create vertical DataFrame
            df_vertical = pd.DataFrame({
                "Info": ["Last Price", "Time"],
                "Value": [data['lastPrice'], data['time']]
            })

            # Create horizontal DataFrame
            df_horizontal = pd.DataFrame([{
                "Bid Price": data['bid1Price'],
                "Bid Size": data['bid1Size'],
                "Ask Price": data['ask1Price'],
                "Ask Size": data['ask1Size'],
                "24h High": data['highPrice24h'],
                "24h Low": data['lowPrice24h']
            }])

            styled_vertical = format_dashboard(df_vertical).set_caption(symbol)
            styled_horizontal = format_dashboard(df_horizontal).set_caption("Market Data")

            html_vertical = styled_vertical._repr_html_()
            html_horizontal = styled_horizontal._repr_html_()

            combined_html = f"""
            <table>
              <tr>
                <td style="vertical-align: top; padding-right: 20px;">{html_vertical}</td>
                <td style="vertical-align: top;">{html_horizontal}</td>
              </tr>
            </table>
            """

            # Display the combined HTML
            display_html(combined_html, raw=True)
            return None
        else:
            # If retCode is not zero, return an empty DataFrame for consistency
            return pd.DataFrame()


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

    
