# pybit_ms

This library is a modification of the official **pybit** library, designed to facilitate trading automation and analysis.

---

## Installation Instructions

Install the library using `pip` with the following command:

```bash
pip install pybit_ms
```

---

## Usage example

Import the BybitAPI class required for interacting with the Bybit's API:

```python
from pybit_ms import BybitAPI    
```    

<br>

### 1. Public endpoint:


First we show how to query a public endpoint, i.e. one that does not require porfile authentication. In this example we implement the get_tickers() function which queries the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.

Initialize the BybitAPI class wit:

```python
api = BybitAPI()
```

and query with parameters of your choice, for example spot trade, and coin pair BTC-USDT:

```python
api.market.get_tickers(category="spot", symbol="BTCUSDT", only_ticker=False, raw=False)
```
<br>

This will display an html table like the one below:

(table)

In case we are only interested in the price we can set the only_ticker parameter to True, or set the raw parameter to True for the complete raw request response.



### 2. Private endpoint:

To query a private endpoint we need to pass our API keys as parameters in the intial BybitAPI client class. Store the API keys in two string variables: public_key and private_key.

Initialize the BybitAPI client class wit:

```python
api = BybitAPI(testnet=True, api_key=public_key, api_secret=private_key)
```

<br>

Note: 
* it is always good practice to store the actual keys in a separate file and read them from there when necessary (refer to safe_api.py file in the examples folder for an example of how to store and read them).
* when experimenting for the first times or for simulations you can set the testnet parameter to true and use your Bybit's testnt apikeys to login into the Bybit's Testnet account. 

<br>

Now we can query private endpoints like looking at our wallet balance with the command get_wallet_balance():

```python
api.account.get_wallet_balance(accountType="UNIFIED", plot=False, raw=False)
```

Like in this example, if desired this will allow us, through the corresponding parameters, to look at a pie chart of our wallet balance and have formatted response:

(image)

Total equity: $105,277.80

BTC: Wallet Balance = 1.001055, USD Value = $95510.41

ETH: Wallet Balance = 1.288068, USD Value = $4329.78

USDT: Wallet Balance = 5439.141664, USD Value = $5437.61