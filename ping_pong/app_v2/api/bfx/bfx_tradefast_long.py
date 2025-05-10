from fastapi import APIRouter, HTTPException
from app.logic.entities import BFXOrderRequest
from app.endpoints.bfx_a_client import get_bfx_client

# Create the router
router = APIRouter()

@router.post("/bfx_long")
def create_long_order(order_request: BFXOrderRequest):
    """
    Endpoint to create a long order on Bitfinex.
    """
    try:
        bfx = get_bfx_client()
        
        # Place a leveraged long order
        response = bfx.rest.auth.submit_order(
            type="LIMIT", 
            symbol=order_request.symbol,
            amount=str(order_request.amount), 
            price=None,  # Market price
            lev=order_request.leverage
        )
        
        return {
            "status": "success",
            "order": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
