# entities.py
from typing import Any, Dict, Optional
from pydantic import BaseModel

class BaseOrderRequest(BaseModel):
    symbol: str = "BTCUSD"
    amount: float = 10.0
    leverage: float = 1.0
    price: Optional[float] = None  # Optional, for LIMIT orders

class BNBOrderRequest(BaseOrderRequest):
    type: str = "MARKET"

class BFXOrderRequest(BaseOrderRequest):
    """
    Known values for symbol: "tBTCUSD", "tETHUSD", "tLTCBTC", 
    "tXRPUSD", "tEOSUSD", "tBCHUSD", "tNEOUSD", 
    "tXLMUSD", "tIOTAUSD", "tTRXUSD". 

    Known values for order_type: 
    "LIMIT", "EXCHANGE LIMIT", "MARKET", "EXCHANGE MARKET", "STOP", "EXCHANGE STOP",
    "STOP LIMIT", "EXCHANGE STOP LIMIT", "TRAILING STOP", "EXCHANGE TRAILING STOP",
    "FOK", "EXCHANGE FOK", "IOC", "EXCHANGE IOC"
    """
    order_type: str = "LIMIT"

# BITFINEX ENTITIES

class BFXOrderID(BaseModel):
    id: str

class BFXOrderUpdate(BFXOrderID):
    amount: float
    price: int

class BFXOrderDelete(BFXOrderID):
    ...

class BFXOrderResponse(BaseModel):
    id: int
    gid: int
    cid: int
    symbol: str
    mts_create: int
    mts_update: int
    amount: float
    amount_orig: float
    order_type: str
    position_type: str
    type_prev: str
    mts_tif: int
    flags: int
    order_status: str
    price: float
    price_avg: float
    price_trailing: float
    price_aux_limit: float
    notify: int
    hidden: int
    placed_id: int
    routing: str
    meta: Dict[str, Any]

class BFXCollateralRequest(BaseModel):
    type: str = "LIMIT"
    symbol: str
    amount: str
    price: str
    lev: int

class BFXCollateralResponse(BaseModel):
    ...

# GMX Entities
class Chain(BaseModel):
    chain: str

class GMXTxRequest(Chain):
    address: Optional[str] = None

class GMXConfig(Chain):
    debug_mode: bool = True

class GMXLiqRequest(Chain):
    liq_info: Optional[str] = "AAVE_long"
    address: Optional[str] = None

# Withdraw and Deposit Request
class GMXWithdrawRequest(GMXConfig):
    market_token_symbol: str = "ETH"
    out_token_symbol: str = "USDC"
    gm_amount: int = 3

class GMXDepositRequest(GMXConfig):
    market_token_symbol: str = "ETH"
    long_token_symbol: str = "ETH"
    short_token_symbol: str = "USDC"
    long_token_usd: int = 5
    short_token_usd: int = 0

# Swap Request
class BasicOrder(BaseModel):
    # is_long: True for long, False for short.
    is_long: bool
    # slippage_percent: As a decimal ie 0.003 == 0.3%
    slippage_percent: float

# Swap Request
class GMXDeltaParams(GMXConfig):
    is_long: bool
    """True for Long Orders, False for Short."""
    slippage_percent: float
    """As a decimal ie 0.003 == 0.3%"""
    size_delta_usd: int
    """Position size in USD."""

class GMXSwapRequest(GMXDeltaParams):
    out_token_symbol: str
    start_token_symbol: str
    initial_collateral_delta: float

# Increase and Decrease
class GMXDeltaRequest(GMXDeltaParams):
    """Class mapping common fields for Increase and Decrease Requests"""
    index_token_symbol: str
    """The market you want to trade on."""
    collateral_token_symbol: str
    """The token to use as collateral. Start token swaps into collateral token if different."""
    
    
class GMXDecreaseRequest(GMXDeltaRequest):
    initial_collateral_delta: Optional[float] = None
    """Collateral delta in principal (not USD). """

class GMXIncreaseRequest(GMXDeltaRequest):
    start_token_symbol: Optional[str] = None
    """The token to start with - WETH not supported yet."""
    leverage: Optional[float] = None
    """If passed, will calculate number of tokens in start_token_symbol amount."""

# Decrease Request, using Known Positions
class GMXDecreaseWithKnownPosRequest(GMXConfig,BasicOrder):
    market_symbol: str
    out_token: str
    amount_of_position_to_close: int
    amount_of_collateral_to_remove: int

# Find Farming Opportunities Request
class GMXFarmingParams(GMXConfig):
    slippage_percent: float
    """As a decimal ie 0.003 == 0.3%"""
    size_delta_usd: int
    """Position size in USD."""
    is_delta_neutral: bool = True
    size_delta: int = 10
    net_rate_threshold: int = 0
    leverage: Optional[float] = 1
    """If passed, will calculate number of tokens in start_token_symbol amount."""

class GMXFarmingRequest(GMXFarmingParams):
    index_token_symbol: str
    """The market you want to trade on."""
    collateral_token_symbol: str
    """The token to use as collateral. Start token swaps into collateral token if different."""
    start_token_symbol: Optional[str] = None
    """The token to start with - WETH not supported yet."""
    ignore_oi_imbalance: bool = True
    """oi_imbalances"""
