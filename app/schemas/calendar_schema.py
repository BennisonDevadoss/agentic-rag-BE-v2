from pydantic import BaseModel
from typing import List, Optional


class EventRequest(BaseModel):
    summary: str
    start: str  # ISO format: "2025-09-29T10:00:00"
    end: str  # ISO format: "2025-09-29T11:00:00"
    attendees: Optional[List[str]] = None


class EventResponse(BaseModel):
    event_link: str
    event_id: str
