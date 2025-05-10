from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Ana Menü
main_menu = [['Ürünler', 'Sipariş Ver'], ['Hakkında']]

# Ürün Listesi
urunler = {
    "Discord Nitro": 25,
    "Spotify Premium": 15,
    "Netflix": 30
}

ADMIN_ID = 8121637254 # Kendi Telegram ID'n ile değiştir

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hoş geldin! Menüden seçim yapabilirsin:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Ürünler":
        liste = "\n".join([f"- {ad}: {fiyat}₺" for ad, fiyat in urunler.items()])
        await update.message.reply_text(f"Satıştaki ürünler:\n\n{liste}")
    elif text == "Hakkında":
        await update.message.reply_text("Bu bot lisans key satışı için tasarlanmıştır.")
    elif text == "Sipariş Ver":
        urun_menu = [[urun] for urun in urunler.keys()]
        await update.message.reply_text(
            "Hangi ürünü almak istersin?",
            reply_markup=ReplyKeyboardMarkup(urun_menu, resize_keyboard=True)
        )
    elif text in urunler:
        key = ver_key(text)
        if key:
            await update.message.reply_text(f"Tebrikler! İşte ürünün keyi:\n\n`{key}`", parse_mode="Markdown")
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Yeni sipariş!\n\nKullanıcı: @{update.effective_user.username or 'Anonim'}\nID: {update.effective_user.id}\nÜrün: {text}\nKey: {key}"
            )
        else:
            await update.message.reply_text("Üzgünüz, bu ürün stokta yok.")
    else:
        await update.message.reply_text("Geçerli bir seçim yap lütfen.")

def ver_key(urun_adi):
    try:
        with open("keys.txt", "r") as f:
            satirlar = f.readlines()

        for i, line in enumerate(satirlar):
            ad, key = line.strip().split(":", 1)
            if ad == urun_adi:
                del satirlar[i]
                with open("keys.txt", "w") as f:
                    f.writelines(satirlar)
                return key
        return None
    except FileNotFoundError:
        return None

if __name__ == '__main__':
    app = ApplicationBuilder().token("7982398630:AAHlh2apXUtrdaOv44_P7sRka0HelKtFlnk").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))

    print("Bot çalışıyor...")
    app.run_polling()
