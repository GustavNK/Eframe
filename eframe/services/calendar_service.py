import string
from datetime import datetime

import pytz

from eframe.models.event import Event
from eframe.services.calendar_api_service import CalendarApiService


class CalendarService:
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        self.cal_api_service = CalendarApiService()

    def list_coming_events(self, time_min: datetime, time_max: datetime) -> [Event]:
        event_list_json = self.cal_api_service.list_coming_events(
            self.calendar_id,
            time_min.replace(tzinfo=pytz.UTC).isoformat(),
            time_max.replace(tzinfo=pytz.UTC).isoformat()
        )['items']
        events = []
        for i in event_list_json:
            if 'dateTime' in i['start']:
                events.append(Event(i["summary"], i['start']['dateTime']))
            elif 'date' in i['start']:
                events.append(Event(i["summary"], i['start']['date']))
        return events
