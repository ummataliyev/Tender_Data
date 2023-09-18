from data_app.libs.telebot import telebot


def send_telegram(*args, **kwargs) -> dict:
    """
    Use this function to send a telegram message
    """

    text = "New Updates On Tenders"
    telebot.send_message(text)
