from math import fabs
from typing import Literal, Optional
import requests
import logging
from binance.cm_futures import CMFutures
from binance.lib.utils import config_logging

# Bitfinex Api
from bfxapi import Client

# Gmx Api
from gmx_python_sdk.scripts.v2.gmx_utils import ConfigManager
from gmx_python_sdk.scripts.v2.order.order_argument_parser import (
    OrderArgumentParser
)
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager
)
from gmx_python_sdk.scripts.v2.order.create_increase_order import (
    IncreaseOrder
)
from logic.entities import (
    # GMX ENTITIES
    IncreaseRequest,
    # BITFINEX ENTITIES
    BFXOrder,
    # BINANCE ENTITIES
    BNBOrder
)

from binance.error import ClientError as BinanceClientError
from binance.api import API

LIMIT = "LIMIT"
MARKET = "MARKET"

BNB_FUTURES = 'https://fapi.binance.com'
BNB_TESTNET = 'https://testnet.binancefuture.com'
BNB_LEV = "/fapi/v1/leverage"
BNB_ORD = "/fapi/v1/order"

BNB_API_KEY=os.getenv("BNB_API_KEY"),
BNB_API_SECRET=os.getenv("BNB_API_SECRET"),

# Soon - Literal and Dictionaries
bfx_simboli: Literal[
    "tBTCUSD", "tETHUSD", "tLTCBTC", "tXRPUSD", "tEOSUSD", "tBCHUSD", "tNEOUSD", "tXLMUSD", "tIOTAUSD", "tTRXUSD"
]

def bnb_api(base_url: str):
    # Initialize API instance
    return API(
        api_key=BINANCE_TEST_KEY,
        api_secret=BINANCE_TEST_SECRET,
        base_url=base_url
    )

def bnb_set_leverage(
        endpoint: str,
        api: API,
        symbol: str,
        lev: float
    ):
    """
    Set leverage for a symbol in Binance Futures.
    """
    payload = {"symbol": symbol, "leverage": lev}
    try:
        response = api.sign_request("POST", endpoint, payload)
        print("Leverage set successfully:", response)
    except BinanceClientError as e:
        print(f"Failed to set leverage: {e}")

