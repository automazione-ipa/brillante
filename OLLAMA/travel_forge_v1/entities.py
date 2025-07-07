from pydantic import BaseModel
from typing import Optional


class SeasonDates(BaseModel):
    season: str
    from_date: Optional[str]
    to_date: Optional[str]


class ItineraryRequest(BaseModel):
    city_country: str
    duration_days: int
    season_or_dates: SeasonDates
