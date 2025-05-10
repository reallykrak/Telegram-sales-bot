from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    """
    Inline bir menü oluşturur.
    Butona basıldığında callback_data "button_pressed" gönderilir.
    """
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Butona Bas", callback_data="button_pressed")
    keyboard.add(button)
    return keyboard
