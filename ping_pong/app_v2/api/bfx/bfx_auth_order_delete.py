from fastapi import APIRouter, HTTPException
from bfxapi.types import Notification, Order
from app.logic.entities import BFXOrderDelete
from app.endpoints.bfx_a_client import get_bfx_client

# Create the router
router = APIRouter()

@router.post("/bfx_order_delete")
def delete_order(order_request: BFXOrderDelete):
    """
    General endpoint to create both long and short orders on Bitfinex.
    Long orders use positive amounts, short orders use negative amounts.
    """
    try:
        bfx = get_bfx_client()
        
        cancel_order_notification: Notification[Order] = bfx.rest.auth.cancel_order(
            id=order_request.id
        )
        data: Order = cancel_order_notification.data

        print("Cancel order notification:", cancel_order_notification)
        
        return {
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
