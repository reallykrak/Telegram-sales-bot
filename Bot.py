import telebot
from telebot.types import ReplyKeyboardMarkup
import os
import json

BOT_TOKEN = "7982398630:AAFxFGTHL1r6jj9dY0QZPJlSgZkh5VOWqAE"
ADMIN_ID = 8121637254
DATA_FILE = "data.json"

bot = telebot.TeleBot(BOT_TOKEN)

# Veriler
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"used_gift_codes": [], "languages": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

data = load_data()
used_gift_codes = data.get("used_gift_codes", [])
user_languages = data.get("languages", {})
pending_gift_users = set()

# Dil paketleri
LANGUAGES = {
    "tr": {
        "start": "Lütfen bir seçenek seç:",
        "language_changed": "Dil başarıyla Türkçe olarak ayarlandı.",
        "prompt_gift": "Lütfen size verilen hediye kodunu girin:",
        "code_used": "Bu kod daha önce kullanılmış.",
        "code_valid": "Tebrikler! Kod doğru. Key'in: FLEXSTAR-3DAY",
        "code_invalid": "Üzgünüm, bu kod geçersiz veya daha önce kullanılmış.",
        "no_gift_file": "Kod listesi bulunamadı.",
    },
    "en": {
        "start": "Please select an option:",
        "language_changed": "Language changed to English successfully.",
        "prompt_gift": "Please enter your gift code:",
        "code_used": "This code has already been used.",
        "code_valid": "Congratulations! The code is valid. Your key: FLEXSTAR-3DAY",
        "code_invalid": "Sorry, this code is invalid or has already been used.",
        "no_gift_file": "Code list not found.",
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
    buttons = {
        "tr": [
            ["🌟 Ödeme Seçenekleri 🌟"],
            ["🎁 Bonus", "💨 Key Menü", "🔥 Komutlar"],
            ["🎁 Hediye Kodu", "📊 İstatistikler"],
            ["🔄 Botu Güncelle"],
            ["🌐 Dil Değiştir", "❓ Yardım"]
        ],
        "en": [
            ["🌟 Payment Options 🌟"],
            ["🎁 Bonus", "💨 Key Menu", "🔥 Commands"],
            ["🎁 Gift Code", "📊 Statistics"],
            ["🔄 Update Bot"],
            ["🌐 Change Language", "❓ Help"]
        ]
    }
    for row in buttons[lang]:
        keyboard.row(*row)
    return keyboard

@bot.message_handler(commands=["start"])
def send_welcome(message):
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, LANGUAGES[lang]["start"], reply_markup=get_keyboard(lang))

@bot.message_handler(func=lambda m: m.text in ["🌐 Dil Değiştir", "🌐 Change Language"])
def change_language(message):
    user_id = message.from_user.id
    current = get_user_language(user_id)
    new_lang = "en" if current == "tr" else "tr"
    set_user_language(user_id, new_lang)
    bot.send_message(message.chat.id, LANGUAGES[new_lang]["language_changed"], reply_markup=get_keyboard(new_lang))

@bot.message_handler(func=lambda m: m.text in ["🎁 Hediye Kodu", "🎁 Gift Code"])
def gift_code_prompt(message):
    lang = get_user_language(message.from_user.id)
    pending_gift_users.add(message.from_user.id)
    bot.send_message(message.chat.id, LANGUAGES[lang]["prompt_gift"])

@bot.message_handler(func=lambda m: m.from_user.id in pending_gift_users)
def process_gift_code(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    code = message.text.strip().lower()

    if not os.path.exists("gift.txt"):
        bot.send_message(message.chat.id, LANGUAGES[lang]["no_gift_file"])
    else:
        with open("gift.txt", "r", encoding="utf-8") as f:
            codes = [line.strip().lower() for line in f if line.strip()]

        if code in used_gift_codes:
            bot.send_message(message.chat.id, LANGUAGES[lang]["code_used"])
        elif code in codes:
            codes.remove(code)
            with open("gift.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(codes) + "\n")
            bot.send_message(message.chat.id, LANGUAGES[lang]["code_valid"])
            used_gift_codes.append(code)
            data["used_gift_codes"] = used_gift_codes
            save_data()
        else:
            bot.send_message(message.chat.id, LANGUAGES[lang]["code_invalid"])

    pending_gift_users.discard(user_id)

@bot.message_handler(func=lambda m: True)
def general_handler(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    text = message.text

    if text in ["🌟 Ödeme Seçenekleri 🌟", "🌟 Payment Options 🌟"]:
        if lang == "tr":
            bot.send_message(message.chat.id, "• Papara\n• Ziraat\n• Shopier\nİletişim: @ZEUS_BABA12")
        else:
            bot.send_message(message.chat.id, "• Papara\n• Ziraat\n• Shopier\nContact: @ZEUS_BABA12")
    elif text in ["🎁 Bonus"]:
        if lang == "tr":
            bot.send_message(message.chat.id, "Bugünün bonusu: 1 günlük VIP key! Yarın tekrar gel.")
        else:
            bot.send_message(message.chat.id, "Today's bonus: 1-day VIP key! Come back tomorrow.")
    elif text in ["🔄 Botu Güncelle", "🔄 Update Bot"]:
        bot.send_message(message.chat.id, "Bot şu anda güncel.")
    elif text in ["🔥 Komutlar", "🔥 Commands"]:
        bot.send_message(message.chat.id, "/start - Botu başlat\n/dil - Dili değiştir")
    else:
        bot.send_message(message.chat.id, LANGUAGES[lang]["start"], reply_markup=get_keyboard(lang))

print("Bot aktif...")
bot.polling()
