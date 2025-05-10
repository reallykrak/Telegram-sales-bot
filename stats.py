import json
from telegram import Update
from telegram.ext import CallbackContext

def get_statistics(update: Update, context: CallbackContext):
    with open("database.json") as file:
        data = json.load(file)
    
    total_users = len(data["users"])
    total_sales = sum(len(user["purchases"]) for user in data["users"].values())

    message = f"📊 **Bot İstatistikleri:**\n👥 Toplam Kullanıcı: {total_users}\n💰 Toplam Satış: {total_sales}"
    update.message.reply_text(message)