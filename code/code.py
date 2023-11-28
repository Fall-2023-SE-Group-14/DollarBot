#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import telebot
import time
import helper
import edit
import history
import display
from reminder import check_reminders
import estimate
import delete
import add
import budget
import category
import add_user
import csvfile
import delete_user
import pdf
import send_mail
import add_recurring
import delete_expense
from datetime import datetime
from jproperties import Properties
from telebot import types
import reminder
from datetime import datetime, time
import threading
import time
import ocr

configs = Properties()

with open("user.properties", "rb") as read_prop:
    configs.load(read_prop)

api_token = str(configs.get("api_token").data)
user_list = helper.read_json()
bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)


# Define listener for requests by user
def listener(user_requests):
    for req in user_requests:
        if req.content_type == "text":
            print(
                "{} name:{} chat_id:{} \nmessage: {}\n".format(
                    str(datetime.now()),
                    str(req.chat.first_name),
                    str(req.chat.id),
                    str(req.text),
                )
            )


bot.set_update_listener(listener)


# Define your list of commands and descriptions
menu_commands = [
    ("add", "Record/Add a new spending"),
    ("add_recurring", "Record the recurring expenses"),
    ("display", "Show sum of expenditure"),
    ("estimate", "Show an estimate of expenditure"),
    ("history", "Display spending history"),
    ("delete", "Clear/Erase your records"),
    ("delete_all", "Clear/Erase all your records"),
    ("edit", "Edit/Change spending details"),
    ("budget", "Add/Update/View/Delete budget"),
    ("category", "Add/Delete/Show custom categories in telegram bot"),
    ("set_reminder", "Create a reminder for your purchases or bills"),
    ("add_user", "Add user to the dollar split wise"),
    ("csv", "Download the expense in a CSV export file"),
    ("send_mail", "Send the expense report in the mail"),
    ("pdf", "Get the expense report in the form of PDF"),
    ("delete_user", "Delete a user from the epense tracker"),
    ("ocr", "Please upload your bill")
]

bot.set_my_commands(
    [
        types.BotCommand(command=command, description=description)
        for command, description in menu_commands
    ]
)


# Define a function to handle the /start and /menu commands
@bot.message_handler(commands=["start", "menu"])
def start_and_menu_command(message):
    chat_id = message.chat.id
    text_intro = "Welcome to MyDollarBot! Please select an option:"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for command, _ in menu_commands:
        markup.add(types.KeyboardButton(f"/{command}"))

    bot.send_message(chat_id, text_intro, reply_markup=markup)


# Define command handlers for each menu option
@bot.message_handler(commands=[command for command, _ in menu_commands])
def handle_menu_command(message):
    command = message.text[1:]  # Remove the '/' character from the command
    if command == "add":
        add.run(message, bot)
    elif command == "display":
        display.run(message, bot)
    elif command == "estimate":
        estimate.run(message, bot)
    elif command == "add_recurring":
        add_recurring.run(message, bot)
    elif command == "delete_all":
        delete.run(message, bot)
    elif command == "delete":
        delete_expense.run(message, bot)
    elif command == "budget":
        budget.run(message, bot)
    elif command == "edit":
        edit.run(message, bot)
    elif command == "history":
        history.run(message, bot)
    elif command == "set_reminder":
        print("Setting reminder")
        reminder.run(message, bot)
    elif command == 'ocr':
        print('Upload Bills')
        ocr.run(message, bot)
    elif command == "add_user":
        add_user.register_people(message, bot)
    elif command == "csv":
        csvfile.run(message, bot)
    elif command == "delete_user":
        delete_user.delete_user(message, bot)
    elif command == "pdf":
        pdf.run(message, bot)
    elif command == "send_mail":
        send_mail.run(message, bot)


# Define a function to periodically check reminders
def reminder_checker():
    while True:
        check_reminders(bot)
        # Sleep for one minute
        time.sleep(60)


# The main function
def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")


if __name__ == "__main__":
    reminder_thread = threading.Thread(target=reminder_checker)
    reminder_thread.daemon = True
    reminder_thread.start()

    main()
