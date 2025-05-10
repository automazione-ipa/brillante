# decrease.py
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
from gmx_python_sdk.scripts.v2.order.create_decrease_order import (
    DecreaseOrder
)
from app.logic.entities import (
    DecreaseRequest
)
from config_manager import (
    config_manager_dependency
)

# Create the router
router = APIRouter()

@router.post("/")
def create_decrease_order(
        decrease_request: DecreaseRequest,
        config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Endpoint to create a decrease order on GMX.
    """
    try:
        decrease_params = OrderArgumentParser(
            config, is_decrease=True
        ).process_parameters_dictionary(
            decrease_request.dict(exclude={"debug_mode"})
        )

        decrease_order = DecreaseOrder(
            config=config,
            market_key=decrease_params['market_key'],
            collateral_address=decrease_params['collateral_address'],
            index_token_address=decrease_params['index_token_address'],
            is_long=decrease_params['is_long'],
            size_delta=decrease_params['size_delta'],
            initial_collateral_delta_amount=decrease_params['initial_collateral_delta'],
            slippage_percent=decrease_params['slippage_percent'],
            swap_path=[],
            debug_mode=decrease_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": decrease_params}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
