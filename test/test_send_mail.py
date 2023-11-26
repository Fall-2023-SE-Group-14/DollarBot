import os
import json
from mock.mock import patch
from telebot import types
from code import send_mail
from mock import ANY


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    send_mail.run(message, mc)
    assert (mc.register_next_step_handler.called)


@patch('telebot.telebot')
def test_add_emails(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("recommenderrecipe@gmail.com")
    send_mail.add_emails(message, mc)
    assert (mc.register_next_step_handler.called)


@patch('telebot.telebot')
def test_send_email(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Y")
    send_mail.send_email(message, mc)
    #assert ()


def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")