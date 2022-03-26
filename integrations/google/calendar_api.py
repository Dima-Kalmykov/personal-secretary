from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

import utils
from model.EventContent import EventResponse
from variables.constants import CALENDAR_SERVICE, CALENDAR_API_VERSION


def add_event(user_id):
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)
    event = make_json_event()
    created_event = calendar.events().insert(calendarId='primary', body=event).execute()

    start_time = created_event['start']['datetime']
    end_time = created_event['end']['datetime']

    current_event = EventResponse("", start_time, end_time)
    if created_event['summary']:
        current_event.summary = created_event['summary']

    return current_event


def get_events(user_id):
    result = []
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    events = calendar.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                    orderBy='startTime').execute().get('items', [])

    for event in events:
        start_time = event['start']['datetime']
        end_time = event['end']['datetime']

        current_event = EventResponse("", start_time, end_time)
        if event['summary']:
            current_event.summary = event['summary']

        result.append(current_event)

    return result


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
