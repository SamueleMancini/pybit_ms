from enum import Enum


class SpotMarginTrade(str, Enum):
    # UTA endpoints
    TOGGLE_MARGIN_TRADE = "/v5/spot-margin-trade/switch-mode"
    SET_LEVERAGE = "/v5/spot-margin-trade/set-leverage"
    VIP_MARGIN_DATA = "/v5/spot-margin-trade/data"
    STATUS_AND_LEVERAGE = "/v5/spot-margin-trade/state"
    # normal mode (non-UTA) endpoints
    NORMAL_GET_BORROW_COLLATERAL_LIMIT = "/v5/crypto-loan/borrowable-collateralisable-number"
    NORMAL_GET_COLLATERAL_COIN_INFO = "/v5/crypto-loan/collateral-data"
    NORMAL_GET_BORROWABLE_COIN_INFO = "/v5/crypto-loan/loanable-data"
    NORMAL_GET_UNPAID_LOAN_ORDERS = "/v5/crypto-loan/ongoing-orders"
    NORMAL_BORROW = "/v5/crypto-loan/borrow"
    NORMAL_REPAY = "/v5/crypto-loan/repay"
    NORMAL_GET_LOAN_ORDER_HISTORY = "/v5/crypto-loan/borrow-history"
    NORMAL_GET_REPAYMENT_ORDER_HISTORY = "/v5/crypto-loan/repayment-history"
    NORMAL_ADJUST_COLLATERAL_AMOUNT = "/v5/crypto-loan/adjust-ltv"
    NORMAL_GET_LOAN_ADJUSTMENT_HISTORY = "/v5/crypto-loan/adjustment-history"
    NORMAL_GET_MAX_REDUCTION_COLLATERAL_AMOUNT = "/v5/crypto-loan/max-collateral-amount"

    def __str__(self) -> str:
        return self.value
