from pybit.exceptions import InvalidRequestError
from pybit.unified_trading import HTTP
import uuid

from app_v2.utils.statistics import get_list_timestamp


class ApiCallByBit:
    def __init__(self, api_key, secret_key):
        self.session_v2 = HTTP(
            testnet=False,
            api_key=api_key,
            api_secret=secret_key,
        )

    # OK
    def check_correct_key_v2(self):
        try:
            res = self.session_v2.get_account_info()
            return res, True
        except BaseException as x:
            return x, False

    # OK
    def get_wallet_balance_unified_v2(self):
        res = self.session_v2.get_wallet_balance(
            accountType="UNIFIED")
        return res

    # OK
    def get_wallet_balance_unified_by_coin_v2(self, coin):
        res = self.session_v2.get_wallet_balance(
            accountType="UNIFIED", coin=coin)
        return res

    # OK
    def get_wallet_balance_fund_v2(self):
        res = self.session_v2.get_coins_balance(
            accountType="FUND", coin="USDT")
        return res
    
    # OK
    def get_wallet_balance_fund_by_coin_v2(self, coin):
        res = self.session_v2.get_coins_balance(
            accountType="FUND", coin=coin)
        return res

    # OK
    def transfer_from_fund_to_unified_v2(self, qty):
        myuuid = uuid.uuid4()
        try:
            res = self.session_v2.create_internal_transfer(
                transferId=str(myuuid),
                coin="USDT",
                amount=str(round(qty, 2)),
                fromAccountType="FUND",
                toAccountType="UNIFIED",
            )
        except BaseException as e:
            print(e)

    # OK
    def place_order_v2(self, qty, symbol, category, side, marketUnit="baseCoin"):
        res = self.session_v2.place_order(
            category=category,
            symbol=symbol,
            side=side,
            orderType="Market",
            marketUnit=marketUnit,
            qty=str(qty),
            isLeverage=0,
        )
        return res

    # OK
    def close_short_order_v2(self, symbol, category, side):
        res = self.session_v2.place_order(
            symbol=symbol,
            reduceOnly=True,
            closeOnTrigger=True,
            orderType="Market",
            qty="0",
            category=category,
            side=side
        )
        return res

    # OK
    def get_last_price_v2(self):
        return self.session_v2.get_tickers(
            category="spot",
            symbol="STETHUSDT",
        )

    def price_ticker(self, symbol: str, category: str = "spot"):
        return self.session_v2.get_tickers(
            category=category, symbol=symbol,
        )
    
    # OK
    def get_info_account_v2(self):
        try:
            return [self.session_v2.get_api_key_information(), True]
        except InvalidRequestError as e:
            return [e, False]
        
    # OK
    def get_info_UTA_account_v2(self):
        try:
            return [self.session_v2.get_account_info(), True]
        except InvalidRequestError as e:
            return [e, False]

    # FOR RENDERING FRONTEND
    def get_old_funding(self, start):
        lst_date = get_list_timestamp(start)
        # tipo -> lst_date = [1712419200000,1712419200000,1712419200000]
        list_res = []
        for data in lst_date:
            api_res = self.session_v2.get_executions(
                category="linear",
                limit=100,
                execType="Funding",
                startTime=data,
                # endTime=1713802774365
            )
            for res in api_res['result']['list']:
                list_res.append({"Time": int(res['execTime']),
                                 "Symbol": res['symbol'],
                                 "Quantity": res['execQty'],
                                 "execPrice": res['execPrice'],
                                 "execValue": res['execValue'],
                                 "FeeRate": res['feeRate'],
                                 "Funding": -float(res['execFee']),
                                 })
        res = []
        [res.append(x) for x in list_res if x not in res]
        return res

    def get_steth_quantity(self):
        res = self.session_v2.get_wallet_balance(
            accountType="UNIFIED", coin="STETH")['result']['list'][0]['coin'][0]['walletBalance']
        return res

    def get_wallet_balance_v2(self):
        res = self.session_v2.get_wallet_balance(
            accountType="UNIFIED")
        return res
    
    def set_position_mode_to_one_way_v2(self, coin):
        res = self.session_v2.switch_position_mode(
            category="linear", # linear, USDT Perp; inverse, Inverse Futures
            symbol=coin,
            mode=0)
        return res

    @staticmethod
    def set_collateral_v3(coin, api_key, secret_key):
        import requests
        import time
        import hashlib
        import hmac
        import json

        url = "https://api.bybit.com/v5/account/set-collateral-switch"

        # Dati per la richiesta
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        body = {
            "coin": coin,
            "collateralSwitch": "ON"
        }

        # Conversione del corpo in stringa JSON
        raw_request_body = json.dumps(body)

        # Creazione della stringa per la firma
        param_str = f'{timestamp}{api_key}{recv_window}{raw_request_body}'

        # Generazione della firma usando HMAC-SHA256
        signature = hmac.new(secret_key.encode(), param_str.encode(), hashlib.sha256).hexdigest()

        # Costruzione dell'header
        headers = {
            "X-BAPI-SIGN": signature,
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "Content-Type": "application/json"
        }

        # Invio della richiesta POST
        response = requests.post(url, headers=headers, data=raw_request_body)

        return response.json()
