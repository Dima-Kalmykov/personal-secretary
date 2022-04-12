from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

import integrations.google.dao as dao
import utils
from mesproc import EventProcessor
from model.EventContent import EventResponse
from variables.constants import CALENDAR_SERVICE, CALENDAR_API_VERSION


def add_event(user_id, message, timest):
    print("in add_event")
    try:
        credentials = utils.get_google_credentials(user_id)
        creds = Credentials(**credentials)
        calendar = discovery.build(CALENDAR_SERVICE, CALENDAR_API_VERSION, credentials=creds)
        print("Before mje")
        event = make_json_event(message, timest)
        calendar.events().insert(calendarId='primary', body=event).execute()
    except Exception as exp:
        print('-' * 100)
        print("Exception add_event", exp)
        print('-' * 100)
        dao.delete_user(user_id)
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


def make_json_event(summary, timest):
    try:
        print("Message from mje: ", summary)
    except Exception as exp:
        print('-' * 100)
        print("Exception mje", exp)
        print('-' * 100)
    timestamp = datetime.strptime(timest, "%Y-%m-%d %H:%M:%S")
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
