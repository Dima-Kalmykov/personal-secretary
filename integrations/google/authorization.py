import flask
from flask import Blueprint
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient import discovery

import utils
from integrations.google import dao
from integrations.google.dao import User
from variables.constants import *

google_server = Blueprint(GOOGLE_AUTHORIZATION_STR, __name__)


@google_server.route(f'/{PROVIDE_ACCESS_COMMAND}')
def provide_access():
    user_id = utils.get_user_id_from_query(flask.request)

    if dao.get_user_by_id(user_id):
        return 'You are already logged in'

    flask.session[USER_ID] = user_id
    return flask.redirect(GOOGLE_AUTHORIZE_METHOD)


@google_server.route(f'/{GOOGLE_AUTHORIZE_METHOD}')
def authorize():
    try:
        flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)

        flow.redirect_uri = flask.url_for(
            f'{GOOGLE_AUTHORIZATION_STR}.{GOOGLE_CALLBACK_METHOD}',
            _external=True,
            _scheme=HTTPS
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        flask.session[STATE] = state

        return flask.redirect(authorization_url)
    except:
        return "You should provide access to your google calendar"


@google_server.route(f'/{GOOGLE_CALLBACK_METHOD}')
def oauth2callback():
    state = flask.session[STATE]

    flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES, state=state)

    flow.redirect_uri = flask.url_for(
        f'{GOOGLE_AUTHORIZATION_STR}.{GOOGLE_CALLBACK_METHOD}',
        _external=True,
        _scheme=HTTPS
    )

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    user_id = flask.session[USER_ID]

    if not dao.get_user_by_id(user_id):
        new_user = User(user_id, credentials.token, credentials.refresh_token, None)
        dao.add_user(new_user)

    user_email = get_email(user_id, credentials)
    dao.update_user(user_id, credentials.token, credentials.refresh_token, user_email)

    return 'Successfully! You can close the page'


def get_email(user_id, credentials):
    credentials = utils.get_google_credentials(user_id, credentials.token, credentials.refresh_token)
    creds = Credentials(**credentials)

    service = discovery.build(OAUTH_SERVICE, OAUTH_API_VERSION, credentials=creds)
    data = service.userinfo().get().execute()

    return data['email']
