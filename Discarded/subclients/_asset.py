from ._http_manager import HTTPManager
from .asset import Asset


class AssetHTTP:

    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

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
        path = f"{self.endpoint}{Asset.GET_COIN_EXCHANGE_RECORDS}"

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
        path = f"{self.endpoint}{Asset.GET_USDC_CONTRACT_SETTLEMENT}"

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
        path = f"{self.endpoint}{Asset.GET_SINGLE_COIN_BALANCE}"

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
        path = f"{self.endpoint}{Asset.GET_TRANSFERABLE_COIN}"

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
            path=f"{self.endpoint}{Asset.CREATE_INTERNAL_TRANSFER}",
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
        path = f"{self.endpoint}{Asset.GET_INTERNAL_TRANSFER_RECORDS}"

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
