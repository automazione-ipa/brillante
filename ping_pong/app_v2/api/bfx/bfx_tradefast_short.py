from fastapi import APIRouter, HTTPException
from app.logic.entities import BFXOrderRequest
from app.endpoints.bfx_a_client import get_bfx_client

# Create the router
router = APIRouter()

@router.post("/bfx_short")
def create_short_order(order_request: BFXOrderRequest):
    """
    Endpoint to create a short order on Bitfinex.
    """
    try:
        bfx = get_bfx_client()
        
        # Place a leveraged short order (amount is negative for shorts)
        response = bfx.rest.auth.submit_order(
            type="LIMIT", 
            symbol=order_request.pair,
            amount=str(-order_request.amount),  # Negative amount indicates short
            price=None,  # Market price
            lev=order_request.leverage
        )
        
        return {
            "status": "success",
            "order": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
