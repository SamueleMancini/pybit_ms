import requests
import ftx_client


secret_key_ftx = 'secret_key_ftx'
api_key_ftx = 'api_key_ftx'


client_ftx = ftx_client.FtxClient(api_key=api_key_ftx, api_secret=secret_key_ftx)
balance = client_ftx.get_balances()

print(balance[0]['free'])
filled = 0
while filled == 0:
    orderbook = requests.get('https://ftx.com/api/markets/XRP/USD/orderbook').json()
    bid_price_ftx = orderbook['result']['bids'][0][0]
    ask_price_ftx = orderbook['result']['asks'][0][0]

    try:
        s_ftx = client_ftx.place_order(market="XRP/USD", side="buy", price= ask_price_ftx, size= balance[0]['free'] , ioc=True)
        print("Order:", s_ftx)
        print('\n\n', orderbook)
        order = client_ftx.get_order_status(s_ftx['id'])
        filled = order['filledSize']
        print(filled, '\n', order['status'])
        if filled == 0:
            print("NOT FILLED\n")
        else:
            print("SUCCESSFULL")
        
    except Exception as e:
        print(f'Error making Ftx second order request: {e}')

print(client_ftx.get_order_history()[0],'\n\n',client_ftx.get_order_history()[1], '\n\n', balance, '\n\n\n\n', client_ftx.get_order_status('161841685389'))