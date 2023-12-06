import pickle
import os.path
import string

import pytz
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import logging
from google.oauth2.credentials import Credentials
from pathlib import Path
from google.auth.transport.requests import Request

from eframe.models.event import Event
from eframe.services.google_api_credentials_service import GoogleApiCredentialsService

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class CalendarApiService:
    def __init__(self):
        self.service = GoogleApiCredentialsService.get_google_api_calendar_service()

    def get_cal_id_by_name(self, name: string):
        result = self.list_all_calendars()["items"]
        cal_id = None
        for i in result:
            if i["summary"] == name:
                cal_id = i["id"]
        return cal_id

    def list_all_calendars(self):
        return self.service.calendarList().list().execute()

    def list_coming_events(self, cal_id: int, time_min: string, time_max: string):
        return self.service.events().list(
            calendarId=cal_id, timeMin=time_min, timeMax=time_max, showDeleted=False,
            singleEvents=True, orderBy="startTime"
        ).execute()

    def get_coming_events(self):
        result = self.list_all_calendars()

        main_cal_id = result["items"][0]["id"]

        today = datetime.utcnow()
        today = today.replace(tzinfo=pytz.UTC).isoformat()

        later = datetime.utcnow() + timedelta(days=60)
        later = later.replace(tzinfo=pytz.UTC).isoformat()

        logging.debug("GET service.events.list comming")
        result = self.service.events().list(calendarId=main_cal_id, timeMin=today, timeMax=later, showDeleted=False,
                                       singleEvents=True, orderBy="startTime").execute()
        logging.debug("DONE service.events.list comming")

        comming_events = []
        for event in result['items']:
            comming_events.append(event)

        return comming_events

    def json_to_event_list(self, calender_json) -> [Event]:
        events = []
        for event in calender_json:
            summary = event['summary']
            if 'date' in event['start']:
                date = event['start']['date']
                start_date = datetime.strptime(date, '%Y-%m-%d')
            elif 'dateTime' in event['start']:
                date = event['start']['dateTime']
                thisDatetime = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
                start_date = thisDatetime
            thisEvent = Event(summary, start_date)
            events.append(thisEvent)
        return events


    def get_event_list(self, token):
        cal_json = self.get_coming_events(token)
        events_list = self.json_to_event_list(cal_json)
        return events_list
