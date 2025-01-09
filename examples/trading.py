from read_api_keys import read_api_keys
import sys

sys.path.append('c:\\Users\\Samuele\\Desktop\\Bocconi\\4th Year\\Software Engineering\\Project\\pybit_ms')
from pybit_ms.bybit_client import BybitAPI

keys = read_api_keys("TAK.txt")
public_key = keys.get('PUBLIC_KEY')
private_key = keys.get('PRIVATE_KEY')

client = BybitAPI(api_key=public_key, api_secret=private_key, testnet=1)
print(client)

["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "TRX", "ADA", "AVAX", "SHIB", "LINK", "DOT", "LTC", "PEPE", "FET", "XLM", "SUI", "VET", "OP", "GRT", "RUNE", "FLOKI", "GALA", "ALGO", "FTM", "HBAR", "SEI", "EOS", "KLAY", "NEAR", "STX", "MANA"]
coin1="BTC"
client.market.get_kline(category="linear", coin1=coin1, coin2="USDT", interval="60", price_type="close", limit=720)

