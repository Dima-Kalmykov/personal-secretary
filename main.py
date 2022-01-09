import flask
from flask import Flask, request
from telebot import TeleBot
from telebot.types import Update

import utils
from integrations.google import dao
from integrations.google.google_authorization import google_server
from variables.constants import *
from variables.env_variables import FLASK_SECRET_KEY, BOT_TOKEN, PORT


def get_server():
    server = Flask(__name__)
    server.secret_key = FLASK_SECRET_KEY
    server.register_blueprint(google_server)

    return server


dao.init_db_tables_if_needed()
bot = TeleBot(BOT_TOKEN)
bot_server = get_server()


@bot_server.route(f'/{REQUEST_ACCESS_COMMAND}')
def start():
    user_id = utils.get_user_id_from_query(request)

    if dao.get_user_by_id(user_id):
        return 'You are already logged in'

    flask.session[USER_ID] = user_id
    return flask.redirect(GOOGLE_AUTHORIZE_METHOD)


@bot.message_handler(commands=[REQUEST_ACCESS_COMMAND, REVOKE_ACCESS_COMMAND])
def process_command(message):
    user_id = message.from_user.id
    encoded_id = utils.encode_string(str(user_id))
    command = message.text

    bot.send_message(
        message.chat.id,
        f"{HEROKU_URL}/{command}?{USER_ID}={encoded_id}"
    )


@bot.message_handler(func=lambda x: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, f'{message.text}')


@bot_server.route(f'/{BOT_TOKEN}', methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = Update.de_json(json_string)

    bot.process_new_updates([update])

    return '!', 200


@bot_server.route('/')
def webhook():
    bot.remove_webhook()
    app_url = f'{HEROKU_URL}/{BOT_TOKEN}'
    bot.set_webhook(url=app_url)

    return '!', 200


if __name__ == '__main__':
    bot_server.run(host='0.0.0.0', port=PORT, debug=True)
