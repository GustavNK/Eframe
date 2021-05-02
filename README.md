# Eframe

This project is inspirede by demo code provided by [WaveShare](https://github.com/waveshare/e-Paper)

Using the WaveShare e-Paper 4.2 inch, show the current date, along upcomming calendar events and Trello List

## Links

[4.2 inch e-papar Module Wiki](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module)

[WaveShare git](https://github.com/waveshare/e-Paper)

[Integrating Google Calendar API in Python Projects](https://www.youtube.com/watch?v=j1mh0or2CX8&t=317s)

[Get client secret](https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/credentials?authuser=1&project=first-242717&supportedpurview=project)

[Trello API](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/)

## Mine noter

Husk at RPIzw ikke kan fobinde til 5GHz WiFi. Stofas router er underlig så 2.4 virker ikke altid. Genstart router


## Google Calendar Api setup

For at forbinde med Google oauth, se denne video [Integrating Google Calendar API in Python Projects](https://www.youtube.com/watch?v=j1mh0or2CX8&t=317s).

* Hent client_secret fra [Google Cloud Platform](https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/credentials)
* Oversæt client secret til credentials, og gem i en token

```python
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

scopes = ['https://www.googleapis.com/auth/calendar.readonly']

flow = InstalledAppFlow.from_client_secrets_file(("client_secret.json"), scopes=scopes)
credentials = flow.run_console()

pickle.dump(credentials, open("token.pkl", "wb"))
```

## TODO

* Migrate Calendar to new google account
* Add auto run on linux startup

## Dependencies

* sudo apt-get update
* sudo apt-get install python3-pip
* sudo apt-get install python3-pil
* sudo apt-get install python3-numpy
* sudo pip3 install RPi.GPIO
* sudo pip3 install pytz
* sudo pip3 install google-api-python-client
* sudo pip3 install google_auth_oauthlib
* sudo pip3 install spidev

Enable SSH via `sudo raspi-config`

## Setup WiFi Headless

* Create empty file named "ssh" in boot
* Add wpa_supplicant.conf
[Headless](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)

```bash
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

## Setup auto launch

d