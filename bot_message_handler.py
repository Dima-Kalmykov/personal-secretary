import requests
from google.oauth2.credentials import Credentials
from telebot import TeleBot, types

import utils
from integrations.google import dao
from variables.constants import *
from variables.env_variables import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=[REVOKE_ACCESS_COMMAND])
def revoke(message):
    try:
        user_id = message.from_user.id
        print(user_id)
        credentials = Credentials(**utils.get_google_credentials(user_id))

        print("Start request")
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
    except Exception as error:
        print("-" * 100)
        print(f'Error was {error}')
        print("-" * 100)


@bot.message_handler(commands=['settings'])
def process_settings(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    print("Try to get user id")
    user_id = message.from_user.id
    if dao.get_user_by_id(user_id):
        item = types.InlineKeyboardButton('Revoke access', callback_data='revoke')
    else:
        encoded_id = utils.encode_string(str(user_id))
        item = types.InlineKeyboardButton(
            'Provide access',
            url=f"{HEROKU_URL}/{GOOGLE_URL_PREFIX}/{PROVIDE_ACCESS_COMMAND}?{USER_ID}={encoded_id}"
        )

    print(f"Add item {item} to markup")
    markup.add(item)
    bot.send_message(message.chat.id, 'Choose', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'revoke':
            print("Start revoke")
            print(call.message)
            revoke(call.message)


@bot.message_handler(commands=[PROVIDE_ACCESS_COMMAND])
def provide(message):
    user_id = message.from_user.id
    encoded_id = utils.encode_string(str(user_id))

    bot.send_message(
        message.chat.id,
        f"{HEROKU_URL}/{GOOGLE_URL_PREFIX}/{PROVIDE_ACCESS_COMMAND}?{USER_ID}={encoded_id}"
    )


@bot.message_handler(func=lambda x: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, f'{message.text}')


if __name__ == "__main__":
    utils.update_bot_hints_for_commands()
