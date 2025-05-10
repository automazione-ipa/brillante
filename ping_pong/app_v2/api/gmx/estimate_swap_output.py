# get_positions.py
from fastapi import (
    Depends,
    APIRouter,
    HTTPException
)
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager
)
from app.logic.entities import (
    TxRequest
)
from config_manager import (
    config_manager_dependency
)
from app.endpoints import (
    get_positions
)

router = APIRouter()

@router.post("/")
def estimate_swap_output(
    request: TxRequest,
    config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Endpoint to estimate the swap output, given amount, token_in_symbol and token_out_symbol.
    """
    try:
        positions = get_positions(config=config, address=request.address)
        return {"positions": positions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
