from telegram import Update
from telegram.ext import CallbackContext
import json
from config import CONFIG

def is_admin(user_id):
    return str(user_id) in CONFIG["ADMIN_IDS"]

def admin_commands(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)

    if not is_admin(user_id):
        update.message.reply_text("🚫 Yetkiniz yok!")
        return

    update.message.reply_text("🔧 Admin paneline hoş geldiniz!")

def update_stock(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)

    if not is_admin(user_id):
        update.message.reply_text("🚫 Yetkiniz yok!")
        return

    query = update.callback_query
    key_name = query.data

    with open("stok.json", "r+") as file:
        data = json.load(file)
        if key_name in data:
            data[key_name]["stock"] -= 1
            file.seek(0)
            json.dump(data, file, indent=4)
            update.message.reply_text(f"✅ {key_name} stok güncellendi!")
        else:
            update.message.reply_text("❌ Stokta böyle bir ürün yok.")