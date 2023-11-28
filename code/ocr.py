# This is an inprogress file
from PIL import Image
import helper
import logging
from telebot import types
from datetime import datetime
import pytesseract
import re

option = {}


# Main run function
def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    msg = bot.reply_to(message, "Please Upload Bill", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_invoice, bot)


def handle_invoice(message, bot):
    # Download and save the photo
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    chat_id = message.chat.id
    with open("invoice.jpg", "wb") as new_file:
        new_file.write(downloaded_file)
        bot.send_message(chat_id, "Bill Uploaded, scanning")

    text = ocr_invoice("invoice.jpg")
    bot.send_message(chat_id, text)
    global amount
    amount = extract_amount_from_text(text)  # extract total

    if amount is not None:
        msg = bot.reply_to(
            message, f"OCR detected amount: {amount}\nIs this correct? (Yes/No)"
        )
    else:
        bot.reply_to(
            message, "Couldn't detect the amount from the invoice. Please try again."
        )
    bot.register_next_step_handler(msg, runOCR, bot)


def ocr_invoice(image_path):
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
    # Use Tesseract OCR to extract text from the image
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_amount_from_text(text):
    text = text.lower()
    matches = re.findall(r"total\s*\$([\d,.]+)", text)
    if matches:
        # Take the last match
        last_match = matches[-1]
        amount = float(last_match.replace(",", ""))
        return amount
    return None


def runOCR(message, bot):
    helper.read_json()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    print("Categories:")
    for c in helper.getSpendCategories():
        print("\t", c)
        markup.add(c)
    msg = bot.reply_to(message, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


# Contains step to run after the category is selected
def post_category_selection(message, bot):
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                'Sorry I don\'t recognize this category "{}"!'.format(selected_category)
            )

        option[chat_id] = selected_category
        # message=amount
        message = bot.send_message(
            chat_id,
            f"Adding {amount} to category - {selected_category}".format(
                str(option[chat_id])
            ),
        )
        bot.register_next_step_handler(
            message, post_amount_input, bot, selected_category
        )
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no! " + str(e))
        display_text = ""
        commands = helper.getCommands()
        for (
            c
        ) in (
            commands
        ):  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, "Please select a menu option from below:")
        bot.send_message(chat_id, display_text)


# Contains step to run after the amount is inserted
def post_amount_input(message, bot, selected_category):
    try:
        chat_id = message.chat.id
        amount_value = amount
        date_of_entry = datetime.today().strftime(
            helper.getDateFormat() + " " + helper.getTimeFormat()
        )
        date_str, category_str, amount_str = (
            str(date_of_entry),
            str(option[chat_id]),
            str(amount_value),
        )
        helper.write_json(
            add_user_record(
                chat_id, "{},{},{}".format(date_str, category_str, amount_str)
            )
        )
        bot.send_message(
            chat_id,
            "The following expenditure has been recorded: You have spent ${} for {} on {}".format(
                amount_str, category_str, date_str
            ),
        )
        helper.display_remaining_budget(message, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no. " + str(e))


def add_user_record(chat_id, record_to_be_added):
    user_list = helper.read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    user_list[str(chat_id)]["data"].append(record_to_be_added)
    return user_list
