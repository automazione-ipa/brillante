from fastapi import FastAPI
from src.routers.generate_itinerary import router as itinerary_router

app = FastAPI(
    title="TravelForge Itinerary Service",
    version="0.1.0"
)

app.include_router(
    itinerary_router,
    prefix="/generate-itinerary"
)
