import requests
from google.oauth2.credentials import Credentials
from telebot import TeleBot

import utils
from integrations.google import dao
from variables.constants import *
from variables.env_variables import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=[REVOKE_ACCESS_COMMAND])
def revoke(message):
    user_id = message.from_user.id
    credentials = Credentials(**utils.get_google_credentials(user_id))
    response = requests.post('https://oauth2.googleapis.com/revoke',
                             params={'token': credentials.token},
                             headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = response.status_code
    response_message = "Something went wrong"

    if status_code == 200:
        dao.delete_user(user_id)
        response_message = "Access successfully revoked!"

    bot.send_message(message.chat.id, response_message)


@bot.message_handler(commands=[PROVIDE_ACCESS_COMMAND])
def process_command(message):
    user_id = message.from_user.id
    encoded_id = utils.encode_string(str(user_id))

    bot.send_message(
        message.chat.id,
        f"{HEROKU_URL}/{GOOGLE_URL_PREFIX}/{PROVIDE_ACCESS_COMMAND}?{USER_ID}={encoded_id}"
    )


@bot.message_handler(func=lambda x: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, f'{message.text}')
