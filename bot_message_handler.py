import requests
from google.oauth2.credentials import Credentials
from telebot import TeleBot, types

import utils
from integrations.google import dao
from integrations.google.calendar_api import get_events, add_event
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


@bot.message_handler(commands=[EVENTS_COMMAND])
def process_events(message):
    user_id = message.from_user.id
    user = dao.get_user_by_id(user_id)

    if user:
        events = get_events(message.from_user.id)
        result_message = "List of your events:\n"
        for event in events:
            result_message += f"summary = {event.summary}\n" \
                       f"start_time = {event.start_time}\n" \
                       f"end_time = {event.end_time}\n" \
                       f"-------------------------------------"
        bot.send_message(message.chat.id, result_message)
    else:
        bot.send_message(message.chat.id, f"Please, provide access to your google account")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    command = call.data
    message = call.message

    if command == REVOKE_ACCESS_COMMAND:
        revoke(message)
    if command == CONFIRM_ADDING_EVENT_COMMAND:
        remove_keyboard(message)
        add_event(message.chat.id, message)
        bot.reply_to(message, "Successfully added")
    if command == CANCEL_EVENT_ADDING_COMMAND:
        remove_keyboard(message)
        bot.reply_to(message, "Adding canceled")


@bot.message_handler(func=lambda x: True, content_types=['text'])
def process_text_messages(message):
    user_id = message.from_user.id
    user = dao.get_user_by_id(user_id)

    if user:
        yes_button = types.InlineKeyboardButton("Yes", callback_data=CONFIRM_ADDING_EVENT_COMMAND)
        no_button = types.InlineKeyboardButton("No", callback_data=CANCEL_EVENT_ADDING_COMMAND)

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(yes_button, no_button)

        bot.reply_to(message, f'Do you want to add event with given content?\n{message.text}', reply_markup=markup)
    else:
        bot.reply_to(message, f"Can't add this event. Please, provide access to your google account")


def remove_keyboard(message):
    chat_id = message.chat.id
    message_id = message.message_id

    bot.edit_message_reply_markup(chat_id, message_id)


if __name__ == "__main__":
    utils.update_bot_hints_for_commands()
