from cryptography.fernet import Fernet

from bot_message_handler import bot
from integrations.google import dao
from variables.constants import TOKEN_URI, CLIENT_ID, SCOPES, USER_ID, COMMANDS
from variables.env_variables import FERNET_KEY, CLIENT_SECRET

fernet = Fernet(FERNET_KEY.encode())


def encode_string(message):
    return fernet.encrypt(message.encode()).decode()


def decode_string(message):
    return fernet.decrypt(message.encode()).decode()


def get_user_id_from_query(request):
    return decode_string(request.args.get(USER_ID))


def get_google_credentials(user_id):
    user = dao.get_user_by_id(user_id)

    return {
        'token': user.google_token,
        'refresh_token': user.google_refresh_token,
        'token_uri': TOKEN_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scopes': SCOPES
    }


def update_bot_hints_for_commands():
    commands_are_set = bot.set_my_commands(COMMANDS)

    if commands_are_set:
        print("Commands are set")
    else:
        print("Something went wrong")
