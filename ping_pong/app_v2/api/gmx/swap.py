# swap.py
from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from gmx_python_sdk.scripts.v2.order.order_argument_parser import (
    OrderArgumentParser
)
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager
)
from gmx_python_sdk.scripts.v2.order.create_swap_order import (
    SwapOrder
)
from app.logic.entities import (
    SwapRequest
)
from config_manager import (
    config_manager_dependency
)
# Create the router
router = APIRouter()

@router.post("/")
def create_swap_order(
        swap_request: SwapRequest,
        config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Endpoint to create a swap order on GMX.
    """
    try:
        swap_order_parameters = OrderArgumentParser(
            config, is_swap=True
        ).process_parameters_dictionary(
            swap_request.dict(exclude={"debug_mode"})
        )

        swap_order = SwapOrder(
            config=config,
            market_key=swap_order_parameters['swap_path'][-1],
            start_token=swap_order_parameters['start_token_address'],
            out_token=swap_order_parameters['out_token_address'],
            collateral_address=swap_order_parameters['start_token_address'],
            index_token_address=swap_order_parameters['out_token_address'],
            is_long=False,
            size_delta=0,
            initial_collateral_delta_amount=(
                swap_order_parameters['initial_collateral_delta']
            ),
            slippage_percent=swap_order_parameters['slippage_percent'],
            swap_path=swap_order_parameters['swap_path'],
            debug_mode=swap_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": swap_order_parameters}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
