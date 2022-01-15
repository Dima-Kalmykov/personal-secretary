import flask
from flask import Blueprint
from google_auth_oauthlib.flow import Flow

import utils
from integrations.google import dao
from integrations.google.dao import User
from variables.constants import *

google_server = Blueprint(GOOGLE_AUTHORIZATION_STR, __name__)


@google_server.route(f'/{PROVIDE_ACCESS_COMMAND}')
def provide_access():
    user_id = utils.get_user_id_from_query(flask.request)
    print(f'User with id = {id} will be added')

    if dao.get_user_by_id(user_id):
        return 'You are already logged in'

    flask.session[USER_ID] = user_id
    return flask.redirect(GOOGLE_AUTHORIZE_METHOD)


@google_server.route(f'/{GOOGLE_AUTHORIZE_METHOD}')
def authorize():
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

    if dao.get_user_by_id(user_id):
        dao.update_user(user_id, credentials.token, credentials.refresh_token)
    else:
        new_user = User(user_id, credentials.token, credentials.refresh_token)
        dao.add_user(new_user)

    return 'Successfully! You can close the page'
