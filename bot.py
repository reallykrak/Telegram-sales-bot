from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from handlers import start_handler, purchase_handler, order_history_handler, show_feedback_handler
from admin_panel import admin_commands
from menu import main_menu_handler

updater = Updater("7656355783:AAF7_PXEx8YeCNxCeJiqvgv8lTBzlkf6AIw")
dispatcher = updater.dispatcher

# Kullanıcı komutları
dispatcher.add_handler(CommandHandler("start", start_handler))
dispatcher.add_handler(CallbackQueryHandler(main_menu_handler, pattern="menu"))
dispatcher.add_handler(CallbackQueryHandler(order_history_handler, pattern="order_history"))
dispatcher.add_handler(CallbackQueryHandler(show_feedback_handler, pattern="feedback"))

# Admin işlemleri
dispatcher.add_handler(admin_commands)

updater.start_polling()
