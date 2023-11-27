import helper
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF

user_emails = {}

# === Documentation of add.py ===
def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    message1 = bot.send_message(chat_id, "Please enter the email address")
    bot.register_next_step_handler(message1, add_emails, bot)

def add_emails(message, bot):
    chat_id = message.chat.id
    email = message.text
    # Assuming you want to store the email address in the user_emails dictionary
    user_emails[chat_id] = email

    # You can also validate the email address if needed
    if not is_valid_email(email):
        bot.send_message(chat_id, "Invalid email address. Please enter a valid email.")
        return

    # Notify the user that their email address has been recorded
    choice = bot.send_message(chat_id, f"Thank you for providing your email. Do you want to send email to {email}? Y/N")
    bot.register_next_step_handler(choice, send_email, bot)

# Example of a basic email validation function (you can expand this)
def is_valid_email(email):
    import re
    email_pattern = r'^\S+@\S+\.\S+$'
    return re.match(email_pattern, email) is not None
    
def send_email(choice, bot):
    if str(choice.text) == "Y" or str(choice.text) == "y":
        # Set up the Gmail API
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Port for TLS
        smtp_username = 'csc510group32@gmail.com'
        smtp_password = 'hqrx opxo lviu mubb'  

        # Create an SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)


        # Compose and send emails to all users
        for chat_id, email in user_emails.items():
            # Create a MIME message with a subject
            subject = "Calculated Owings"
            message_body = format_text_data(helper.read_json())
            message = MIMEMultipart()
            message['From'] = smtp_username
            message['To'] = email
            message['Subject'] = subject
            message.attach(MIMEText(message_body, 'plain'))

            # Send the email
            server.sendmail(smtp_username, email, message.as_string()) 

        # Close the SMTP connection
        server.quit()



def format_text_data(user_list):
    text_data = "```\n"

    for user, details in user_list.items():
        for user_name in details["users"]:
            gets_back_amount = round(details['owed'][user_name], 2)
            text_data += f"{user_name} gets back {gets_back_amount} dollars.\n"

            gives_to_list = list(details["owing"][user_name].keys())
            gives_amount_list = list(details["owing"][user_name].values())

            if not gives_to_list:
                text_data += f"{user_name} gives to no one.\n"
            else:
                for i in range(len(gives_to_list)):
                    gives_to_entry = gives_to_list[i]
                    gives_amount_entry = round(gives_amount_list[i], 2)
                    text_data += f"{user_name} gives {gives_amount_entry} dollars to {gives_to_entry}.\n"

    text_data += "```"
    return text_data












