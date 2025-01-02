from enum import Enum


class Asset(str, Enum):
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
