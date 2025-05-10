from fastapi import APIRouter, HTTPException
from bfxapi.types import Notification, Order
from app.logic.entities import (
    BFXOrderUpdate
)
from app.endpoints.bfx_a_client import get_bfx_client

# Create the router
router = APIRouter()

@router.post("/bfx_order_update")
def update_order(order_request: BFXOrderUpdate):
    """
    General endpoint to create both long and short orders on Bitfinex.
    Long orders use positive amounts, short orders use negative amounts.
    """
    try:
        bfx = get_bfx_client()
        

        update_order_notification: Notification[Order] = bfx.rest.auth.update_order(
            id=order_request.id,
            amount=order_request.amount,
            price=order_request.price
        )
        data: Order = update_order_notification.data
        print("Update order notification:", update_order_notification)

        return {
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
