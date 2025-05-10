from fastapi import APIRouter, HTTPException
from bfxapi.types import Notification, Order
from app.logic.entities import (
    BFXOrderRequest,
    BFXOrderResponse
)
from app.endpoints.bfx_a_client import get_bfx_client

# Create the router
router = APIRouter()

@router.post("/bfx_order_submit")
def create_order(order_request: BFXOrderRequest):
    """
    General endpoint to create both long and short orders on Bitfinex.
    Long orders use positive amounts, short orders use negative amounts.
    """
    try:
        bfx = get_bfx_client()
        
        position_type = "long"
        if order_request.amount < 0:
            position_type = "short"

        # TODO : devo fare una serializzazione per differenziare i tipi ordini?
        submit_order_notification: Notification[Order]  = bfx.rest.auth.submit_order(
            type=order_request.order_type,
            symbol=order_request.symbol,
            amount=order_request.amount,
            price=order_request.price,
            lev=order_request.leverage
        )
        order: Order = submit_order_notification.data
        print("Submit order notification:", submit_order_notification)

        return BFXOrderResponse(
            id=order.id,
            gid=order.gid,
            cid=order.cid,
            symbol=order.symbol,
            mts_create=order.mts_create,
            mts_update=order.mts_update,
            amount=order.amount,
            amount_orig=order.amount_orig,
            order_type=order.order_type,
            position_type=position_type,
            type_prev=order.type_prev,
            mts_tif=order.mts_tif,
            flags=order.flags,
            order_status=order.order_status,
            price=order.price,
            price_avg=order.price_avg,
            price_trailing=order.price_trailing,
            price_aux_limit=order.price_aux_limit,
            notify=order.notify,
            hidden=order.hidden,
            placed_id=order.placed_id,
            routing=order.routing,
            meta=order.meta
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
