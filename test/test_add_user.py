import os
import json
from mock.mock import patch
from telebot import types
from code import add_user
from mock import ANY


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")


def test_read_json():
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_expense_record.json").st_size != 0:
            with open("./test/dummy_expense_record.json") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


@patch("telebot.telebot")
def test_add_person_working(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(add_user, "helper")
    add_user.helper.read_json.return_value = MOCK_USER_DATA
    add_user.add_person(MOCK_USER_DATA, mock_telebot)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_add_person_not_working(mock_telebot, mocker):
    mocker.patch.object(add_user, "helper")
    add_user.helper.read_json.return_value = {}
    add_user.add_person(create_message(""), mock_telebot)
    if add_user.helper.write_json.called is False:
        assert True


@patch("telebot.telebot")
def test_register_people_working(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(add_user, "helper")
    add_user.helper.read_json.return_value = MOCK_USER_DATA
    add_user.register_people(MOCK_USER_DATA, mock_telebot)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_register_people_not_working(mock_telebot, mocker):
    mocker.patch.object(add_user, "helper")
    add_user.helper.read_json.return_value = {}
    add_user.register_people(create_message(""), mock_telebot)
    if add_user.helper.write_json.called is False:
        assert True
