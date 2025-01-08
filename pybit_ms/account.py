from pybit_ms._http_manager import HTTPManager
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib import colormaps


class Account(str, Enum):
    GET_WALLET_BALANCE = "/v5/account/wallet-balance"
    GET_BORROW_HISTORY = "/v5/account/borrow-history"
    REPAY_LIABILITY = "/v5/account/quick-repayment"
    GET_COLLATERAL_INFO = "/v5/account/collateral-info"
    SET_COLLATERAL_COIN = "/v5/account/set-collateral-switch"
    BATCH_SET_COLLATERAL_COIN = "/v5/account/set-collateral-switch-batch"
    GET_FEE_RATE = "/v5/account/fee-rate"
    GET_ACCOUNT_INFO = "/v5/account/info"
    GET_TRANSACTION_LOG = "/v5/account/transaction-log"
    GET_CONTRACT_TRANSACTION_LOG = "/v5/account/contract-transaction-log"
    SET_MARGIN_MODE = "/v5/account/set-margin-mode"
    GET_COIN_EXCHANGE_RECORDS = "/v5/asset/exchange/order-record"
    GET_USDC_CONTRACT_SETTLEMENT = "/v5/asset/settlement-record"
    GET_SINGLE_COIN_BALANCE = "/v5/asset/transfer/query-account-coin-balance"
    GET_TRANSFERABLE_COIN = "/v5/asset/transfer/query-transfer-coin-list"
    CREATE_INTERNAL_TRANSFER = "/v5/asset/transfer/inter-transfer"
    GET_INTERNAL_TRANSFER_RECORDS = (
        "/v5/asset/transfer/query-inter-transfer-list"
    )

    def __str__(self) -> str:
        return self.value
    

