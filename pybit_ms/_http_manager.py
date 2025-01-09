import time
import hmac
import hashlib
import base64
import json
import logging
import requests

from datetime import datetime as dt, timezone
from json.decoder import JSONDecodeError

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from pybit_ms._exceptions import FailedRequestError, InvalidRequestError

HTTP_URL = "https://{SUBDOMAIN}.bybit.com"
SUBDOMAIN_TESTNET = "api-testnet"
SUBDOMAIN_MAINNET = "api"


def _generate_signature(use_rsa, secret, param_str):
    """Generate either HMAC-SHA256 or RSA signature for Bybit."""
    if not use_rsa:
        hashed = hmac.new(
            key=secret.encode("utf-8"),
            msg=param_str.encode("utf-8"),
            digestmod=hashlib.sha256,
        )
        return hashed.hexdigest()
    else:
        hash_obj = SHA256.new(param_str.encode("utf-8"))
        encoded_signature = base64.b64encode(
            PKCS1_v1_5.new(RSA.importKey(secret)).sign(hash_obj)
        )
        return encoded_signature.decode()


class HTTPManager:
    """
    A streamlined HTTP manager for Bybit V5 endpoints.
    
    - Supports testnet/mainnet via 'testnet' bool.
    - HMAC or RSA authentication.
    - Optional retry logic for known transient errors.
    - Logging and request/response inspection.
    """

    def __init__(
        self,
        testnet: bool = False,
        rsa_authentication: bool = False,
        api_key: str = None,
        api_secret: str = None,
        logging_level: int = logging.INFO,
        log_requests: bool = False,
        timeout: int = 10,
        recv_window: int = 5000,
        force_retry: bool = False,
        max_retries: int = 3,
        retry_delay: float = 3.0,
    ):
        self.testnet = testnet
        self.rsa_authentication = rsa_authentication
        self.api_key = api_key
        self.api_secret = api_secret
        self.log_requests = log_requests
        self.timeout = timeout
        self.recv_window = recv_window
        self.force_retry = force_retry
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        subdomain = SUBDOMAIN_TESTNET if self.testnet else SUBDOMAIN_MAINNET
        self.endpoint = HTTP_URL.format(SUBDOMAIN=subdomain)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)

        # If no handlers on the root, add one for this logger.
        if not logging.root.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            handler.setLevel(logging_level)
            self.logger.addHandler(handler)

        self.logger.debug(f"Initialized HTTPManager for {'testnet' if testnet else 'mainnet'}.")

        self.client = requests.Session()
        self.client.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Common Bybit error codes that may warrant a retry
        self.retry_codes = {10002, 10006, 30034, 30035, 130035, 130150}

    @staticmethod
    def _prepare_payload(method, params):
        """
        Prepare payload for a Bybit request:
          - GET => query string
          - others => JSON-encoded string
        Also casts certain fields to the expected types.
        """
        string_params = ["qty", "price", "triggerPrice", "takeProfit", "stopLoss"]
        integer_params = ["positionIdx"]

        for k, v in params.items():
            if v is None:
                continue
            if k in string_params and not isinstance(v, str):
                params[k] = str(v)
            elif k in integer_params and not isinstance(v, int):
                params[k] = int(v)

        if method.upper() == "GET":
            return "&".join(f"{k}={v}" for k, v in sorted(params.items()) if v is not None)
        else:
            return json.dumps(params)

    def _sign(self, payload, timestamp):
        """
        Generate signature for authenticated endpoints using the Bybit formula.
        """
        if not self.api_key or not self.api_secret:
            raise PermissionError("API key/secret needed for authenticated endpoints.")

        param_str = f"{timestamp}{self.api_key}{self.recv_window}{payload}"
        return _generate_signature(self.rsa_authentication, self.api_secret, param_str)

    def _submit_request(self, method, path, query=None, auth=False):
        """
        Primary request submission function. Retries certain known errors if configured.
        """
        if query is None:
            query = {}

        # Convert floats that are effectively ints (e.g., 1.0) to int to avoid signature mismatch
        for k, v in query.items():
            if isinstance(v, float) and v.is_integer():
                query[k] = int(v)

        retries_attempted = 0
        req_params = None

        while True:
            if retries_attempted > self.max_retries:
                raise FailedRequestError(
                    request=f"{method} {path}: {req_params}",
                    message="Maximum retries exceeded.",
                    status_code=400,
                    time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                    resp_headers=None,
                )

            req_params = self._prepare_payload(method, query)

            headers = {}
            if auth:
                timestamp = int(time.time() * 1e3)  # ms
                sig = self._sign(req_params, timestamp)
                headers.update(
                    {
                        "X-BAPI-API-KEY": self.api_key,
                        "X-BAPI-SIGN": sig,
                        "X-BAPI-SIGN-TYPE": "2",
                        "X-BAPI-TIMESTAMP": str(timestamp),
                        "X-BAPI-RECV-WINDOW": str(self.recv_window),
                    }
                )

            # Build request
            if method.upper() == "GET":
                url = f"{path}?{req_params}" if req_params else path
                req_obj = requests.Request(method, url, headers=headers)
            else:
                req_obj = requests.Request(method, path, data=req_params, headers=headers)

            prepared = self.client.prepare_request(req_obj)

            if self.log_requests:
                self.logger.debug(
                    f"Request -> {method.upper()} {path}, Auth={auth}, "
                    f"Payload={req_params if method.upper() != 'GET' else None}, "
                    f"Headers={headers}, Attempt={retries_attempted+1}"
                )

            try:
                resp = self.client.send(prepared, timeout=self.timeout)
            except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.SSLError,
                requests.exceptions.ConnectionError,
            ) as e:
                if self.force_retry:
                    self.logger.error(f"Network error: {e}; retrying in {self.retry_delay}s.")
                    time.sleep(self.retry_delay)
                    retries_attempted += 1
                    continue
                else:
                    raise FailedRequestError(
                        request=f"{method} {path}: {req_params}",
                        message=str(e),
                        status_code=None,
                        time=dt.utcnow().strftime("%H:%M:%S"),
                        resp_headers=None,
                    )

            if resp.status_code != 200:
                err_msg = "HTTP status != 200"
                if resp.status_code == 403:
                    err_msg = "IP or region restricted, or IP rate limit breach."
                self.logger.debug(f"Response text: {resp.text}")
                raise FailedRequestError(
                    request=f"{method} {path}: {req_params}",
                    message=err_msg,
                    status_code=resp.status_code,
                    time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                    resp_headers=resp.headers,
                )

            try:
                data = resp.json()
            except JSONDecodeError:
                if self.force_retry:
                    self.logger.error(f"JSONDecodeError; retrying in {self.retry_delay}s.")
                    time.sleep(self.retry_delay)
                    retries_attempted += 1
                    continue
                else:
                    raise FailedRequestError(
                        request=f"{method} {path}: {req_params}",
                        message="Could not decode JSON.",
                        status_code=409,
                        time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                        resp_headers=resp.headers,
                    )

            ret_code = data.get("retCode", 0)
            ret_msg = data.get("retMsg", "OK")

            if ret_code != 0:
                # Potentially fixable errors
                if ret_code in self.retry_codes:
                    self.logger.error(f"Error code {ret_code}: {ret_msg}; retrying.")
                    if ret_code == 10002:
                        self.recv_window += 2500
                        self.logger.debug("Increased recv_window by 2500ms.")
                    time.sleep(self.retry_delay)
                    retries_attempted += 1
                    continue
                else:
                    raise InvalidRequestError(
                        request=f"{method} {path}: {req_params}",
                        message=ret_msg,
                        status_code=ret_code,
                        time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                        resp_headers=resp.headers,
                    )

            if self.log_requests:
                self.logger.debug(f"Response -> {data}")

            return data
        
        
    def _submit_paginated_request(
        self,
        method: str,
        path: str,
        query=None,
        auth=False,
        max_pages: int = None,
    ):
        """
        Fetch multiple pages using Bybit's cursor-based pagination.
        - 'nextPageCursor' in response['result'] indicates the next cursor.
        - Pass 'cursor' in the request query to get the next page.

        :param method: e.g. "GET" or "POST"
        :param path: full URL, typically self.endpoint + "/v5/..."
        :param query: dict of query params (including 'limit' if desired)
        :param auth: whether this endpoint needs authentication
        :param max_pages: if set, fetch at most this many pages (default is all pages)

        :return: a combined list of all items from 'result["list"]' across all pages
        """
        if query is None:
            query = {}

        all_records = []
        current_cursor = None
        pages_fetched = 0

        while True:
            # Add cursor to the query if we have one
            if current_cursor:
                query["cursor"] = current_cursor

            # Single-page request using the existing logic
            single_response = self._submit_request(method, path, query=query, auth=auth)
            result = single_response.get("result", {})
            records = result.get("list", [])
            all_records.extend(records)

            # Check nextPageCursor
            next_cursor = result.get("nextPageCursor")
            if not next_cursor:
                # No more pages
                break

            # Prepare for next iteration
            current_cursor = next_cursor
            pages_fetched += 1

            # If max_pages was given and we've hit it, stop
            if max_pages is not None and pages_fetched >= max_pages:
                break

        return all_records
