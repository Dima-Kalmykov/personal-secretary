from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

import utils
from mesproc import EventProcessor
from model.EventContent import EventResponse
from variables.constants import CALENDAR_SERVICE, CALENDAR_API_VERSION


def add_event(user_id, message):
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)
    event = make_json_event(message)
    created_event = calendar.events().insert(calendarId='primary', body=event).execute()

    start_time = created_event['start']['dateTime']
    end_time = created_event['end']['dateTime']

    current_event = EventResponse("", start_time, end_time)
    if created_event.get('summary'):
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
        start_time = event['start']['dateTime']
        end_time = event['end']['dateTime']

        current_event = EventResponse("", start_time, end_time)
        if event.get('summary'):
            current_event.summary = event['summary']

        result.append(current_event)

    return result


def make_json_event(message):
    print(f'Message = {message}')
    processor = EventProcessor()
    summary, timestamp = processor.process_message(message)
    return {
        "summary": f"{summary}",
        'start': {
            'dateTime': f'{datetime.isoformat(timestamp)}',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': f'{datetime.isoformat(timestamp + timedelta(hours=1))}',
            'timeZone': 'America/Los_Angeles',
        },
    }
