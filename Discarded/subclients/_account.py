from ._http_manager import HTTPManager
from .account import Account


class AccountHTTP:
    
    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

    def get_wallet_balance(self, **kwargs):
        """
        Obtain wallet balance, query asset information, etc.
        https://bybit-exchange.github.io/docs/v5/account/wallet-balance
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_WALLET_BALANCE}",
            query=kwargs,
            auth=True,
        )
    
    def get_borrow_history(self, max_pages=None, **kwargs):
        """
        Get interest records in reverse order of creation time.
        If you specify 'max_pages', multiple pages are fetched (cursor-based).
        
        https://bybit-exchange.github.io/docs/v5/account/borrow-history

        :param max_pages: (int) Maximum number of pages to fetch, or None for a single request.
        :param kwargs: Additional request params (like 'limit', 'accountType', etc.).
        :return: Single page (default) or combined list (if using pagination).
        """
        path = f"{self.endpoint}{Account.GET_BORROW_HISTORY}"

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

    def get_account_info(self, **kwargs):
        """
        Query the margin mode configuration of the account.
        https://bybit-exchange.github.io/docs/v5/account/account-info
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_ACCOUNT_INFO}",
            query=kwargs,
            auth=True,
        )

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
