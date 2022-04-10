from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

import integrations.google.dao as dao
import utils
from mesproc import EventProcessor
from model.EventContent import EventResponse
from variables.constants import CALENDAR_SERVICE, CALENDAR_API_VERSION


def add_event(user_id, message):
    try:
        credentials = utils.get_google_credentials(user_id)
        creds = Credentials(**credentials)
        calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)
        event = make_json_event(message)
        calendar.events().insert(calendarId='primary', body=event).execute()
    except:
        dao.delete_user(message.chat.id)
        return -1


def get_events(user_id):
    result = []
    try:
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
    except:
        return -1
    return result


def make_json_event(message):
    try:
        processor = EventProcessor()
        summary, timestamp = processor.process_message(message.text)
    except Exception as exp:
        print('-' * 100)
        print("Exception mje", exp)
        print('-' * 100)
    print("Making json event: ", datetime.isoformat(timestamp))
    return {
        "summary": f"{summary}",
        'start': {
            'dateTime': f'{datetime.isoformat(timestamp)}',
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': f'{datetime.isoformat(timestamp + timedelta(hours=1))}',
            'timeZone': 'Europe/Moscow',
        },
    }
