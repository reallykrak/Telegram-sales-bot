from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import json

# Ana Menü Başlatıcı
def start_handler(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🛍️ Key Satın Al", callback_data="menu")],
        [InlineKeyboardButton("📜 Sipariş Geçmişi", callback_data="order_history")],
        [InlineKeyboardButton("💬 Yorumlar", callback_data="feedback")]
    ]
    update.message.reply_text("📌 Ana Menü:", reply_markup=InlineKeyboardMarkup(keyboard))

# Sipariş Geçmişi Görüntüleyici
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

# Kullanıcı Geri Bildirimleri
def show_feedback_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    with open("yorumlar.json") as file:
        comments = json.load(file)
    
    feedback_text = "💬 **Kullanıcı Yorumları:**\n" + "\n".join(f"📝 {comment}" for comment in comments.values())
    
    query.message.reply_text(feedback_text)

# Eksik Olan `purchase_handler` Fonksiyonu
def purchase_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    key_name = query.data

    with open("stok.json") as file:
        stok = json.load(file)

    if key_name in stok and stok[key_name]["stock"] > 0:
        message = f"🎥 **Tanıtım Videosu:** {stok[key_name]['video']}\n💰 **Fiyat:** {stok[key_name]['price']}\n📩 **Satın almak için DM:** @YourTelegram"
        query.message.reply_text(message)

        # Stok Güncellemesi
        stok[key_name]["stock"] -= 1
        with open("stok.json", "w") as file:
            json.dump(stok, file, indent=4)
    else:
        query.message.reply_text(f"❌ {key_name} tükenmiştir.")
