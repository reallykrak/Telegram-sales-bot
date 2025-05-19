import telebot
from telebot.types import ReplyKeyboardMarkup
import os
import json
from datetime import datetime

BOT_TOKEN = "7982398630:AAHCt_rIF2Gs3u_nrliVE7iHlfO-AmzgUho"
ADMIN_ID = 8121637254

DATA_FILE = "data.json"
LOG_DIR = "logs"
USER_LOG = os.path.join(LOG_DIR, "users.log")
PURCHASE_LOG = os.path.join(LOG_DIR, "purchases.log")

bot = telebot.TeleBot(BOT_TOKEN)

# Veri yönetimi
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"used_gift_codes": [], "languages": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()
used_gift_codes = data["used_gift_codes"]
user_languages = data.get("languages", {})

os.makedirs(LOG_DIR, exist_ok=True)

def log_user(user):
    with open(USER_LOG, "a") as f:
        f.write(f"{datetime.now()} - {user.id} | {user.first_name}\n")

def log_purchase(user, item):
    with open(PURCHASE_LOG, "a") as f:
        f.write(f"{datetime.now()} - {user.id} | {user.first_name} satın aldı: {item}\n")

LANGUAGES = {
    "tr": {
        "start": "Lütfen bir seçenek seç:",
        "language_changed": "Dil başarıyla Türkçe olarak ayarlandı.",
        "menu": [
            ["🌟 Ödeme Seçenekleri 🌟"],
            ["🎁 Bonus", "💨 Key Menü", "🔥 Komutlar"],
            ["🎁 Hediye Kodu", "📊 İstatistikler"],
            ["🔄 Botu Güncelle"],
            ["🌐 Dil Değiştir", "❓ Yardım"]
        ]
    },
    "en": {
        "start": "Please select an option:",
        "language_changed": "Language changed to English successfully.",
        "menu": [
            ["🌟 Payment Options 🌟"],
            ["🎁 Bonus", "💨 Key Menu", "🔥 Commands"],
            ["🎁 Gift Code", "📊 Statistics"],
            ["🔄 Update Bot"],
            ["🌐 Change Language", "❓ Help"]
        ]
    }
}

def get_user_language(user_id):
    return user_languages.get(str(user_id), "tr")

def set_user_language(user_id, lang_code):
    user_languages[str(user_id)] = lang_code
    data["languages"] = user_languages
    save_data()

def get_keyboard(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in LANGUAGES[lang]["menu"]:
        keyboard.row(*row)
    return keyboard

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user = message.from_user
    log_user(user)
    lang = get_user_language(user.id)
    bot.send_message(
        message.chat.id,
        LANGUAGES[lang]["start"],
        reply_markup=get_keyboard(lang)
    )

@bot.message_handler(func=lambda m: m.text in ["🌐 Dil Değiştir", "🌐 Change Language"])
def change_language(message):
    user = message.from_user
    current = get_user_language(user.id)
    new_lang = "en" if current == "tr" else "tr"
    set_user_language(user.id, new_lang)
    bot.send_message(
        message.chat.id,
        LANGUAGES[new_lang]["language_changed"],
        reply_markup=get_keyboard(new_lang)
    )

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    user = message.from_user
    lang = get_user_language(user.id)
    if message.text in ["🌐 Dil Değiştir", "🌐 Change Language"]:
        change_language(message)
    elif message.text in ["🌟 Ödeme Seçenekleri 🌟", "🌟 Payment Options 🌟"]:
        if lang == "tr":
            bot.send_message(message.chat.id,
                "=== 🌟 Ödeme Bilgileri 🌟 ===\n\n"
                "• Papara\n"
                "• Ziraat\n"
                "• Shopier\n\n"
                "İletişim • @ZEUS_BABA12\n"
                "🔥 Not - Ciddi Alıcı Değilseniz Yazmayın Lütfen.")
        else:
            bot.send_message(message.chat.id,
                "=== 🌟 Payment Information 🌟 ===\n\n"
                "• Papara\n"
                "• Ziraat\n"
                "• Shopier\n\n"
                "Contact • @ZEUS_BABA12\n"
                "🔥 Note - Please do not contact if you are not a serious buyer.")
    else:
        bot.send_message(message.chat.id, LANGUAGES[lang]["start"], reply_markup=get_keyboard(lang))

@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Admin paneline hoş geldiniz.")
    else:
        bot.send_message(message.chat.id, "Bu komut yalnızca yöneticilere özeldir.")

@bot.message_handler(commands=["toplam_kodlar"])
def total_codes(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"Kullanılmış toplam hediye kodu: {len(used_gift_codes)}")

@bot.message_handler(commands=["kodlar"])
def used_codes(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Kullanılmış kodlar:\n" + "\n".join(used_gift_codes))

@bot.message_handler(commands=["sifirla"])
def reset_codes(message):
    if message.from_user.id == ADMIN_ID:
        data["used_gift_codes"] = []
        save_data()
        bot.send_message(message.chat.id, "Kullanılmış kodlar sıfırlandı.")

print("Bot çalışıyor...")
bot.polling()
