from datetime import datetime, timedelta
import json
import os
import unittest

import pytz

from eframe.models.event import Event
from eframe.services.calendar_api_service import CalendarApiService

from pathlib import Path
import eframe
from eframe.services.calendar_service import CalendarService


class TestCalendarService(unittest.TestCase):

    def test_2(self):
        print(Path(eframe.__file__).absolute())
        curr_path = os.path.dirname(__file__)

        print(os.path.join(curr_path, "..\..", "token.json"))
    def test_connection(self):
        with open("../token.json") as token:
            cal_service = CalendarService(token)
            list = cal_service.get_coming_events()
            for i in cal_service.json_to_event_list(list):
                print(i.start_datetime)
            self.assertTrue(list != [])

    def test_234(self):
        with open("../token.json") as token:
            cal_service = CalendarService(token)
            result = json.loads(json.dumps(cal_service.get_coming_events_list()["items"]))
            for i in result:
                if i["summary"] == "Fælles":
                    faelles = i["id"]
                if i["summary"] == "Gustav":
                    gustav = i["id"]
                if i["summary"] == "gustav.knudsen96@gmail.com":
                    gustav_mail = i["id"]
                if i["summary"] == "elisabethloefting@gmail.com":
                    elisabeth = i["id"]

        self.assertTrue(faelles)
        self.assertTrue(gustav)
        self.assertTrue(elisabeth)
        self.assertTrue(gustav_mail)

    def test_fsdfsd(self):
        cal_service = CalendarApiService()
        result = json.loads(json.dumps(cal_service.list_all_calendars()["items"]))
        faelles = None
        for i in result:
            if i["summary"] == "Fælles":
                faelles = i["id"]
        time1 = datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        time2 = (datetime.utcnow() + timedelta(days=60)).replace(tzinfo=pytz.UTC).isoformat()
        event_list = CalendarService(faelles).list_coming_events(time1, time2)
        for i in event_list:
            if 'dateTime' in i['start']:
                Event(i["summary"], i['start']['dateTime'])
            elif 'date' in i['start']:
                Event(i["summary"], i['start']['date'])

    def test_get_events(self):
        cal_service = CalendarApiService()
        cal_id = cal_service.get_cal_id_by_name("Fælles")
        service = CalendarService(cal_id)
        result = service.list_coming_events(
            datetime.utcnow(),
            (datetime.utcnow() + timedelta(days=60))
        )

        self.assertNotEquals(result, [])


