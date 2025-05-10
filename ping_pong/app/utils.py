
import random
from flask import Request
from app.entities import OrderParams

# Bot logic
TRADE_PAIR = "BTC_USD"


def str_key_value(
        key:str,
        default: str,
        req: Request
    ) -> str:
    """General single value parser from string request parameter. """
    data: dict = req.get_json()
    return data.get(key, default)

def get_pair(req: Request):
    """Parser for the trading pair given by the user."""
    
    return str_key_value("trading_pair", default=TRADE_PAIR, req=req)

def get_order_id(req: Request):
    """Parser for the order_id given by the user."""
    
    return str_key_value("order_id", default=TRADE_PAIR, req=req)

def get_order_payload(req: Request) -> OrderParams:
    """Retrieves an OrderPayload from data."""

    data: dict = req.get_json()
    return OrderParams(
        trade_pair=data.get("trading_pair"),
        order_type=data.get("order_type"),
        side=data.get("side"),
        amount=data.get("amount"),
        price=data.get("price")
    )

# Random functions
def random_range(tpl_range, precision):
    return round(random.uniform(*tpl_range), precision)

def random_int(tpl_range):
    return random.randint(*tpl_range)

def price_rnd(mid_price):
    return round(mid_price * random_range((0.999, 1.001), 2))

# Mid-price calculation methods
def simple_mid_price(bids, asks) -> float:
    best_bid = bids[0][0]
    best_ask = asks[0][0]
    return round((best_bid + best_ask) / 2, 6)

def volume_weighted_mid_price(bids, asks):
    best_bid_price, best_bid_size = bids[0]
    best_ask_price, best_ask_size = asks[0]
    return ((best_bid_price * best_bid_size) + (best_ask_price * best_ask_size)) / (best_bid_size + best_ask_size)

def order_book_depth_mid_price(bids, asks, depth=3):
    total_bid_value = sum(price * size for price, size in bids[:depth])
    total_ask_value = sum(price * size for price, size in asks[:depth])
    total_bid_size = sum(size for _, size in bids[:depth])
    total_ask_size = sum(size for _, size in asks[:depth])
    return (total_bid_value + total_ask_value) / (total_bid_size + total_ask_size)
