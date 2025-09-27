from fastapi import APIRouter

from services import calendar_service
from config.logger import logger
from schemas.calendar_schema import EventRequest, EventResponse

calendar_router = APIRouter(prefix="/calendar", tags=["Calendar"])


@calendar_router.get("/auth")
async def authenticate():
    """
    Authenticate your Google account once.
    Opens browser for consent if needed.
    """
    try:
        message = calendar_service.authenticate_user()
        return {"message": message}
    except Exception as e:
        logger.exception(e)
        raise e


@calendar_router.post("/create_event", response_model=EventResponse)
async def create_event(request: EventRequest):
    """
    Create an event on your Google Calendar using your account.
    """
    try:
        event = calendar_service.create_event(
            summary=request.summary,
            start=request.start,
            end=request.end,
            attendees=request.attendees,
        )
        return EventResponse(event_link=event["event_link"], event_id=event["event_id"])
    except Exception as e:
        logger.exception(e)
        raise e
