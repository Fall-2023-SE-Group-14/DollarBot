import os
import json
from mock.mock import patch
from telebot import types
from code import csvfile
from mock import ANY


@patch("telebot.telebot")
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    csvfile.run(message, mc)
    assert mc.send_message.called


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")
