from google.oauth2.credentials import Credentials
from googleapiclient import discovery

import utils
from variables.constants import API_SERVICE_NAME, API_VERSION


def add_event(user_id):
    credentials = utils.get_google_credentials(user_id)
    creds = Credentials(**credentials)
    calendar = discovery.build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    event = make_json_event()
    created_event = calendar.events().insert(calendarId='primary', body=event).execute()

    print(f"Event created: {created_event.get('htmlLink')}")


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
