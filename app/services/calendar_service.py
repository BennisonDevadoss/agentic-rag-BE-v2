import os
import datetime

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_FILE = "./creds/token.json"
CREDENTIALS_FILE = "./creds/token.json"


def authenticate_user() -> str:
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
        # return "Already authenticated"
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
        return "Authentication successful"


def get_calendar_service():
    """
    Loads saved token or refreshes it, returns Google Calendar service instance.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("User not authenticated. Call /v1/calendar/auth first.")

    service = build("calendar", "v3", credentials=creds)
    return service


def create_event(summary: str, start: str, end: str, attendees: list = None) -> dict:
    """
    Creates an event on the authenticated user's Google Calendar.
    """
    service = get_calendar_service()

    start_time = datetime.datetime.fromisoformat(start)
    end_time = datetime.datetime.fromisoformat(end)

    event = {
        "summary": summary,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    if attendees:
        event["attendees"] = [{"email": email} for email in attendees]

    created_event = (
        service.events()
        .insert(calendarId="primary", body=event, sendUpdates="all")
        .execute()
    )
    return {
        "event_link": created_event.get("htmlLink"),
        "event_id": created_event.get("id"),
    }


# uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib
