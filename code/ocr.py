# This is an inprogress file
from PIL import Image
import helper
import logging
from telebot import types
from datetime import datetime
import pytesseract

option = {}

# Main run function
def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    print("Categories:")
    for c in helper.getSpendCategories():
        print("\t", c)
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup = markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)

@bot.message_handler(content_types=['photo'])
def handle_invoice(message):
	# Download the photo
	file_info = bot.get_file(message.photo[-1].file_id)
	downloaded_file = bot.download_file(file_info.file_path)

	# Save the photo locally
	with open("invoice.jpg", 'wb') as new_file:
		new_file.write(downloaded_file)

	# Perform OCR on the saved image
	text = ocr_invoice("invoice.jpg")

	# Check if OCR result contains a number
	amount = extract_amount_from_text(text)

	if amount is not None:
		user_states[message.chat.id] = {'amount': amount}
		bot.reply_to(message, f"OCR detected amount: {amount}\nIs this correct? (Yes/No)")
	else:
		bot.reply_to(message, "Couldn't detect the amount from the invoice. Please try again.")

@bot.message_handler(func=lambda message: message.text.lower() in ['yes', 'no'] and message.chat.id in user_states)
def handle_confirmation(message):
	user_id = message.chat.id

	if message.text.lower() == 'yes':
		amount = user_states[user_id]['amount']
		bot.reply_to(message, f"Great! The confirmed amount is: {amount}")
	else:
		bot.reply_to(message, "Please upload the invoice again for OCR.")

	# Clear user state
	del user_states[user_id]

def ocr_invoice(image_path):
	# Use Tesseract OCR to extract text from the image
	image = Image.open(image_path)
	text = pytesseract.image_to_string(image)

	return text

def extract_amount_from_text(text):
	# You may need a more sophisticated method to extract the amount from OCR text
	# This is just a basic example
	for word in text.split():
		if word.replace('.', '', 1).isdigit():
			return float(word)

	return None

if __name__ == "__main__":
	bot.polling()
