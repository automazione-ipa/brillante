from fastapi import APIRouter, HTTPException
from bfxapi.types import Notification, PositionClaim
from app.endpoints.bfx_a_client import get_bfx_client

# Create the router
router = APIRouter()

@router.post("/claim_positions")
def claim_all_positions():
    """
    Endpoint to claim all active positions on Bitfinex.
    """
    try:
        bfx = get_bfx_client()
        
        # Claims all active positions
        claimed_positions = []
        for position in bfx.rest.auth.get_positions():
            notification: Notification[PositionClaim] = bfx.rest.auth.claim_position(
                position.position_id
            )
            claim: PositionClaim = notification.data
            claimed_positions.append({
                "position": str(position),
                "claim": str(claim)
            })
            # TODO : rimuovi la stampa e processa meglio la risposta.
            print(f"Position: {position} | PositionClaim: {claim}")
        
        return {
            "status": "success",
            "claimed_positions": claimed_positions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

