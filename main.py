import flask
import telebot
from flask import Flask, request

import utils
from integrations.google import calendar_api, dao
from integrations.google.google_authorization import google_server
from variables.constants import HEROKU_URL
from variables.env_variables import FLASK_SECRET_KEY, BOT_TOKEN, PORT


def get_server():
    server = Flask(__name__)
    server.secret_key = FLASK_SECRET_KEY
    server.register_blueprint(google_server)

    return server


dao.init_db_tables_if_needed()
bot = telebot.TeleBot(BOT_TOKEN)
bot_server = get_server()


# Todo Если пришло сообщение неавторизованному пользователю, то просим авторизоваться
# Todo Вынести /start в отдельную команду (хотя она не нужна, будем просить вызвать /help)
# Todo Делать clear session, если пользователь делает ревок.


@bot_server.route('/start')
def start():
    user_id = utils.get_decoded_id_from_query(request)

    if not dao.get_user_by_id(user_id):
        flask.session['user_id'] = user_id
        return flask.redirect("authorize")

    calendar_api.add_event(user_id)
    return '200'


@bot.message_handler(commands=['revoke', 'start'])
def process_command(message):
    user_id = message.from_user.id
    encoded_id = utils.encode_string(str(user_id))
    command = message.text

    bot.send_message(
        message.chat.id,
        f"{HEROKU_URL}/{command}?id={encoded_id}"
    )


@bot.message_handler(func=lambda x: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, f'{message.text}')


# Todo Сделать обработчик /start
# Todo Если пользователь есть в базе, то говорим, что за всеми подсказками в /help
# Todo в /help появлюятся кнопки: авторизоваться, забрать доступ и др (прямо тут берётся user_id.
# Todo          и по нему генерится fernet url, который линкуеися к кнопке)
# Todo Если же пользователя нет в базе, то добавляем его туда и говорим, чтобы шёл в help.
@bot_server.route(f'/{BOT_TOKEN}', methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)

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
