from telegram import Update
from telegram.ext import CallbackContext
import json

def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text("📌 Ana Menü:", reply_markup=generate_main_menu())

def order_history_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(update.effective_user.id)

    with open("database.json") as file:
        data = json.load(file)
    
    orders = data["users"].get(user_id, {}).get("purchases", [])

    if orders:
        order_text = "📦 **Sipariş Geçmişiniz:**\n" + "\n".join(f"✅ {order}" for order in orders)
    else:
        order_text = "❌ Henüz bir siparişiniz yok."

    query.message.reply_text(order_text)

def show_feedback_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    with open("yorumlar.json") as file:
        comments = json.load(file)
    
    feedback_text = "💬 **Kullanıcı Yorumları:**\n" + "\n".join(f"📝 {comment}" for comment in comments.values())
    
    query.message.reply_text(feedback_text)