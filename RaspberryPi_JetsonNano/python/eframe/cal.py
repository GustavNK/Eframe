import pickle
import os.path
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import time

class Event():
    def __init__(self, summary, start_datetime):
        self.summary = summary
        self.start_datetime = start_datetime

    def __eq__(self, other):
        summary = self.summary == other.summary
        date = self.start_datetime == other.start_datetime
        return (summary or date)



def getGoogleCalendarJson(token):
    if(not os.path.exists("token.pkl")):
        exit()

    credentials = pickle.load(open("token.pkl", "rb"))

    service = build("calendar", "v3", credentials=credentials)

    result = service.calendarList().list().execute()

    main_cal_id = result["items"][0]["id"]

    today = datetime.utcnow()
    today = today.replace(tzinfo=pytz.UTC).isoformat()

    later = datetime.utcnow() + timedelta(days=60)
    later = later.replace(tzinfo=pytz.UTC).isoformat()

    result = service.events().list(calendarId=main_cal_id, timeMin=today, timeMax=later, showDeleted=False, singleEvents=True, orderBy="startTime").execute()

    comming_events = []
    for event in result['items']:
        comming_events.append(event)

    return comming_events

def jsonToEventList(calender_json):
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

def getEventList(token):
    cal_json = getGoogleCalendarJson(token)
    events_list = jsonToEventList(cal_json)
    return events_list
