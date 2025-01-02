from enum import Enum


class InstitutionalLoan(str, Enum):
    GET_PRODUCT_INFO = "/v5/ins-loan/product-infos"
    GET_MARGIN_COIN_INFO = "/v5/ins-loan/ensure-tokens-convert"
    GET_LOAN_ORDERS = "/v5/ins-loan/loan-order"
    GET_REPAYMENT_ORDERS = "/v5/ins-loan/repaid-history"
    GET_LTV = "/v5/ins-loan/ltv-convert"

    def __str__(self) -> str:
        return self.value
