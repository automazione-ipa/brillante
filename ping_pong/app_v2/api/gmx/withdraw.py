# withdraw.py
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
from app.logic.entities import (
    WithdrawRequest
)
from gmx_python_sdk.scripts.v2.order.create_withdrawal_order import (
    WithdrawOrder
)
from config_manager import (
    config_manager_dependency
)

# Create the router
router = APIRouter()

@router.post("/")
def create_withdraw_order(
        withdraw_request: WithdrawRequest,
        config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Endpoint to create a withdraw order on GMX.
    """
    try:
       
        withdraw_params = LiquidityArgumentParser(
            config, is_withdrawal=True
        ).process_parameters_dictionary(
            withdraw_request.dict(exclude={"debug_mode"})
        )

        withdraw_order = WithdrawOrder(
            config=config,
            market_key=withdraw_params["market_key"],
            out_token=withdraw_params["out_token_address"],
            gm_amount=withdraw_params["gm_amount"],
            debug_mode=withdraw_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": withdraw_params}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
