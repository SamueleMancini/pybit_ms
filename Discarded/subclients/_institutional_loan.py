from ._http_manager import HTTPManager
from .institutional_loan import InstitutionalLoan as InsLoan


class InstitutionalLoanHTTP:
    
    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager
        self.endpoint = http_manager.endpoint

    def get_product_info(self, **kwargs) -> dict:
        """
            https://bybit-exchange.github.io/docs/v5/otc/margin-product-info
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_PRODUCT_INFO}",
            query=kwargs,
        )

    def get_margin_coin_info(self, **kwargs) -> dict:
        """
            https://bybit-exchange.github.io/docs/v5/otc/margin-coin-convert-info
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_MARGIN_COIN_INFO}",
            query=kwargs,
        )

    def get_loan_orders(self, **kwargs) -> dict:
        """
        Get loan orders information
            https://bybit-exchange.github.io/docs/v5/otc/loan-info
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_LOAN_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_repayment_info(self, **kwargs) -> dict:
        """
        Get a list of your loan repayment orders (orders which repaid the loan).
            https://bybit-exchange.github.io/docs/v5/otc/repay-info
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_REPAYMENT_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_ltv(self, **kwargs) -> dict:
        """
        Get your loan-to-value ratio.
            https://bybit-exchange.github.io/docs/v5/otc/ltv-convert
        """
        return self._http_manager._submit_request(
            method="GET",
            path=f"{self.endpoint}{InsLoan.GET_LTV}",
            query=kwargs,
            auth=True,
        )
