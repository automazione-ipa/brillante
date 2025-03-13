from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class Tweet(BaseModel):
    """Model representing a Tweet object."""
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    testo: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TopicRequest(BaseModel):
    """Model representing a TopicRequest. """
    topic: str

