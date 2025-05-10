from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import json

# Ana Menü Butonları
def generate_main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Ödeme Seçenekleri", callback_data="payment")],
        [InlineKeyboardButton("🔒 Güvence", callback_data="security")],
        [InlineKeyboardButton("📊 İstatistikler", callback_data="stats")],
        [InlineKeyboardButton("🎁 Referans Sistemi", callback_data="referral")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Stok Menü Butonları
def generate_key_menu():
    keyboard = []
    with open("stok.json") as file:
        stok = json.load(file)
        for key_name, key_data in stok.items():
            if key_data["stock"] > 0:
                keyboard.append([InlineKeyboardButton(key_name, callback_data=f"buy_{key_name}")])
            else:
                keyboard.append([InlineKeyboardButton(f"{key_name} (Tükendi)", callback_data="none", disabled=True)])
    return InlineKeyboardMarkup(keyboard)

# Ana Menü Handler (Eksik Olan Fonksiyon Eklendi!)
def main_menu_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.message.reply_text("📌 Ana Menü:", reply_markup=generate_main_menu())
