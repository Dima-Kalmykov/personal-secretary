from variables.env_variables import CLIENT_SECRET

SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'
HEROKU_URL = 'https://super-test2001.herokuapp.com'
TOKEN_URI = 'https://oauth2.googleapis.com/token'
CLIENT_ID = '188727049297-8rkda4oi4agupp55t028ptjato8o2bjo.apps.googleusercontent.com'

GOOGLE_AUTHORIZATION_STR = 'google_authorization'
GOOGLE_CALLBACK_METHOD = 'oauth2callback'

HTTPS = 'https'


CLIENT_CONFIG = {
    "web": {
        "client_id": CLIENT_ID,
        "project_id": "pers-secretary",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": TOKEN_URI,
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": f"{CLIENT_SECRET}",
        "redirect_uris": [
            "https://super-test2001.herokuapp.com/oauth2callback"
        ]
    }
}
