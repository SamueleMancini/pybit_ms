import requests
import time
import hmac
import hashlib
import json
from json.decoder import JSONDecodeError

PUBLIC_PREFIX = "api-pub"
PRIVATE_PREFIX = "api"
HOST = "bitfinex.com"
VERSION = "v2"


class BitF_client:

    def __init__(self, key=None, secret=None):
        self.private_url = "https://%s.%s/" % (PRIVATE_PREFIX, HOST)
        self.public_url = "https://%s.%s/" % (PUBLIC_PREFIX, HOST)
        self.key = key
        self.secret = secret


    def _nonce(self):
        return str(float(time.time() * 1000))


    def _headers(self, path, nonce, body):
        """
        create signed headers
        """
        signature = "/api/{}{}{}".format(path, nonce, body)
        hmc = hmac.new(self.secret.encode('utf8'), signature.encode('utf8'), hashlib.sha384)
        signature = hmc.hexdigest()
        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.key,
            "bfx-signature": signature,
            "content-type": "application/json"
        }


    def _post(self, path, payload, verify=False):
        """
        Send post request to bitfinex
        """
        nonce = self._nonce()
        headers = self._headers(path, nonce, payload)
        response = requests.post(self.private_url + path, headers=headers, data=payload, verify=verify)

        if response.status_code == 200:
            return response.json()
        else:
            try:
                content = response.json()
            except JSONDecodeError:
                content = response.text
            raise Exception(response.status_code, response.reason, content)


    def _public_post(self, path, payload, verify=False):
        """
        Send post request to bitfinex
        """
        response = requests.post(self.public_url + path, data=payload, verify=verify)

        if response.status_code == 200:
            return response.json()
        else:
            try:
                content = response.json()
            except JSONDecodeError:
                content = response.text
            raise Exception(response.status_code, response.reason, content)


    def _get(self, path, **params):
        """
        Send get request to bitfinex
        """
        url = self.public_url + path
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            try:
                content = response.json()
            except JSONDecodeError:
                content = response.text
            raise Exception(response.status_code, response.reason, content)


    def ticker(self, symbol):
        path = "v2/ticker/{}".format(symbol)
        response = self._get(path)
        return response


    def book(self, symbol, precision="P0", **kwargs):
        params="?"
        for key, value in kwargs.items():
            params = f"{params}{key}={value}&"
        params = params[:-1] # remove last & or ? if there are no optional parameters 

        path = "v2/book/{}/{}{}".format(symbol, precision, params)
        response = self._get(path)
        return response


    def wallets_balance(self):
        body = {}
        raw_body = json.dumps(body)
        path = "v2/auth/r/wallets"
        response = self._post(path, raw_body, verify=True)
        return response
    

    def wallets_history(self, **kwargs):
        raw_body = json.dumps(kwargs)
        path = "v2/auth/r/wallets/hist"
        response = self._post(path, raw_body, verify=True)
        return response


    def active_orders(self, trade_pair=""):
        path = "v2/auth/r/orders/{}".format(trade_pair)
        response = self._post(path, "", verify=True)
        return response


    def submit_order(self, order_type, symbol, amount, price= None, **kwargs):
        body = {
            "type": order_type,
            "symbol": symbol,
            "price": str(price),
            "amount": str(amount),
            "meta": {"aff_code": "b2UR2iQr"},
            **kwargs
        }

        path = "v2/auth/w/order/submit"
        response = self._post(path, json.dumps(body), verify=True)
        return response


    def order_update(self, order_id, **kwargs):
        body = {
            "id": order_id,
            **kwargs
        }

        path = "v2/auth/w/order/update"
        response = self._post(path, json.dumps(body), verify=True)
        return 


    def cancel_order(self, **kwargs):
        body = {
            **kwargs
        }

        path = "v2/auth/w/order/cancel"
        response = self._post(path, json.dumps(body), verify=True)
        return response


    def orders_history(self, trade_pair=None, **kwargs):
        body = kwargs
        raw_body = json.dumps(body)
        if trade_pair:
            path = "v2/auth/r/orders/{}/hist".format(trade_pair)
        else:
            path = "v2/auth/r/orders/hist"
        response = self._post(path, raw_body, verify=True)
        return response


    def trades_history(self, trade_pair=None, **kwargs):
        raw_body = json.dumps(kwargs)
        if trade_pair is None:
            path = "v2/auth/r/trades/hist"  # will load history for all pairs
        else:
            path = "v2/auth/r/trades/{}/hist".format(trade_pair)
        response = self._post(path, raw_body, verify=True)
        return response


    def active_positions(self):
        body = {}
        raw_body = json.dumps(body)
        path = "v2/auth/r/positions"
        response = self._post(path, raw_body, verify=True)
        return response


    def positions_history(self, **kwargs):
        body = kwargs
        raw_body = json.dumps(body)
        path = "v2/auth/r/positions/hist"
        response = self._post(path, raw_body, verify=True)
        return response