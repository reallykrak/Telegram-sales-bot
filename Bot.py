from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

main_menu = [['Hakkında', 'İletişim'], ['Yardım']]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hoş geldin! Aşağıdaki menüden seçim yapabilirsin:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

async def mesaj_yaniti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Hakkında":
        await update.message.reply_text("Bu bot, örnek amaçlı oluşturulmuştur.")
    elif text == "İletişim":
        await update.message.reply_text("Bize ulaşmak için: @kullaniciadi")
    elif text == "Yardım":
        await update.message.reply_text("Yardım için bu mesajı kullanabilirsin.")
    else:
        await update.message.reply_text("Anlayamadım. Lütfen menüden bir seçim yap.")

if __name__ == '__main__':
    app = ApplicationBuilder().token("7656355783:AAF7_PXEx8YeCNxCeJiqvgv8lTBzlkf6AIw").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yaniti))

    print("Bot çalışıyor...")
    app.run_polling()