def bnb_place_order(
        endpoint: str,
        api: API,
        bnb_request: BNBOrder,
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
        response = api.sign_request("POST", endpoint, payload)
        print("Order placed successfully:", response)
        return response
    except BinanceClientError as e:
        print(f"Failed to place order: {e}")

def bnb_funding(symbol):
    config_logging(logging, logging.DEBUG)
    cm_futures_client = CMFutures()
    cm_futures_client.mark_price("BTCUSD_PERP")
    logging.info()

def bnb_get_perp_price(
        endpoint: str,
        api: API,
        bnb_request: BNBOrder,
        short: Optional[bool] = False
    ):
    """
    Get the price for long or short PERP of a symbol in Binance Futures.
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
        response = api.sign_request("POST", endpoint, payload)
        print("Order placed successfully:", response)
        return response
    except BinanceClientError as e:
        print(f"Failed to place order: {e}")


# GMX
def get_config_manager(
        chain: str
    ) -> ConfigManager:
    """
    Returns a configured instance of ConfigManager based on the provided chain.

    :param chain: The blockchain chain name to be used for configuration.
    :return: An instance of ConfigManager.
    """
    config_manager = ConfigManager(chain=chain)
    config_manager.set_config(filepath="config.yaml")
    return config_manager


def gmx_submit_order(increase_request: IncreaseRequest):
    chain = "arbitrum"
    config = get_config_manager(chain=chain)
    increase_order_params = OrderArgumentParser(
            config, is_increase=True
        ).process_parameters_dictionary(
            increase_request.dict(exclude={"debug_mode"})
        )

    increase_order = IncreaseOrder(
        config=config,
        market_key=increase_order_params['market_key'],
        collateral_address=increase_order_params['start_token_address'],
        index_token_address=increase_order_params['index_token_address'],
        is_long=increase_order_params['is_long'],
        size_delta=increase_order_params['size_delta'],
        initial_collateral_delta_amount=(
            increase_order_params['initial_collateral_delta']
        ),
        slippage_percent=increase_order_params['slippage_percent'],
        swap_path=increase_order_params['swap_path'],
        debug_mode=increase_request.debug_mode
    )

    # In debug mode, you might not want to execute the order but just see the parameters.
    return {"status": "success", "order_details": increase_order_params}

# BITFINEX
def get_bfx_client():
    """
    Returns a pre-configured Bitfinex Client instance.
    """
    return Client(
        api_key=os.getenv("BFX_API_KEY"),
        api_secret= os.getenv("BFX_SECRET"),
    )

def fetch_best_trading_pair():
    """
    Mocked function to fetch the best trading pair for farming funding rates.
    Replace this logic with a real API call to your backend for production.
    """
    # Mocking the best trading pair
    print("Fetching the best trading pair to farm funding rates...")
    return "ADA"

def get_price(ticker):
    url = f"https://api-pub.bitfinex.com/v2/ticker/{ticker}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    print(type(data))
    print(f"Ticker: {ticker}  Data: {data}")

    return data


def get_funding(ticker):
    url = "https://api-pub.bitfinex.com/v2/status/deriv?keys=tBTCF0%3AUSTF0%2CtETHF0%3AUSTF0"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    print(type(data))
    print(f"FUNDING RATES: {ticker}  Data: {data}")

    return data

def calculate_apr(funding_bfx, funding_gmx, leverage):
    """
    Calculate the APR (Annualized Percentage Rate) based on funding rates and leverage.
    """
    diff = -(funding_bfx - fabs(funding_gmx))  # Funding differential
    apr = diff * leverage * 365  # Assuming daily funding rates
    return apr

def bfx_submit_limit_order(
        request: BFXOrder,
        short: Optional[bool] = False
    ):
    """
    Place a long order with leverage on Bitfinex.
    """
    print(f"\n\nPlacing a long order on Bitfinex: symbol={request.symbol}, amount={request.amount}, leverage={request.leverage}, price={request.price}")
    try:
        bfx = get_bfx_client()
        short_desc = "Long"
        amount = request.amount
        if short is True:
            short_desc = "Short"
            amount = - amount
        
        # Place a leveraged long order
        response = bfx.rest.auth.submit_order(
            type=request.order_type,
            symbol=request.symbol,
            amount=str(amount),
            price=request.price,
            lev=request.leverage
        )
        if response.status == "SUCCESS":
            print(f"\n\n{short_desc} order placed successfully:", response.data)
            return True
        else:
            print("Error placing long order:", response.status)
            return False
    except Exception as e:
        print("Exception while placing long order:", str(e))
        return False

def get_bfx_basic_trading_pair(symbol):
    """
    Generates a trading pair string in the format 't<SYMBOL>USD'.
    
    :param symbol: str, the cryptocurrency symbol (e.g., "BNB", "ADA").
    :return: str, the formatted trading pair (e.g., "tBNBUSD").
    """
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string.")
    return f"t{symbol.upper()}USD"


def get_order_trading_pair(symbol, provider="bfx", test=False):
    """
    Converts a trading pair string in the format 't<SYMBOL>F0:USDTF0'.

    :param symbol: str, the cryptocurrency symbol (e.g., "BNB", "ADA").
    :return: str, the formatted trading pair (e.g., "tADAF0:USDTF0").
    """
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string.")
    
    # Bitfinex Trading Pair
    if provider == "bfx":
        if test:
            return f"tTEST{symbol}F0:TESTUSDTF0"
        return f"t{symbol}F0:USDTF0"
    # Binance Trading Pair
    elif provider == "binance":  
        return f"{symbol}USDT"

def execute_strategy():
    """
    Execute the trading strategy by fetching the best trading pair, calculating profitability,
    and placing long and short orders if profitable.
    """
    # Minimum APR threshold for profitability (percentage)
    USER_DOLLAR_AMOUNT = 1000 # DOLLAR_USER
    print(f"\nUSER AMOUNT: {USER_DOLLAR_AMOUNT}$")
    LEVERAGE = 5
    print(f"\nLEVERAGE: {LEVERAGE}$")
    APR_THRESHOLD = 5 
    
    # Step 1: Fetch Best Trading Pairs
    symbol = fetch_best_trading_pair() # "ADA"
    print(f"\n\nSelected Best Trading Pair: {symbol}")
    
    # Step 2: Fetch Pair Trading Price
    trading_pair = get_bfx_basic_trading_pair(symbol)
    price = get_price(trading_pair)[0]
    print(f"\n\nTrading Pair Price: {price} , {type(price)}")

    amount_exchange = USER_DOLLAR_AMOUNT/2
    qty_order_bfx = int(amount_exchange/price)
    print(f"\n\nBFX ORDER QTY (round): {qty_order_bfx} of {symbol}")

    # Step 3: Define Funding Rates
    bxf_fund = get_funding(trading_pair)[0][12]
    print(f"\n\nFunding rate data: {bxf_fund}")
    funding_bfx = 0.02  # Mock funding rate for Bitfinex (positive means paying funding)
    funding_gmx = -0.10  # Mock funding rate for GMX (negative means receiving funding)

    # Step 4: Calculate the APR
    apr = APR_THRESHOLD + 1
    calculated_apr = calculate_apr(
        funding_bfx, funding_gmx, LEVERAGE
    )
    print(f"\n\nEstimated Desired APR (annualized): {calculated_apr:.2f}%")
    
    print(f"\n\nCalculated APR (annualized): {apr:.2f}%")

    # Step 5: Build Order Messages
    # Step 5.1 : BFX Order
    bfx_symbol = get_order_trading_pair(symbol,"bfx",test=True)
    bfx_long = {
        "symbol": bfx_symbol,
        "amount": amount_exchange,
        "leverage": LEVERAGE,
        "order_type": LIMIT,
        "price": price,
    }

    bfx_long_request = BFXOrder(**bfx_long)
    print("Price: ", bfx_long_request.price)
    # Step 5.2 : BINANCE Order
    bnb_symbol = get_order_trading_pair(symbol,"binance")
    conf_short = {
        "symbol": bnb_symbol,
        "amount": qty_order_bfx, # quantity
        "leverage": LEVERAGE,
        "type": LIMIT,
        "price": price,
    }
    bnb_short_request = BNBOrder(**conf_short)

    # Step 6: Check Profitability & Place Orders
    if apr > APR_THRESHOLD:
        bnbapi = bnb_api(BNB_TESTNET)

        print("\n\nStrategy is profitable. Proceeding with order placement...")
        # Bitfinex Long
        success_bfx_long = bfx_submit_limit_order(bfx_long_request, short=False)
        # Binance Short
        bnb_set_leverage(BNB_LEV, bnbapi, bnb_symbol, LEVERAGE)
        success_bnb_short = bnb_place_order( BNB_ORD, bnbapi, bnb_short_request, short=True)

        # Final status
        if success_bfx_long and success_bnb_short: 
            print("\n\nBoth orders placed successfully.")
        else:
            print("\n\nError in placing one or both orders.")
    else:
        print(f"\n\nStrategy is not profitable: APR = {apr:.2f}%")
        # ALTERNATIVE PIPELINE EXAMPLES
        # BITFINEX SHORT - Place Short Order on Bitfinex
        # success_bfx_short = bfx_submit_limit_order(bfx_short_request, short=True)
        # GMX SHORT - Place Short Order on GNX
        # success_gmx = gmx_short_leverage(symbol, amount, leverage)


# Main Execution
if __name__ == "__main__":
    execute_strategy()
