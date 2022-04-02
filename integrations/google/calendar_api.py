from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

import utils
from model.EventContent import EventResponse
from variables.constants import CALENDAR_SERVICE, CALENDAR_API_VERSION
from pprint import pprint

def add_event(user_id):
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)
    event = make_json_event()
    created_event = calendar.events().insert(calendarId='primary', body=event).execute()

    start_time = created_event['start']['dateTime']
    end_time = created_event['end']['dateTime']

    current_event = EventResponse("", start_time, end_time)
    if created_event['summary']:
        current_event.summary = created_event['summary']

    return current_event


def get_events(user_id):
    print("get_events")
    result = []
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    events = calendar.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                    orderBy='startTime').execute().get('items', [])
    #  print(events)
    for event in events:
        pprint(event)
        start_time = event['start']['dateTime']
        end_time = event['end']['dateTime']
        print(start_time, end_time)
        current_event = EventResponse("", start_time, end_time)
        if event.get('summary'):
            current_event.summary = event['summary']
        print("after_if")
        result.append(current_event)

    return result


def make_json_event():
    return {
        "summary": "Da da 04",
        'start': {
            'dateTime': '2022-04-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2022-04-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
    }
