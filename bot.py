import telebot
import config
import handlers

# Bot nesnesini oluştur
bot = telebot.TeleBot(config.TOKEN)

# Handler’ları kayıt altına al
handlers.register_handlers(bot)

# Botu polling yöntemi ile çalıştır
bot.polling()
