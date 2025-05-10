from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Admin ID
ADMIN_ID = 8121637254  # Kendi Telegram ID'ni yaz

# Diller
LANGUAGES = {
    "tr": {
        "start": "Lütfen bir seçenek seç:",
        "payment": "Ödeme bilgileri:\n\n- Papara: 1234567890\n- BTC: bc1qexample\n- İletişim: @reallykrak",
        "choose_key": "Lütfen almak istediğiniz key'i seçin:",
        "gift_prompt": "Lütfen hediye kodunu yaz:",
        "gift_success": "Tebrikler! Kod doğru. 1 ürün ücretsiz kazandınız.",
        "gift_fail": "Üzgünüm, geçersiz kod girdiniz.",
        "stats": "Bot İstatistikleri:\n\nToplam Kullanıcı: 128\nToplam Satış: 42\nAktif Key: 16",
        "restart_ok": "Bot yeniden başlatılıyor...",
        "restart_fail": "Bu komut yalnızca yöneticilere özeldir.",
        "product_info": "{} için bilgiler:\n\nFiyat: 25₺\nStok: Var\nSatın almak için @reallykrak ile iletişime geçin.",
        "invalid": "Geçerli bir seçenek seçin.",
        "lang_select": "Lütfen dil seçin / Please select your language:",
    },
    "en": {
        "start": "Please select an option:",
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
        "lang_select": "Lütfen dil seçin / Please select your language:",
    }
}

# Menü tanımları
main_menu = [["💰Ödeme Seçenekleri", "💢Keys"], ["🎁Hediye", "📊İstatistikler"], ["📱Botu Güncelle"]]
keys_menu = [["King Mod", "Shield"], ["Zolo", "Khan"], ["Soi7", "Ana Menü"]]
lang_menu = [["Türkçe", "English"]]

# Kullanıcı dilini tutmak için
user_lang = {}

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_lang:
        await update.message.reply_text("Lütfen dil seçin / Please select your language:",
                                        reply_markup=ReplyKeyboardMarkup(lang_menu, resize_keyboard=True))
    else:
        lang = user_lang[user_id]
        await update.message.reply_text(LANGUAGES[lang]["start"],
                                        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

# Tüm mesajlara yanıt
async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Dil seçimi
    if text == "Türkçe":
        user_lang[user_id] = "tr"
        await update.message.reply_text(LANGUAGES["tr"]["start"],
                                        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        return
    elif text == "English":
        user_lang[user_id] = "en"
        await update.message.reply_text(LANGUAGES["en"]["start"],
                                        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        return

    # Dil tanımlı mı?
    lang = user_lang.get(user_id)
    if not lang:
        await update.message.reply_text("Lütfen önce dil seçin / Please select a language.",
                                        reply_markup=ReplyKeyboardMarkup(lang_menu, resize_keyboard=True))
        return

    # Fonksiyonlar
    if text == "💰Ödeme Seçenekleri":
        await update.message.reply_text(LANGUAGES[lang]["payment"])

    elif text == "💢Keys":
        await update.message.reply_text(LANGUAGES[lang]["choose_key"],
                                        reply_markup=ReplyKeyboardMarkup(keys_menu, resize_keyboard=True))

    elif text == "Ana Menü":
        await start(update, context)

    elif text in ["King Mod", "Shield", "Zolo", "Khan", "Soi7"]:
        await update.message.reply_text(LANGUAGES[lang]["product_info"].format(text))

    elif text == "🎁Hediye":
        await update.message.reply_text(LANGUAGES[lang]["gift_prompt"])
        context.user_data['awaiting_gift'] = True

    elif text == "📊İstatistikler":
        await update.message.reply_text(LANGUAGES[lang]["stats"])

    elif text == "📱Botu Güncelle":
        if user_id == ADMIN_ID:
            await update.message.reply_text(LANGUAGES[lang]["restart_ok"])
            os.system("bash restart.sh")  # restart.sh varsa
        else:
            await update.message.reply_text(LANGUAGES[lang]["restart_fail"])

    elif context.user_data.get("awaiting_gift"):
        context.user_data['awaiting_gift'] = False
        if text == "FREE123":
            await update.message.reply_text(LANGUAGES[lang]["gift_success"])
        else:
            await update.message.reply_text(LANGUAGES[lang]["gift_fail"])

    else:
        await update.message.reply_text(LANGUAGES[lang]["invalid"])

# Bot başlatıcı
if __name__ == '__main__':
    app = ApplicationBuilder().token("7982398630:AAHlh2apXUtrdaOv44_P7sRka0HelKtFlnk").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))
    print("Bot çok dilli olarak çalışıyor...")
    app.run_polling()
