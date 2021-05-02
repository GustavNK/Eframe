# Eframe

## Links

[Integrating Google Calendar API in Python Projects](https://www.youtube.com/watch?v=j1mh0or2CX8&t=317s)

[Get client secret](https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/credentials?authuser=1&project=first-242717&supportedpurview=project)

https://www.googleapis.com/auth/calendar.readonly

## Mine noter

Husk at RPIzw ikke kan fobinde til 5GHz WiFi. Stofas router er underlig så 2.4 virker ikke altid.

## Google Calendar Api

For at forbinde med Google oauth, se denne video [Integrating Google Calendar API in Python Projects](https://www.youtube.com/watch?v=j1mh0or2CX8&t=317s). 
* Hent client_secret fra [Google Cloud Platform](https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/credentials)
* Oversæt client secret til credentials, og gem i en token

```
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

scopes = ['https://www.googleapis.com/auth/calendar.readonly']

flow = InstalledAppFlow.from_client_secrets_file(("client_secret.json"), scopes=scopes)
credentials = flow.run_console()

pickle.dump(credentials, open("token.pkl", "wb"))
```

## Dependencies

* sudo apt-get update
* sudo apt-get install python3-pip
* sudo apt-get install python3-pil
* sudo apt-get install python3-numpy
* sudo pip3 install RPi.GPIO
* sudo pip3 install pytz
* sudo pip3 install google-api-python-client
* sudo pip3 install google_auth_oauthlib
