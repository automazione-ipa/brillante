# increase.py
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
from gmx_python_sdk.scripts.v2.order.create_increase_order import (
    IncreaseOrder
)
from app.logic.entities import (
    IncreaseRequest
)
from config_manager import (
    config_manager_dependency
)

# Create the router
router = APIRouter()

@router.post("/")
def create_increase_order(
        increase_request: IncreaseRequest,
        config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Endpoint to create an increase order on GMX.
    """
    try:
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
