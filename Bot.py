from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

ADMIN_ID = 8121637254  # Kendi Telegram ID'nizi buraya girin

# Dil verisi
LANGUAGES = {
    "tr": {
        "start": "Lütfen bir seçenek seç:",
        "menu": [["💰Ödeme Seçenekleri", "💢Keys"],
                 ["🎁Hediye", "📊İstatistikler"],
                 ["📱Botu Güncelle", "🌐 Dil Değiştir"]],
        "keys_menu": [["King Mod", "Shield"], ["Zolo", "Khan"], ["Soi7", "Ana Menü"]],
        "payment": "Ödeme Bilgileri:\n\n- Papara: 1234567890\n- BTC: bc1qexample\n- İletişim: @reallykrak",
        "choose_key": "Lütfen almak istediğiniz key'i seçin:",
        "gift_prompt": "Lütfen hediye kodunu yaz:",
        "gift_success": "Tebrikler! Kod doğru. 1 ürün ücretsiz kazandınız.",
        "gift_fail": "Üzgünüm, geçersiz kod girdiniz.",
        "stats": "Bot İstatistikleri:\n\nToplam Kullanıcı: 128\nToplam Satış: 42\nAktif Key: 16",
        "restart_ok": "Bot yeniden başlatılıyor...",
        "restart_fail": "Bu komut yalnızca yöneticilere özeldir.",
        "product_info": "{} için bilgiler:\n\nFiyat: 25₺\nStok: Var\nSatın almak için @reallykrak ile iletişime geçin.",
        "invalid": "Geçerli bir seçenek seçin.",
        "lang_select": "Lütfen dil seçin:",
        "lang_menu": [["Türkçe 🇹🇷", "English 🇬🇧"]],
        "about": "Bu bot @reallykrak tarafından geliştirilmiştir.\n\nSatış, anahtar yönetimi, hediye sistemi ve daha fazlası için tasarlanmıştır.",
    },
    "en": {
        "start": "Please select an option:",
        "menu": [["💰Payment Options", "💢Keys"],
                 ["🎁Gift", "📊Statistics"],
                 ["📱Restart Bot", "🌐 Change Language"]],
        "keys_menu": [["King Mod", "Shield"], ["Zolo", "Khan"], ["Soi7", "Main Menu"]],
        "payment": "Payment Info:\n\n- Papara: 1234567890\n- BTC: bc1qexample\n- Contact: @reallykrak",
        "choose_key": "Please choose the key you want:",
        "gift_prompt": "Please enter your gift code:",
        "gift_success": "Congrats! Code accepted. You've won 1 free item.",
        "gift_fail": "Sorry, invalid gift code.",
        "stats": "Bot Stats:\n\nTotal Users: 128\nTotal Sales: 42\nActive Keys: 16",
        "restart_ok": "Restarting bot...",
        "restart_fail": "This command is for admins only.",
        "product_info": "Details for {}:\n\nPrice: 25₺\nIn Stock\nContact @reallykrak to buy.",
        "invalid": "Please select a valid option.",
        "lang_select": "Please select your language:",
        "lang_menu": [["Türkçe 🇹🇷", "English 🇬🇧"]],
        "about": "This bot is developed by @reallykrak.\n\nIt's designed for selling, key management, gift system and more.",
    }
}

user_lang = {}

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_lang:
        await update.message.reply_text("Lütfen dil seçin / Please select your language:",
                                        reply_markup=ReplyKeyboardMarkup([["Türkçe 🇹🇷", "English 🇬🇧"]], resize_keyboard=True))
    else:
        lang = user_lang[user_id]
        await update.message.reply_text(LANGUAGES[lang]["start"],
                                        reply_markup=ReplyKeyboardMarkup(LANGUAGES[lang]["menu"], resize_keyboard=True))

# /about komutu
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "tr")
    await update.message.reply_text(LANGUAGES[lang]["about"])

# Mesajları işle
async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if "Türkçe" in text:
        user_lang[user_id] = "tr"
        await update.message.reply_text(LANGUAGES["tr"]["start"],
                                        reply_markup=ReplyKeyboardMarkup(LANGUAGES["tr"]["menu"], resize_keyboard=True))
        return
    elif "English" in text:
        user_lang[user_id] = "en"
        await update.message.reply_text(LANGUAGES["en"]["start"],
                                        reply_markup=ReplyKeyboardMarkup(LANGUAGES["en"]["menu"], resize_keyboard=True))
        return

    lang = user_lang.get(user_id)
    if not lang:
        await update.message.reply_text("Lütfen önce dil seçin / Please select a language:",
                                        reply_markup=ReplyKeyboardMarkup([["Türkçe 🇹🇷", "English 🇬🇧"]], resize_keyboard=True))
        return

    l = LANGUAGES[lang]

    if text == l["menu"][0][0]:  # Ödeme / Payment
        buttons = [[InlineKeyboardButton("Papara ile Öde", url="https://papara.com")],
                   [InlineKeyboardButton("BTC ile Öde", url="https://bitcoin.org")],
                   [InlineKeyboardButton("Satıcıyla İletişim", url="https://t.me/reallykrak")]]
        await update.message.reply_text(l["payment"], reply_markup=InlineKeyboardMarkup(buttons))

    elif text == l["menu"][0][1]:  # Keys
        await update.message.reply_text(l["choose_key"],
                                        reply_markup=ReplyKeyboardMarkup(l["keys_menu"], resize_keyboard=True))

    elif text == l["menu"][1][0]:  # Hediye / Gift
        await update.message.reply_text(l["gift_prompt"])
        context.user_data['awaiting_gift'] = True

    elif text == l["menu"][1][1]:  # İstatistik / Statistics
        await update.message.reply_text(l["stats"])

    elif text == l["menu"][2][0]:  # Botu güncelle / restart
        if user_id == ADMIN_ID:
            await update.message.reply_text(l["restart_ok"])
            os.system("bash restart.sh")
        else:
            await update.message.reply_text(l["restart_fail"])

    elif text == l["menu"][2][1]:  # Dil değiştir
        user_lang.pop(user_id, None)
        await update.message.reply_text(l["lang_select"],
                                        reply_markup=ReplyKeyboardMarkup(l["lang_menu"], resize_keyboard=True))

    elif text in sum(l["keys_menu"], []):  # Key ürünleri
        if "Ana Menü" in text or "Main Menu" in text:
            await update.message.reply_text(l["start"],
                                            reply_markup=ReplyKeyboardMarkup(l["menu"], resize_keyboard=True))
        else:
            await update.message.reply_text(l["product_info"].format(text))

    elif context.user_data.get("awaiting_gift"):
        context.user_data['awaiting_gift'] = False
        if text == "FREE123":
            await update.message.reply_text(l["gift_success"])
        else:
            await update.message.reply_text(l["gift_fail"])

    else:
        await update.message.reply_text(l["invalid"])

# Botu başlat
if __name__ == '__main__':
    app = ApplicationBuilder().token("7982398630:AAHlh2apXUtrdaOv44_P7sRka0HelKtFlnk").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))
    print("Bot dillerle birlikte çalışıyor.")
    app.run_polling()
