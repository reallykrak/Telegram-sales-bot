from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup()
button = InlineKeyboardButton(text="Butona Bas", callback_data="clicked")
menu.add(button)
