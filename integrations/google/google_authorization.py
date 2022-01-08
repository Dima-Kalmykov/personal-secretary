import flask
import requests
from flask import request, Blueprint
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

import utils
from integrations.google import dao
from integrations.google.dao import User
from variables.constants import CLIENT_CONFIG, SCOPES, GOOGLE_AUTHORIZATION_STR, GOOGLE_CALLBACK_METHOD, HTTPS

google_server = Blueprint(GOOGLE_AUTHORIZATION_STR, __name__)


@google_server.route('/authorize')
def authorize():
    client_config = CLIENT_CONFIG

    flow = Flow.from_client_config(client_config, scopes=SCOPES)

    flow.redirect_uri = flask.url_for(f'{GOOGLE_AUTHORIZATION_STR}.{GOOGLE_CALLBACK_METHOD}', _external=True,
                                      _scheme=HTTPS)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    flask.session['state'] = state

    return flask.redirect(authorization_url)


@google_server.route(f'/{GOOGLE_CALLBACK_METHOD}')
def oauth2callback():
    state = flask.session['state']
    client_config = CLIENT_CONFIG

    flow = Flow.from_client_config(
        client_config, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for(f'{GOOGLE_AUTHORIZATION_STR}.{GOOGLE_CALLBACK_METHOD}', _external=True,
                                      _scheme=HTTPS)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    user_id = flask.session['user_id']

    if dao.get_user_by_id(user_id):
        dao.update_user(user_id, credentials.token, credentials.refresh_token)
    else:
        dao.add_user(User(user_id, credentials.token, credentials.refresh_token))

    return 'Successfully! You can close the page'


@google_server.route('/revoke')
def revoke():
    user_id = utils.get_decoded_id_from_query(request)
    credentials = Credentials(**utils.get_google_credentials(user_id))
    response = requests.post('https://oauth2.googleapis.com/revoke',
                             params={'token': credentials.token},
                             headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = response.status_code

    if status_code == 200:
        dao.delete_user(user_id)
        return 'Credentials successfully revoked.'
    else:
        return 'An error occurred.'
