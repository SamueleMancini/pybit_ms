from ._http_manager import HTTPManager
from .spot_margin_trade import SpotMarginTrade


class SpotMarginTradeHTTP:
    
    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

    def spot_margin_trade_get_vip_margin_data(self, **kwargs):
        """
        https://bybit-exchange.github.io/docs/v5/spot-margin-uta/vip-margin
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.VIP_MARGIN_DATA}",
            query=kwargs,
        )

    def spot_margin_trade_toggle_margin_trade(self, **kwargs):
        """UTA only. Turn spot margin trade on / off.

        Required args:
            spotMarginMode (string): 1: on, 0: off

        https://bybit-exchange.github.io/docs/v5/spot-margin-uta/switch-mode
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.TOGGLE_MARGIN_TRADE}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_set_leverage(self, **kwargs):
        """UTA only. Set the user's maximum leverage in spot cross margin

        Required args:
            leverage (string): Leverage. [2, 5].

        https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-leverage
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.SET_LEVERAGE}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_get_status_and_leverage(self):
        """
        https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.STATUS_AND_LEVERAGE}",
            auth=True,
        )

    def spot_margin_trade_normal_get_borrowable_coin_info(self, **kwargs):
        """Normal (non-UTA) account only.

        https://bybit-exchange.github.io/docs/v5/crypto-loan/loan-coin
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_BORROWABLE_COIN_INFO}",
            query=kwargs,
        )

    def spot_margin_trade_normal_get_collateral_coin_info(self, **kwargs):
        """Normal (non-UTA) account only. Turn on / off spot margin trade

        https://bybit-exchange.github.io/docs/v5/crypto-loan/collateral-coin
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_COLLATERAL_COIN_INFO}",
            query=kwargs,
        )

    def spot_margin_trade_normal_get_borrow_collateral_limit(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            loanCurrency (string): Loan coin name
            collateralCurrency (string): Collateral coin name

        https://bybit-exchange.github.io/docs/v5/crypto-loan/acct-borrow-collateral
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_BORROW_COLLATERAL_LIMIT}",
            query=kwargs,
        )
    
    def spot_margin_trade_normal_get_unpaid_loan_orders(self, **kwargs):
        """Normal (non-UTA) account only.

        https://bybit-exchange.github.io/docs/v5/crypto-loan/unpaid-loan-order
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_UNPAID_LOAN_ORDERS}",
            query=kwargs,
            auth=True,
        )
    
    def spot_margin_trade_normal_borrow(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            loan currency (string): Loan coin name
            collateral currency (string): Currency used to mortgage
            loan amount (string): Amount to borrow

        https://bybit-exchange.github.io/docs/v5/crypto-loan/borrow
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_BORROW}",
            query=kwargs,
            auth=True,
        )

    def spot_margin_trade_normal_repay(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            order Id (string): Loan order ID
            amount (string): Repay amount

        https://bybit-exchange.github.io/docs/v5/crypto-loan/repay
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_REPAY}",
            query=kwargs,
            auth=True,
        )
    
    def spot_margin_trade_normal_get_loan_order_history(self, max_pages=None, **kwargs):
        """
        Query the loan order history for Normal (non-UTA) accounts only.

        https://bybit-exchange.github.io/docs/v5/crypto-loan/comleted-loan-order

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g., symbol, limit, startTime, endTime, etc.).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of loan order history items if max_pages is set.
        """
        path = f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_LOAN_ORDER_HISTORY}"

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
    def spot_margin_trade_normal_get_repayment_order_history(self, max_pages=None, **kwargs):
        """
        Query the repayment order history for Normal (non-UTA) accounts only.

        https://bybit-exchange.github.io/docs/v5/crypto-loan/repay-transaction

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters (e.g., symbol, limit, startTime, endTime, etc.).
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of repayment order history items if max_pages is set.
        """
        path = f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_REPAYMENT_ORDER_HISTORY}"

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
    
    def spot_margin_trade_normal_get_max_reduction_collateral_amount(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            order Id (string): Loan order ID

        https://bybit-exchange.github.io/docs/v5/crypto-loan/reduce-max-collateral-amt
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_MAX_REDUCTION_COLLATERAL_AMOUNT}",
            query=kwargs,
            auth=True,
        )
    
    def spot_margin_trade_normal_adjust_collateral_amount(self, **kwargs):
        """Normal (non-UTA) account only.

        Required args:
            order Id (string): Loan order ID
            amount (string): Adjstment amount
            direction (string): 0: add collateral, 1: reduce collateral
        
        https://bybit-exchange.github.io/docs/v5/crypto-loan/adjust-collateral
        """
        return self._http_manager._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotMarginTrade.NORMAL_ADJUST_COLLATERAL_AMOUNT}",
            query=kwargs,
            auth=True,
        )
    
    def spot_margin_trade_normal_get_loan_adjustment_history(self, max_pages=None, **kwargs):
        """
        Query the transaction history of collateral amount adjustment for Normal (non-UTA) accounts only.

        https://bybit-exchange.github.io/docs/v5/crypto-loan/ltv-adjust-history

        :param max_pages: (int) If set, fetch multiple pages up to this limit.
        :param kwargs: Additional query parameters.
        :return:
            - A single Bybit response dict if max_pages is None.
            - A combined list of repayment order history items if max_pages is set.
        """
        path = f"{self.endpoint}{SpotMarginTrade.NORMAL_GET_LOAN_ADJUSTMENT_HISTORY}"

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