class Account_client:
    
    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint


    def get_wallet_balance(self, accountType, plot=False, raw=False, **kwargs):
        """
        Fetch and process the wallet balance from the Bybit API.

        This function retrieves wallet balance details, optionally plots a 
        pie chart of the balance distribution, and can return either the 
        raw response or formatted text output.

        Required args:
            accountType (string): Account type
                Unified account: UNIFIED
                Normal account: CONTRACT

        Args:
            plot (bool): Whether to plot the wallet balance as a pie chart.
            raw (bool): Whether to return the raw API response.
            **kwargs: Additional query parameters for the API request.

        Returns:
            dict or None: 
                - If raw=True, returns the full API response as a dictionary.
                - If raw=False, prints the wallet balance in a formatted manner.
        
        https://bybit-exchange.github.io/docs/v5/account/wallet-balance
        """


        def plot_wallet_balance(response):
            """
            Plot a pie chart for the wallet balance distribution.
            """
            coin_data = response['result']['list'][0]['coin']
            coins = [entry['coin'] for entry in coin_data]
            usd_values = [float(entry['usdValue']) for entry in coin_data]
            total_equity = float(response['result']['list'][0]['totalEquity'])

            cmap = colormaps.get_cmap("Set3")
            colors = [cmap(i / len(coins)) for i in range(len(coins))]

            explode = [0.05] * len(coins)

            plt.figure(figsize=(6, 6))
            plt.pie(
                usd_values,
                labels=coins,
                autopct='%1.1f%%',
                startangle=140,
                colors=colors,
                explode=explode
            )
            plt.title(f"Wallet Distribution\nTotal Equity: ${total_equity:,.2f}")
            plt.show()

        def format_wallet_balance(response):
            """
            Format the wallet balance into a readable string format.            
            """

            coin_data = response['result']['list'][0]['coin']
            total_equity = float(response['result']['list'][0]['totalEquity'])
            output_lines = []
            for entry in coin_data:
                coin = entry['coin']
                wallet_balance = float(entry['walletBalance'])
                usd_value = float(entry['usdValue'])
                output_lines.append(
                    f"{coin}: Wallet Balance = {wallet_balance:.6f}, "
                    f"USD Value = ${usd_value:.2f}"
                )
            print(f"Total equity: ${total_equity:,.2f}")
            print("\n".join(output_lines))
        
        kwargs["accountType"] = accountType

        # Fetch wallet balance from the API
        response = self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_WALLET_BALANCE}",
            query=kwargs,
            auth=True,
        )

        # Plot the wallet balance if requested
        if plot:
            plot_wallet_balance(response)

        # Return either the raw response or formatted wallet balance
        if raw:
            return response
        else:
            return format_wallet_balance(response)


    def repay_liability(self, **kwargs):
        """
        Repay liabilities of the Unified account.
        https://bybit-exchange.github.io/docs/v5/account/repay-liability
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.REPAY_LIABILITY}",
            query=kwargs,
            auth=True,
        )

    def get_collateral_info(self, **kwargs):
        """
        Get the collateral information, interest rate, etc.
        https://bybit-exchange.github.io/docs/v5/account/collateral-info
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_COLLATERAL_INFO}",
            query=kwargs,
            auth=True,
        )

    def set_collateral_coin(self, **kwargs):
        """
        Decide whether a coin is collateral in Unified account.
        https://bybit-exchange.github.io/docs/v5/account/set-collateral
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.SET_COLLATERAL_COIN}",
            query=kwargs,
            auth=True,
        )

    def batch_set_collateral_coin(self, **kwargs):
        """
        Batch decide which coins are collateral in Unified account.
        https://bybit-exchange.github.io/docs/v5/account/batch-set-collateral
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.BATCH_SET_COLLATERAL_COIN}",
            query=kwargs,
            auth=True,
        )

    def get_fee_rates(self, **kwargs):
        """
        Get derivatives trading fee rate.
        https://bybit-exchange.github.io/docs/v5/account/fee-rate
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_FEE_RATE}",
            query=kwargs,
            auth=True,
        )
    

    def get_account_info(self, raw=False):
        """
        Query account information (e.g., margin mode, account mode).

        Args:
            raw (bool, optional): If True, returns the raw API response. Defaults to False.

        Returns:
            tuple | dict:
                - If `raw=True`, returns the raw response (dict).
                - Otherwise, returns a tuple of (account_status, margin_mode) where
                  `account_status` is a descriptive string for the unifiedMarginStatus,
                  and `margin_mode` is the margin mode as reported by Bybit.

        Note:
            For more details, see
            https://bybit-exchange.github.io/docs/v5/account/account-info
        """

        response = self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_ACCOUNT_INFO}",
            auth=True,
        )

        # If raw output is requested, return the full response
        if raw:
            return response

        # Map the unifiedMarginStatus to a human-readable description
        accounts_dict = {
            1: "Classic account",
            3: "Unified trading account 1.0",
            4: "Unified trading account 1.0 (pro version)",
            5: "Unified trading account 2.0",
            6: "Unified trading account 2.0 (pro version)"
        }

        result = response.get('result', {})
        status_key = result.get('unifiedMarginStatus', '')
        account_status = accounts_dict.get(status_key, "Unknown")

        margin_mode = result.get('marginMode', '')

        return (account_status, margin_mode)


    def get_transaction_log(self, max_pages=None, **kwargs):
        """
        Query transaction logs in Unified account.
        https://bybit-exchange.github.io/docs/v5/account/transaction-log

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (limit, category, etc.).
        :return: A single-page response (dict) if max_pages is None,
                or a combined list of transaction-log items (list) if max_pages is set.
        """
        path = f"{self.endpoint}{Account.GET_TRANSACTION_LOG}"

        if max_pages:
            # Multi-page request
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
                max_pages=max_pages,
            )
        else:
            # Single-page request
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
            )
    
    def get_contract_transaction_log(self, max_pages=None, **kwargs):
        """
        Query transaction logs in Classic account.
        https://bybit-exchange.github.io/docs/v5/account/contract-transaction-log

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (limit, category, etc.).
        :return: A single-page response (dict) if max_pages is None,
                or a combined list of logs (list) if max_pages is set.
        """
        path = f"{self.endpoint}{Account.GET_CONTRACT_TRANSACTION_LOG}"

        if max_pages:
            # Multi-page request
            return self._http_manager._submit_paginated_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
                max_pages=max_pages,
            )
        else:
            # Single-page request
            return self._http_manager._submit_request(
                method="GET",
                path=path,
                query=kwargs,
                auth=True,
            )

    def set_margin_mode(self, **kwargs):
        """
        Set margin mode. 
        https://bybit-exchange.github.io/docs/v5/account/set-margin-mode
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.SET_MARGIN_MODE}",
            query=kwargs,
            auth=True,
        )
    
    def get_coin_exchange_records(self, max_pages=None, **kwargs):
        """
        Query the coin exchange records.
        https://bybit-exchange.github.io/docs/v5/asset/exchange

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query params (limit, coin, startTime, endTime, etc.).
        :return:
            - If max_pages is None (default), returns the standard Bybit response (dict) for a single page.
            - If max_pages is set, returns a list of exchange records aggregated across pages.
        """
        path = f"{self.endpoint}{Account.GET_COIN_EXCHANGE_RECORDS}"

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
        
    def get_usdc_contract_settlement(self, max_pages=None, **kwargs):
        """
        Query session settlement records of USDC perpetual and futures.
        
        Required args:
            category (string): Product type. e.g., "linear"

        https://bybit-exchange.github.io/docs/v5/asset/settlement

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g., limit, startTime, endTime, etc.).
        :return:
            - A single page (dict) if max_pages=None
            - A list of records aggregated across pages if max_pages is specified
        """
        path = f"{self.endpoint}{Account.GET_USDC_CONTRACT_SETTLEMENT}"

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
    
    def get_coin_balance(self, max_pages=None, **kwargs):
        """
        Query the balance of a specific coin in a specific account type.
        Supports querying sub-UID's balance.

        Required args:
            memberId (string): UID. Required when querying sub UID balance
            accountType (string): Account type

        https://bybit-exchange.github.io/docs/v5/asset/account-coin-balance

        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g. coin, memberId, accountType, limit).
        :return:
            - A single-page response (dict) if max_pages is None.
            - A list of records (combined from each page) if max_pages is set.
        """
        path = f"{self.endpoint}{Account.GET_SINGLE_COIN_BALANCE}"

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

    def get_transferable_coin(self, max_pages=None, **kwargs):
        """
        Query the transferable coin list between each account type.

        Required args:
            fromAccountType (string): From account type
            toAccountType (string): To account type

        https://bybit-exchange.github.io/docs/v5/asset/transferable-coin

        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g. limit, fromAccountType, toAccountType).
        :return:
            - A single-page response (dict) if max_pages is None.
            - A list of coins (combined from each page) if max_pages is set.
        """
        path = f"{self.endpoint}{Account.GET_TRANSFERABLE_COIN}"

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

    def create_internal_transfer(self, **kwargs):
        """Create the internal transfer between different account types under the same UID.

        Required args:
            transferId (string): UUID. Please manually generate a UUID
            coin (string): Coin
            amount (string): Amount
            fromAccountType (string): From account type
            toAccountType (string): To account type

            https://bybit-exchange.github.io/docs/v5/asset/create-inter-transfer
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.CREATE_INTERNAL_TRANSFER}",
            query=kwargs,
            auth=True,
        )
    
    def get_internal_transfer_records(self, max_pages=None, **kwargs):
        """
        Query the internal transfer records between different account types under the same UID.
        https://bybit-exchange.github.io/docs/v5/asset/inter-transfer-list

        :param max_pages: (int) If provided, fetch multiple pages up to this limit.
        :param kwargs: Additional parameters (e.g., coin, startTime, endTime, etc.).
        :return:
            - A single-page response dict if max_pages is None
            - A list of transfer records (combined from each page) if max_pages is set
        """
        path = f"{self.endpoint}{Account.GET_INTERNAL_TRANSFER_RECORDS}"

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



    
