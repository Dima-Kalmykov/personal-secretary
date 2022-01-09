from variables.env_variables import CLIENT_SECRET

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'
HEROKU_URL = 'https://private-secretary.herokuapp.com'
TOKEN_URI = 'https://oauth2.googleapis.com/token'
CLIENT_ID = '425347190480-cao3rik3n8u7led5nvptjb4mvidtvtud.apps.googleusercontent.com'

USER_ID = 'user_id'
STATE = 'state'

# Must match the url in the google credentials.
GOOGLE_URL_PREFIX = 'google'
GOOGLE_CALLBACK_METHOD = 'oauth2callback'

GOOGLE_AUTHORIZATION_STR = 'google_authorization'
GOOGLE_AUTHORIZE_METHOD = 'authorize'

HTTPS = 'https'
REVOKE_ACCESS_COMMAND = 'revoke'
PROVIDE_ACCESS_COMMAND = 'provide'

CLIENT_CONFIG = {
    "web": {
        "client_id": CLIENT_ID,
        "project_id": "personal-secretary-337417",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": TOKEN_URI,
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": f"{CLIENT_SECRET}",
        "redirect_uris": [
            f"{HEROKU_URL}/{GOOGLE_URL_PREFIX}/{GOOGLE_CALLBACK_METHOD}",
            f"{HEROKU_URL}/{GOOGLE_URL_PREFIX}/{GOOGLE_AUTHORIZE_METHOD}",
            f"{HEROKU_URL}/{GOOGLE_URL_PREFIX}",
            HEROKU_URL
        ]
    }
}

COMMANDS = [
    {
        "command": f"{PROVIDE_ACCESS_COMMAND}",
        "description": "Provide access to google calendar"
    },
    {
        "command": f"{REVOKE_ACCESS_COMMAND}",
        "description": "Revoke access from google calendar"
    }
]
