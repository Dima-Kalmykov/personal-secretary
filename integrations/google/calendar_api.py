from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

import utils
import pprint
from variables.constants import CALENDAR_SERVICE, CALENDAR_API_VERSION


def add_event(user_id):
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)
    event = make_json_event()
    created_event = calendar.events().insert(calendarId='primary', body=event).execute()

    # Todo возвращать summary и время event'a
    # Todo обрабатывать отсутствие summary
    print(f"Event created: {created_event.get('htmlLink')}")


def get_events(user_id):
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    events_result = calendar.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                           orderBy='startTime').execute()

    events = events_result.get('items', [])

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
    return events


def make_json_event():
    return {
        "summary": "Da da",
        'start': {
            'dateTime': '2022-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2022-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
    }
