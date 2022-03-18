import requests
from google.oauth2.credentials import Credentials
from telebot import TeleBot, types

import utils
from integrations.google import dao
from variables.constants import *
from variables.env_variables import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)


def revoke(message):
    user_id = message.chat.id
    credentials = Credentials(**utils.get_google_credentials(user_id))

    response = requests.post(
        'https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    status_code = response.status_code
    response_message = "Something went wrong"

    if status_code == 200:
        dao.delete_user(user_id)
        response_message = "Access is successfully revoked!"

    bot.send_message(message.chat.id, response_message)


@bot.message_handler(commands=[SETTINGS_COMMAND])
def process_settings(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    settings_message = "Google account is not linked"

    user_id = message.from_user.id
    user = dao.get_user_by_id(user_id)

    if user:
        access_button = types.InlineKeyboardButton('Revoke access', callback_data=REVOKE_ACCESS_COMMAND)
        settings_message = f"All events will be saved to the calendar of user with email {user.email}"
    else:
        encoded_id = utils.encode_string(str(user_id))
        access_button = types.InlineKeyboardButton(
            'Provide access',
            url=f"{SERVER_URL}/{GOOGLE_URL_PREFIX}/{PROVIDE_ACCESS_COMMAND}?{USER_ID}={encoded_id}"
        )

    markup.add(access_button)
    bot.send_message(message.chat.id, settings_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == REVOKE_ACCESS_COMMAND:
        revoke(call.message)


@bot.message_handler(func=lambda x: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, f'{message.text}')


if __name__ == "__main__":
    utils.update_bot_hints_for_commands()
