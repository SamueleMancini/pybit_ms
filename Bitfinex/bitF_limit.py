import requests
import bitfinex_client


SecretKey_bitF = 'SecretKey_bitF'
ApiKey_bitF = 'ApiKey_bitF'


client_bitF = bitfinex_client.BitF_client(ApiKey_bitF, SecretKey_bitF)
orderbook = requests.get('https://api.bitfinex.com/v1/book/BTCUSD').json()
bid_price_bitF = orderbook['bids'][0]['price']
ask_price_bitF = orderbook['asks'][0]['price']

try:
    s_bitF = client_bitF.submit_order(order_type= "EXCHANGE LIMIT", symbol= "tBTCUSD", price= str(float(ask_price_bitF) - 5), amount= (20 / float(ask_price_bitF)))
    order = client_bitF.active_orders()[0]
    status = order[13]
    print(s_bitF, "\n\n\n\n")
    print(order)

except Exception as e:
    print("ERROR OCCURRED AS:", e)
