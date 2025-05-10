from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import json

DATA_FILE = "data.json"
ADMIN_ID = 8121637254  # Telegram ID'nizi buraya girin

# JSON veri yükle/kaydet
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"used_gift_codes": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()
used_gift_codes = data["used_gift_codes"]

# Dil verileri
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
        "gift_fail": "Üzgünüm, geçersiz veya daha önce kullanılmış kod.",
        "stats": "Bot İstatistikleri:\n\nToplam Kullanıcı: 128\nToplam Satış: 42\nAktif Key: 16",
        "restart_ok": "Bot yeniden başlatılıyor...",
        "restart_fail": "Bu komut yalnızca yöneticilere özeldir.",
        "product_info": "{} için bilgiler:\n\nFiyat: 25₺\nStok: Var\nSatın almak için @reallykrak ile iletişime geçin.",
        "invalid": "Geçerli bir seçenek seçin.",
        "lang_select": "Lütfen dil seçin:",
        "lang_menu": [["Türkçe 🇹🇷", "English 🇬🇧"]],
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
        "gift_fail": "Sorry, invalid or used gift code.",
        "stats": "Bot Stats:\n\nTotal Users: 128\nTotal Sales: 42\nActive Keys: 16",
        "restart_ok": "Restarting bot...",
        "restart_fail": "This command is for admins only.",
        "product_info": "Details for {}:\n\nPrice: 25₺\nIn Stock\nContact @reallykrak to buy.",
        "invalid": "Please select a valid option.",
        "lang_select": "Please select your language:",
        "lang_menu": [["Türkçe 🇹🇷", "English 🇬🇧"]],
    }
}

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await update.message.reply_text(LANGUAGES["tr"]["start"],
                                    reply_markup=ReplyKeyboardMarkup(LANGUAGES["tr"]["menu"], resize_keyboard=True))

# Mesajları işle
async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()

    lang = "tr"  # Varsayılan dil Türkçe olarak belirlenmiş

    l = LANGUAGES[lang]
    if text == l["menu"][0][0]:  # Payment
        await update.message.reply_text(l["payment"])

    elif text == l["menu"][0][1]:  # Keys
        await update.message.reply_text(l["choose_key"],
                                        reply_markup=ReplyKeyboardMarkup(l["keys_menu"], resize_keyboard=True))

    elif text == l["menu"][1][0]:  # Gift
        await update.message.reply_text(l["gift_prompt"])
        context.user_data['awaiting_gift'] = True

    elif text == l["menu"][1][1]:  # Stats
        await update.message.reply_text(l["stats"])

    elif text == l["menu"][2][0]:  # Restart
        if int(user_id) == ADMIN_ID:
            await update.message.reply_text(l["restart_ok"])
            os.system("bash restart.sh")
        else:
            await update.message.reply_text(l["restart_fail"])

    elif text == l["menu"][2][1]:  # Language
        await update.message.reply_text(l["lang_select"],
                                        reply_markup=ReplyKeyboardMarkup(l["lang_menu"], resize_keyboard=True))

    elif text in sum(l["keys_menu"], []):
        if "Ana Menü" in text or "Main Menu" in text:
            await update.message.reply_text(l["start"],
                                            reply_markup=ReplyKeyboardMarkup(l["menu"], resize_keyboard=True))
        else:
            await update.message.reply_text(l["product_info"].format(text))

    elif context.user_data.get("awaiting_gift"):
        context.user_data['awaiting_gift'] = False
        if text == "FREE123" and text not in used_gift_codes:
            used_gift_codes.append(text)
            save_data()  # Verileri kaydet
            await update.message.reply_text(l["gift_success"])
        else:
            await update.message.reply_text(l["gift_fail"])

    else:
        await update.message.reply_text(l["invalid"])

# Botu başlat
if __name__ == '__main__':
    app = ApplicationBuilder().token("7982398630:AAHlh2apXUtrdaOv44_P7sRka0HelKtFlnk").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))
    print("Bot çalışıyor ve hediye kodları kalıcı.")
    app.run_polling()
