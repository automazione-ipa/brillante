from pydantic import BaseModel

class BFXOrderRequest(BaseModel):
    type: str = "LIMIT"
    symbol: str
    amount: float
    price: float = None  # Market price
    lev: int

def construct_trade_message(symbol, amount, leverage):
    """
    Construct a trade message for Bitfinex and GMX.
    """
    return BFXOrderRequest(
        type="MARKET",
        symbol=symbol,
        amount=amount,
        lev=leverage
    )
