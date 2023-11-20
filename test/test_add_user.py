import os
import json
from mock.mock import patch
from telebot import types
from code import add_user
from mock import ANY

#
# dateFormat = '%d-%b-%Y'
# timeFormat = '%H:%M'
# monthFormat = '%b-%Y'


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    add_user.run(message, mc)
    #assert (mc.reply_to.called)

@patch('telebot.telebot')
def test_register_user_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []

@patch('telebot.telebot')
def test_register_user_not_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []

@patch('telebot.telebot')
def test_add_person_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []

@patch('telebot.telebot')
def test_add_person_not_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []

@patch('telebot.telebot')
def test_handle_registration_choice(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []

def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


def test_read_json():
    try:
        if not os.path.exists('./test/dummy_expense_record.json'):
            with open('./test/dummy_expense_record.json', 'w') as json_file:
                json_file.write('{}')
            return json.dumps('{}')
        elif os.stat('./test/dummy_expense_record.json').st_size != 0:
            with open('./test/dummy_expense_record.json') as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
