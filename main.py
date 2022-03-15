from flask import Flask
from flask import request
from telebot.types import Update

import utils
from bot_message_handler import bot
from integrations.google import dao
from integrations.google.authorization import google_server
from variables.constants import *
from variables.env_variables import FLASK_SECRET_KEY, BOT_TOKEN, PORT


def get_server():
    server = Flask(__name__)
    server.secret_key = FLASK_SECRET_KEY
    server.register_blueprint(google_server, url_prefix=f'/{GOOGLE_URL_PREFIX}')

    return server


bot_server = get_server()


@bot_server.route(f'/{BOT_TOKEN}', methods=['POST'])
def get_message():
    print("HERE")
    json_string = request.get_data().decode('utf-8')
    update = Update.de_json(json_string)

    print(update)
    bot.process_new_updates([update])

    return '!', 200


@bot_server.route('/')
def webhook():
    print("HERE 2")
    bot.remove_webhook()
    #remove_heroku !!!
    app_url = f'{HEROKU_URL}/{BOT_TOKEN}'
    print(app_url)
    bot.set_webhook(url=app_url)

    return '!', 200


if __name__ == '__main__':
    dao.init_db_tables_if_needed()
    utils.update_bot_hints_for_commands()

    bot_server.run(host='164.90.214.186', port=PORT, debug=True,
    ssl_context=('/etc/letsencrypt/live/personal-secretary.mooo.com/fullchain.pem',
    '/etc/letsencrypt/live/personal-secretary.mooo.com/privkey.pem'))
    # bot.remove_webhook()
    # bot.infinity_polling()
