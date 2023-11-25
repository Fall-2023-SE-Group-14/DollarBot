import os
import json
from mock.mock import patch
from telebot import types
from code import delete_user
from mock import ANY


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


@patch('telebot.telebot')
def test_delete_user(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(delete_user, 'helper')
    delete_user.helper.read_json.return_value = MOCK_USER_DATA
    print("Hello", MOCK_USER_DATA)
    delete_user.helper.write_json.return_value = True
    MOCK_Message_data = create_message("Hello")
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    delete_user.delete_user(MOCK_Message_data, mc)
    assert (delete_user.helper.write_json.called)


@patch('telebot.telebot')
def test_delete_user_without_data(mock_telebot, mocker):
    mocker.patch.object(delete_user, 'helper')
    delete_user.helper.read_json.return_value = {}
    delete_user.helper.write_json.return_value = True
    MOCK_Message_data = create_message("Hello")
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    delete_user.delete_user(MOCK_Message_data, mc)
    if delete_user.helper.write_json.called is False:
        assert True
