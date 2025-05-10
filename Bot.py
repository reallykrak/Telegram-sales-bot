from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Telegram kullanıcı ID'n (admin komutları için)
ADMIN_ID = 8121637254  # BURAYA KENDİ TELEGRAM ID'NI YAZ

# Ana Menü Butonları
main_menu = [
    ["💰Ödeme Seçenekleri", "💢Keys"],
    ["🎁Hediye", "📊İstatistikler"],
    ["📱Botu Güncelle"]
]

# Keys Alt Menüsü
keys_menu = [
    ["King Mod", "Shield"],
    ["Zolo", "Khan"],
    ["Soi7", "Ana Menü"]
]

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hoş geldin! Lütfen bir seçenek seç:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Tüm mesajlara yanıt veren ana fonksiyon
async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰Ödeme Seçenekleri":
        await update.message.reply_text("Ödeme bilgileri:\n\n- Papara: 1234567890\n- BTC: bc1qexample\n- İletişim: @reallykrak")

    elif text == "💢Keys":
        await update.message.reply_text(
            "Lütfen almak istediğiniz key'i seçin:",
            reply_markup=ReplyKeyboardMarkup(keys_menu, resize_keyboard=True)
        )

    elif text == "Ana Menü":
        await start(update, context)

    elif text in ["King Mod", "Shield", "Zolo", "Khan", "Soi7"]:
        await update.message.reply_text(f"{text} için bilgiler:\n\nFiyat: 25₺\nStok: Var\nSatın almak için @reallykrak ile iletişime geçin.")

    elif text == "🎁Hediye":
        await update.message.reply_text("Lütfen hediye kodunu yaz:")
        context.user_data['awaiting_gift'] = True

    elif text == "📊İstatistikler":
        await update.message.reply_text("Bot İstatistikleri:\n\nToplam Kullanıcı: 128\nToplam Satış: 42\nAktif Key: 16")

    elif text == "📱Botu Güncelle":
        if update.effective_user.id == ADMIN_ID:
            await update.message.reply_text("Bot yeniden başlatılıyor...")
            os.system("kill 1")  # VPS veya Termux ortamına göre değişebilir
        else:
            await update.message.reply_text("Bu komut yalnızca yöneticilere özeldir.")

    elif context.user_data.get("awaiting_gift"):
        context.user_data['awaiting_gift'] = False
        kod = text.strip()
        if kod == "FREE193":  # örnek kod
            await update.message.reply_text("Tebrikler! Kod doğru. 1 ürün ücretsiz kazandınız.")
        else:
            await update.message.reply_text("Üzgünüm, geçersiz kod girdiniz.")

    else:
        await update.message.reply_text("Geçerli bir seçenek seçin.")

# Ana çalıştırma
if __name__ == '__main__':
    app = ApplicationBuilder().token("7982398630:AAHlh2apXUtrdaOv44_P7sRka0HelKtFlnk").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))

    print("Bot çalışıyor...")
    app.run_polling()
