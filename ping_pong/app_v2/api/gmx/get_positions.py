# get_positions.py
from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from gmx_python_sdk.scripts.v2.get.get_open_positions import (
    GetOpenPositions
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

router = APIRouter()

# TODO : analyze how to use and customize this function from the get_data() positions 
def get_positions(config: ConfigManager, address: str = None):
    """
    Get open positions for an address on a given network.
    If address is not passed it will take the address from the users config
    file.

    Parameters
    ----------
    chain : str
        arbitrum or avalanche.
    address : str, optional
        address to fetch open positions for. The default is None.

    Returns
    -------
    positions : dict
        dictionary containing all open positions.

    """

    if address is None:
        address = config.user_wallet_address
        if address is None:
            raise Exception("No address passed in function or config!")

    if config.chain == 'arbitrum':
        positions = GetOpenPositions(config=config, address=address).get_data()
    else:
        positions = GetOpenPositions(config=config, address=address).get_raw_data()

    return positions

@router.post("/")
def fetch_positions(
    get_pos_request: TxRequest,
    config: ConfigManager = Depends(config_manager_dependency)
    ):
    """
    Fetch positions using the provided address.

    Parameters: {"chain": "arbitrum", "address":"0x03r2"}

    Returns a dictionary containing all open positions.
    """
    try:
        positions = get_positions(config, get_pos_request.address)
        
        return {"positions": positions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
