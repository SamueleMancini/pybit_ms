import asyncio
import requests
import websockets
import json
import csv
from pprint import pprint
import datetime
import os
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import time
import numpy as np

api_key = 'api_key'
secr_key = 'secr_key'


def convert_timestamp_to_date(timestamp_ms):
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.datetime.fromtimestamp(timestamp_s)
    formatted_date = date_time.strftime('%Y-%m-%d %H:%M')
    
    return formatted_date


def convert_date_to_timestamp(date_str, date_format='%Y-%m-%d %H:%M'):
    date_time = datetime.datetime.strptime(date_str, date_format)
    timestamp_seconds = datetime.datetime.timestamp(date_time)
    timestamp_milliseconds = int(timestamp_seconds * 1000)
    
    return timestamp_milliseconds


def get_historical_klines(symbol, interval, start_str, end_str=None, limit=1000):
    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol,
        'interval': interval,
        'startTime': start_str,
        'limit': limit}
    response = requests.get(url, params=params)
    data = response.json()

    return data


def send_signed_req(method, params, endpoints):
    url = f'https://api.binance.com/{endpoints}'

    query_string = urlencode(params)
    signature = hmac.new(secr_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params['signature'] = signature

    if method == 'get':
        response = requests.get(
        url,
        headers={'X-MBX-APIKEY': api_key},
        params=params
        )
    elif method == 'post':
        response = requests.post(
        url,
        headers={'X-MBX-APIKEY': api_key},
        params=params
        )
    return response.text


def get_margin_interest_fee(symbol):
    url = 'sapi/v1/margin/isolatedMarginData'
    params = {
        'vipLevel':0,
        'symbol': f'{symbol}USDT',
        'timestamp': int(time.time() * 1000)
    }
    response = send_signed_req('get', params, url)
    return float(eval(response)[0]['data'][0]['dailyInterest']) / 24


def get_liquidation_risk_ratio(symbol):
    url = 'sapi/v1/margin/isolatedMarginTier'
    params = {'symbol': symbol,
        'tier': 1,
        'timestamp': int(time.time() * 1000),
        }
    response = send_signed_req('get', params, url)
    return response


def liquidation_price(coin, open_price, collateral, quantity, hours, liquidation_rates, margin_fees):
    M = liquidation_rates[f'{coin}']
    interests_fee = margin_fees[f'{coin}']
    # current_price = float(get_historical_klines(f"{coin}USDT", '1m', int(time.time()*1000) - 60000, limit=1)[0][4])
    liquidation_price = (collateral - quantity * open_price * 0.001 + quantity * open_price)/ (M * (quantity + hours * np.max([interests_fee * quantity, 1e-8])))
    return liquidation_price


def format_kline_response(response):
    kline_keys = ["open_time",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore"]
    formatted_responses = []
    for kline in response:
        formatted_response = dict(zip(kline_keys, kline))
        del formatted_response['ignore']
        formatted_response['open_time'] = convert_timestamp_to_date(formatted_response['open_time'])
        formatted_response['close_time'] = convert_timestamp_to_date(formatted_response['close_time'])
        formatted_responses.append(formatted_response)
    
    return formatted_responses


def read_last_time_up(time):
    dt_object = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    one_minute = datetime.timedelta(minutes=1)
    new_time = dt_object + one_minute
    new_time_str = new_time.strftime('%Y-%m-%d %H:%M')

    return new_time_str