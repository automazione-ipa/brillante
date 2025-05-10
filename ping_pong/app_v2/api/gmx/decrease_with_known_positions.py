# decrease_with_known_positions.py
from decimal import Decimal
from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from gmx_python_sdk.scripts.v2.get.get_markets import Markets
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager,
    find_dictionary_by_key_value,
    get_tokens_address_dict,
    determine_swap_route
)
from gmx_python_sdk.scripts.v2.order.create_decrease_order import (
    DecreaseOrder
)
from app.logic.entities import (
    DecreaseWithKnownPosRequest
)
from app.endpoints import (
    get_positions
)
from config_manager import (
    config_manager_dependency
)

# Create the router
router = APIRouter()

def transform_open_position_to_order_parameters(
    config: ConfigManager,
    positions: dict,
    market_symbol: str,
    is_long: bool,
    slippage_percent: float,
    out_token,
    amount_of_position_to_close,
    amount_of_collateral_to_remove
):
    """
    Find the user defined trade from market_symbol and is_long in a dictionary
    positions and return a dictionary formatted correctly to close 100% of
    that trade.

    Parameters
    ----------
    chain : str
        arbitrum or avalanche.
    positions : dict
        dictionary containing all open positions.
    market_symbol : str
        symbol of market trader.
    is_long : bool
        True for long, False for short.
    slippage_percent : float
        slippage tolerance to close trade as a percentage.

    Raises
    ------
    Exception
        If we can't find the requested trade for the user.

    Returns
    -------
    dict
        order parameters formatted to close the position.

    """
    direction = "short"
    if is_long:
        direction = "long"

    position_dictionary_key = "{}_{}".format(
        market_symbol.upper(),
        direction
    )

    try:
        raw_position_data = positions[position_dictionary_key]
        gmx_tokens = get_tokens_address_dict(config.chain)

        collateral_address = find_dictionary_by_key_value(
            gmx_tokens,
            "symbol",
            raw_position_data['collateral_token']
        )["address"]

        gmx_tokens = get_tokens_address_dict(config.chain)

        index_address = find_dictionary_by_key_value(
            gmx_tokens,
            "symbol",
            raw_position_data['market_symbol'][0]
        )
        out_token_address = find_dictionary_by_key_value(
            gmx_tokens,
            "symbol",
            out_token
        )['address']
        markets = Markets(config=config).info

        swap_path = []

        if collateral_address != out_token_address:
            swap_path = determine_swap_route(
                markets,
                collateral_address,
                out_token_address
            )[0]
        size_delta = int(int(
            (Decimal(raw_position_data['position_size']) * (Decimal(10)**30))
        ) * amount_of_position_to_close)

        return {
            "chain": config.chain,
            "market_key": raw_position_data['market'],
            "collateral_address": collateral_address,
            "index_token_address": index_address["address"],
            "is_long": raw_position_data['is_long'],
            "size_delta": size_delta,
            "initial_collateral_delta": int(int(
                raw_position_data['inital_collateral_amount']
            ) * amount_of_collateral_to_remove
            ),
            "slippage_percent": slippage_percent,
            "swap_path": swap_path
        }
    except KeyError:
        raise Exception(
            "Couldn't find a {} {} for given user!".format(
                market_symbol, direction
            )
        )


@router.post("/")
def create_decrease_with_known_positions_order(
        decrease_pos_request: DecreaseWithKnownPosRequest,
        config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Endpoint to create a decrease order  with known positions on GMX.
    """
    try:
        positions = get_positions(config)

        decrease_pos_params = transform_open_position_to_order_parameters(
            config,
            # gets all open positions as a dictionary, which the keys as each position
            positions=positions,
            market_symbol=decrease_pos_request.market_symbol,
            is_long=decrease_pos_request.is_long,
            slippage_percent=decrease_pos_request.slippage_percent,
            out_token=decrease_pos_request.out_token,
            amount_of_position_to_close=decrease_pos_request.amount_of_position_to_close,
            amount_of_collateral_to_remove=decrease_pos_request.amount_of_collateral_to_remove
        )

        decrease_pos_order = DecreaseOrder(
            config=config,
            market_key=decrease_pos_params['market_key'],
            collateral_address=decrease_pos_params['collateral_address'],
            index_token_address=decrease_pos_params['index_token_address'],
            is_long=decrease_pos_params['is_long'],
            size_delta=decrease_pos_params['size_delta'],
            initial_collateral_delta_amount=(
                decrease_pos_params['initial_collateral_delta']
            ),
            slippage_percent=decrease_pos_params['slippage_percent'],
            swap_path=decrease_pos_params['swap_path'],
            debug_mode=decrease_pos_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": decrease_pos_params}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
