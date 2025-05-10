from math import fabs
import time

def current_ts():
    """Get the current timestamp in ms."""
    return round(time.time() * 1000)


# Statistical Utility
def calculate_apr(funding_bfx, funding_gmx, leverage):
    """
    Calculate the APR (Annualized Percentage Rate) based on funding rates and leverage.
    """
    diff = -(funding_bfx - fabs(funding_gmx))  # Funding differential
    apr = diff * leverage * 365  # Assuming daily funding rates
    return apr

# Bfx Strings
def get_bfx_basic_trading_pair(symbol):
    """
    Generates a trading pair string in the format 't<SYMBOL>USD'.
    
    :param symbol: str, the cryptocurrency symbol (e.g., "BNB", "ADA").
    :return: str, the formatted trading pair (e.g., "tBNBUSD").
    """
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string.")
    return f"t{symbol.upper()}USD"

def get_order_trading_pair(symbol, provider="bitfinex", test=False):
    """
    Converts a trading pair string in the format 't<SYMBOL>F0:USDTF0'.

    :param symbol: str, the cryptocurrency symbol (e.g., "BNB", "ADA").
    :return: str, the formatted trading pair (e.g., "tADAF0:USDTF0").
    """
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string.")
    
    # Bitfinex Trading Pair
    if provider == "bitfinex":
        if test:
            return f"tTEST{symbol}F0:TESTUSDTF0"
        return f"t{symbol}F0:USDTF0"
    # Binance Trading Pair
    elif provider == "binance" or provider=="bybit":  
        return f"{symbol}USDT"
    

# BiBit Strings
def get_usdt_address(data, chain_name):
    """Get USDT address from ByBit raw response data.
    
    :param chain_name: str, the chain symbol (e.g., "SOL", "TRON", "BNB", "ADA", ...).
    :return: str, the formatted address string (e.g., "yf9e0wsadn9e...").
    """
    try:
        chains = data.get("result", {}).get("chains", [])
        for chain in chains:
            if chain.get("chain") == chain_name:
                return chain.get("addressDeposit")
        return f"Indirizzo non trovato per la chain: {chain_name}"
    except Exception as e:
        return f"Errore: {str(e)}"
