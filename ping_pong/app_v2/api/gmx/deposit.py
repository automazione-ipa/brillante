# deposit.py
from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from gmx_python_sdk.scripts.v2.order.liquidity_argument_parser import (
    LiquidityArgumentParser
)
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager
)
from gmx_python_sdk.scripts.v2.order.create_deposit_order import (
    DepositOrder
)
from app.logic.entities import (
    DepositRequest
)
from config_manager import (
    config_manager_dependency
)

# Create the router
router = APIRouter()

@router.post("/")
def create_deposit_order(
        deposit_request: DepositRequest,
        config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Endpoint to create a deposit order on GMX.
    """
    try:
        deposit_params = LiquidityArgumentParser(
            config, is_deposit=True
        ).process_parameters_dictionary(
            deposit_request.dict(exclude={"debug_mode"})
        )

        deposit_order = DepositOrder(
            config,
            market_key=deposit_params["market_key"],
            initial_long_token=deposit_params["long_token_address"],
            initial_short_token=deposit_params["short_token_address"],
            long_token_amount=deposit_params["long_token_amount"],
            short_token_amount=deposit_params["short_token_amount"],
            debug_mode=deposit_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": deposit_params}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
