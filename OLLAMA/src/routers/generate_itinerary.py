from fastapi import APIRouter, HTTPException
import logging

from travel_forge_v1.entities import ItineraryRequest
from src.routers.itinerary_service import ItineraryService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=dict)
async def generate_itinerary(request: ItineraryRequest):
    try:
        service = ItineraryService()
        markdown = await service.create_itinerary(request)
        return {"markdown_report": markdown}
    except Exception as e:
        logger.error("Error generating itinerary: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
