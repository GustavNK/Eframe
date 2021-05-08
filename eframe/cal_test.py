from datetime import datetime, timedelta
import pickle
import os.path
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

print(comming_events)