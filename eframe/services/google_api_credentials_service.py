import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class GoogleApiCredentialsService:
    @staticmethod
    def get_credentials() -> Credentials:
        curr_path = os.path.dirname(__file__)
        token_abs_path = os.path.join(curr_path, "../..", "token.json")
        creds = Credentials.from_authorized_user_file(token_abs_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        return creds

    @staticmethod
    def get_google_api_calendar_service():
        service = build("calendar", "v3", credentials=GoogleApiCredentialsService.get_credentials())
        return service
