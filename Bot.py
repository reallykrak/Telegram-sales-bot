import telebot
from telebot.types import ReplyKeyboardMarkup
import os
import json

BOT_TOKEN = "7982398630:AAFxFGTHL1r6jj9dY0QZPJlSgZkh5VOWqAE"
ADMIN_ID = 8121637254
DATA_FILE = "data.json"

bot = telebot.TeleBot(BOT_TOKEN)

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

LANGUAGES = {
    "tr": {
        "start": "🟢 𝙇𝙪𝙩𝙛𝙚𝙣 𝘽𝙞𝙧 𝙎𝙚𝙘𝙚𝙣𝙚𝙠 𝙎𝙚𝙘𝙞𝙣:",
        "language_changed": "🇹🇷 𝘿𝙞𝙡 𝙗𝙖𝙨𝙖𝙧𝙞𝙮𝙡𝙖 𝙏𝙪𝙧𝙠𝙘𝙚 𝙤𝙡𝙖𝙧𝙖𝙠 𝙖𝙮𝙖𝙧𝙡𝙖𝙣𝙙ı.",
        "prompt_gift": "🎁 𝙇𝙪𝙩𝙛𝙚𝙣 𝙨𝙞𝙯𝙚 𝙫𝙚𝙧𝙞𝙡𝙚𝙣 𝙝𝙚𝙙𝙞𝙮𝙚 𝙠𝙤𝙙𝙪𝙣𝙪 𝙜𝙞𝙧𝙞𝙣:",
        "code_used": "🔴 𝘽𝙪 𝙠𝙤𝙙 𝙙𝙖𝙝𝙖 𝙤𝙣𝙘𝙚 𝙠𝙪𝙡𝙡𝙖𝙣𝙞𝙡𝙢𝙞𝙨!",
        "code_valid": "🟢 𝙏𝙚𝙗𝙧𝙞𝙠𝙡𝙚𝙧! 𝙆𝙤𝙙 𝙙𝙤𝙜𝙧𝙪. 𝙆𝙚𝙮'𝙞𝙣 : 𝙁𝙇𝙀𝙓𝙎𝙏𝘼𝙍-𝘿𝘼𝙔",
        "code_invalid": "🔴 𝙐𝙯𝙜𝙪𝙣𝙪𝙢, 𝙗𝙪 𝙠𝙤𝙙 𝙜𝙚𝙘𝙚𝙧𝙨𝙞𝙯 𝙫𝙚𝙮𝙖 𝙙𝙖𝙝𝙖 𝙤𝙣𝙘𝙚 𝙠𝙪𝙡𝙡𝙖𝙣𝙞𝙡𝙢𝙞𝙨.",
        "no_gift_file": "🔴 𝘽𝙤𝙮𝙡𝙚 𝙗𝙞𝙧 𝙠𝙤𝙙 𝙗𝙪𝙡𝙪𝙣𝙖𝙢𝙖𝙙𝙞.",
        "logo_menu": "🔴 𝙇𝙪𝙩𝙛𝙚𝙣 𝘼𝙡𝙢𝙖𝙠 𝙞𝙨𝙩𝙚𝙙𝙞𝙜𝙞𝙣𝙞𝙯 𝙆𝙚𝙮'𝙞 𝙎𝙚𝙘𝙞𝙣 :",
        "main_menu": "🏠 𝘼𝙣𝙖 𝙈𝙚𝙣𝙪𝙮𝙚 𝘿𝙤𝙣𝙪𝙡𝙙𝙪",
    },
    "en": {
        "start": "🟢 𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙡𝙚𝙘𝙩 𝙖𝙣 𝙤𝙥𝙩𝙞𝙤𝙣:",
        "language_changed": "🇺🇸 𝙇𝙖𝙣𝙜𝙪𝙖𝙜𝙚 𝙘𝙝𝙖𝙣𝙜𝙚𝙙 𝙩𝙤 𝙀𝙣𝙜𝙡𝙞𝙨𝙝 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮.",
        "prompt_gift": "🎁 𝙋𝙡𝙚𝙖𝙨𝙚 𝙚𝙣𝙩𝙚𝙧 𝙮𝙤𝙪𝙧 𝙜𝙞𝙛𝙩 𝙘𝙤𝙙𝙚:",
        "code_used": "This code has already been used.",
        "code_valid": "Congratulations! The code is valid. Your key: FLEXSTAR-3DAY",
        "code_invalid": "Sorry, this code is invalid or has already been used.",
        "no_gift_file": "Code list not found.",
        "logo_menu": "Please choose a logo option:",
        "main_menu": "Returned to main menu.",
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

def get_logo_keyboard(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = {
        "tr": [
            ["🤖 Ai Logo Oluştur"],
            ["❌ Logo 1", "⚽ Logo 2"],
            ["🧿 Logo 3", "♀️ Logo 4", "👾 Logo 5"],
            ["🏠 Ana Menü"]
        ],
        "en": [
            ["🤖 Create Ai Logo"],
            ["❌ Logo 1", "⚽ Logo 2"],
            ["🧿 Logo 3", "♀️ Logo 4", "👾 Logo 5"],
            ["🏠 Main Menu"]
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

@bot.message_handler(func=lambda m: m.text in ["💨 Key Menü", "💨 Key Menu"])
def key_menu(message):
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, LANGUAGES[lang]["logo_menu"], reply_markup=get_logo_keyboard(lang))

@bot.message_handler(func=lambda m: m.text in ["🏠 Ana Menü", "🏠 Main Menu"])
def back_to_main_menu(message):
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, LANGUAGES[lang]["main_menu"], reply_markup=get_keyboard(lang))

@bot.message_handler(func=lambda m: m.text.startswith("❌ Logo 1") or m.text.startswith("⚽ Logo 2") or m.text.startswith("🧿 Logo 3") or m.text.startswith("♀️ Logo 4") or m.text.startswith("👾 Logo 5") or m.text.startswith("🤖"))
def logo_selection(message):
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, f"{message.text} seçildi! (fiyat: sen ayarla)")

@bot.message_handler(func=lambda m: True)
def general_handler(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    text = message.text

    if text in ["🌟 Ödeme Seçenekleri 🌟", "🌟 Payment Options 🌟"]:
        msg = "• Papara\n• Ziraat\n• Shopier\nİletişim: @ZEUS_BABA12" if lang == "tr" else "• Papara\n• Ziraat\n• Shopier\nContact: @ZEUS_BABA12"
        bot.send_message(message.chat.id, msg)
    elif text in ["🎁 Bonus"]:
        msg = "Bugünün bonusu: 1 günlük VIP key! Yarın tekrar gel." if lang == "tr" else "Today's bonus: 1-day VIP key! Come back tomorrow."
        bot.send_message(message.chat.id, msg)
    elif text in ["🔄 Botu Güncelle", "🔄 Update Bot"]:
        bot.send_message(message.chat.id, "Bot şu anda güncel." if lang == "tr" else "Bot is up to date.")
    elif text in ["🔥 Komutlar", "🔥 Commands"]:
        bot.send_message(message.chat.id, "/start - Botu başlat\n/dil - Dili değiştir")
    else:
        bot.send_message(message.chat.id, LANGUAGES[lang]["start"], reply_markup=get_keyboard(lang))

print("Bot aktif...")
bot.polling()
