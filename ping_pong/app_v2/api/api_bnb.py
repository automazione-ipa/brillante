# Binance API
from typing import Optional
import logging

from binance.error import ClientError as BinanceClientError
from binance.api import API
from binance.cm_futures import CMFutures
from binance.lib.utils import config_logging

from app_v2.logic.entities import BNBOrderRequest

BINANCE_TEST_KEY = 'f7bbd52eea221cd6344a20aa78f62e0fecf6fb56b13de128cb457a968f9c16b3'
BINANCE_TEST_SECRET = 'b55adf0fc1043fca45ed3ba7179c97b1f774b5aa151e805faeea7e4ae9c88f54'

BNB_FUTURES = 'https://fapi.binance.com'
BNB_TESTNET = 'https://testnet.binancefuture.com'
BNB_LEV = "/fapi/v1/leverage"
BNB_ORD = "/fapi/v1/order"

class ApiCallBinance:
    def __init__(self, api_key, secret_key, base_url):
        self.bnb_api = API(
            testnet=False,
            api_key=api_key,
            api_secret=secret_key,
            base_url=base_url
        )

        self.cm_futures_client = CMFutures()

    # OK
    def bnb_set_leverage(
            self,
            endpoint: str,
            symbol: str,
            lev: float
        ):
        """
        Set leverage for a symbol in Binance Futures.
        """
        payload = {"symbol": symbol, "leverage": lev}
        try:
            response = self.bnb_api.sign_request("POST", endpoint, payload)
            print("Leverage set successfully:", response)
        except BinanceClientError as e:
            print(f"Failed to set leverage: {e}")

    def bnb_place_order(
            self,
            endpoint: str,
            bnb_request: BNBOrderRequest,
            short: Optional[bool] = False
        ):
        """
        Place a short order for a symbol in Binance Futures.
        """
        side = "BUY"
        if short is True:
            side = "SELL"

        payload = {
            "symbol": bnb_request.symbol,
            "side": side,
            "type": "LIMIT" if bnb_request.price else "MARKET",
            "quantity": bnb_request.amount,
        }
        if bnb_request.price:
            payload["price"] = bnb_request.price
            payload["timeInForce"] = "GTC"
        
        try:
            response = self.bnb_api.sign_request("POST", endpoint, payload)
            print("Order placed successfully:", response)
            return response
        except BinanceClientError as e:
            print(f"Failed to place order: {e}")

    # funding = bnb_funding(symbol="BTCUSD_PERP")
    def bnb_funding(self, symbol: str = "BTCUSD"):
        config_logging(logging, logging.DEBUG)
        self.cm_futures_client.mark_price(f"{symbol}_PERP")
        logging.info()
