from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field


class EventRequest(BaseModel):
    summary: str
    start: datetime
    end: datetime | None  # NOTE: end is not used.
    timezone: str | None = Field(default="Asia/Kolkata")
    attendees: list[str] | None = None
    description: str | None = None
    location: str | None = None


class EventResponse(BaseModel):
    event_id: str
    meet_link: HttpUrl | None = None
    event_link: HttpUrl
