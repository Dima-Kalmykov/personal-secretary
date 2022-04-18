import requests
from google.oauth2.credentials import Credentials
from telebot import TeleBot, types

import utils
from integrations.google import dao
from integrations.google.calendar_api import get_events, add_event
from mesproc import EventProcessor
from variables.constants import *
from variables.env_variables import BOT_TOKEN
from datetime import datetime

bot = TeleBot(BOT_TOKEN)
error_message = "Something went wrong. Please, provide access to Google account once more via /settings command."
processor = EventProcessor()
last_edited_message_by_chat = dict()


def revoke(message):
    user_id = message.chat.id
    credentials = Credentials(**utils.get_google_credentials(user_id))
    requests.post(
        'https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    response_message = "Access is successfully revoked!"

    dao.delete_user(user_id)
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


@bot.message_handler(commands=[START_COMMAND])
def process_start(message):
    bot.send_message(message.chat.id,
                     "Hey!\n\nThis bot allows you to add events to the Google calendar, as well as view them."
                     " 4 commands are supported, information about which you can find out by clicking "
                     "on the corresponding button in the dialog, next to the input field")


@bot.message_handler(commands=[HELP_COMMAND])
def process_help(message):
    bot.send_message(message.chat.id,
                     "Google calendar access control is configured using the command "
                     "/settings.\n\nBoth direct and forwarded messages are supported\n\n"
                     "If the time of the event cannot be determined, then 9 am will be "
                     "used (today or tomorrow, depending on the current time)")


@bot.message_handler(commands=[EVENTS_COMMAND])
def process_events(message):
    user_id = message.from_user.id
    user = dao.get_user_by_id(user_id)

    if user:
        events = get_events(message.from_user.id)
        if events == -1:
            bot.send_message(message.chat.id, error_message)
        else:
            result_message = "List of your events:\n"
            for event in events:
                result_message += f"summary = {event.summary}\n" \
                                  f"start_time = {event.start_time}\n" \
                                  f"end_time = {event.end_time}\n" \
                                  f"-------------------------------------\n"
            if not events:
                result_message = "Event list is empty"
            bot.send_message(message.chat.id, result_message)
    else:
        bot.send_message(message.chat.id, f"Please, provide access to your google account via /settings command")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    command = call.data
    message = call.message

    if command == REVOKE_ACCESS_COMMAND:
        revoke(message)
    if command == CONFIRM_ADDING_EVENT_COMMAND:
        if dao.get_user_by_id(message.chat.id):
            remove_keyboard(message)

            event_text = message.text
            event_time = event_text[41:event_text.find(' and')]
            response = add_event(message.chat.id, event_text[event_text.find('|') + 1:], event_time)
            if response == -1:
                bot.reply_to(message, error_message)
            else:
                bot.reply_to(message, "Successfully added")
        else:
            bot.reply_to(message,
                         f"Can't add this event. Please, provide access to your google account via /settings command")
    if command == CANCEL_EVENT_ADDING_COMMAND:
        remove_keyboard(message)
        bot.reply_to(message, "Adding canceled")
    if command == EDIT_EVENT_COMMAND:
        user = dao.get_user_by_id(message.chat.id)
        if user:
            if user.state == WAITING_TIME_AND_CONTENT_STATE:
                bot.reply_to(message, "You can't edit this message as you are editing another one")
                return
            last_edited_message_by_chat[message.chat.id] = message.message_id
            remove_keyboard(message)
            dao.set_user_state(message.chat.id, WAITING_TIME_AND_CONTENT_STATE)
            bot.reply_to(message,
                         "Input time and content in format %H:%M %d.%m.%Y content "
                         "(like 14:20 24.02.2022 Hello, world!)\n\n"
                         "If you want to stop editing and cancel adding - type 'CANCEL' without quotes")
        else:
            bot.reply_to(message,
                         f"Can't edit this event. Please, provide access to your google account via /settings command")


@bot.message_handler(func=lambda x: True, content_types=['text'])
def process_text_messages(message):
    user_id = message.from_user.id
    user = dao.get_user_by_id(user_id)

    if user:
        if user.state == WAITING_TIME_AND_CONTENT_STATE:
            try:
                text = message.text
                if text == 'CANCEL':
                    dao.set_user_state(user_id, DEFAULT_STATE)
                    return

                second_space_index = text.find(' ', text.find(' ') + 1)
                time = extract_time(text[:second_space_index])
                content = text[second_space_index + 1:]
                bot.edit_message_text(f'Do you want to add event with start time {time} and given content|\n{content}',
                                      message.chat.id, last_edited_message_by_chat[message.chat.id])
                dao.set_user_state(user_id, DEFAULT_STATE)
                response = add_event(message.chat.id, content, time)
                if response == -1:
                    bot.reply_to(message, error_message)
                else:
                    bot.reply_to(message, "Successfully added")
            except:
                bot.send_message(message.chat.id,
                                 f'Invalid format of message. Please, try again.'
                                 f" Correct format = %H:%M %d.%m.%Y content "
                                 f"(or 'CANCEL' without quotes to stop editing and adding)")
        else:
            yes_button = types.InlineKeyboardButton("Yes", callback_data=CONFIRM_ADDING_EVENT_COMMAND)
            no_button = types.InlineKeyboardButton("No", callback_data=CANCEL_EVENT_ADDING_COMMAND)
            edit_button = types.InlineKeyboardButton("Edit", callback_data=EDIT_EVENT_COMMAND)

            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(yes_button, edit_button, no_button)
            summary, timestamp = processor.process_message(message.text)
            bot.reply_to(message, f'Do you want to add event with start time {timestamp} and given content|\n{summary}',
                         reply_markup=markup)
    else:
        bot.reply_to(message,
                     f"Can't add this event. Please, provide access to your google account via /settings command")


def extract_time(text):
    return str(datetime.strptime(text, "%H:%M %d.%m.%Y"))


def remove_keyboard(message):
    chat_id = message.chat.id
    message_id = message.message_id

    bot.edit_message_reply_markup(chat_id, message_id)


if __name__ == "__main__":
    utils.update_bot_hints_for_commands()
