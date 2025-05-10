from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers import start_handler, purchase_handler, order_history_handler, show_feedback_handler
from admin_panel import admin_commands
from menu import main_menu_handler

app = ApplicationBuilder().token("7656355783:AAF7_PXEx8YeCNxCeJiqvgv8lTBzlkf6AIw").build()

# Kullanıcı komutları
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CallbackQueryHandler(main_menu_handler, pattern="menu"))
app.add_handler(CallbackQueryHandler(order_history_handler, pattern="order_history"))
app.add_handler(CallbackQueryHandler(show_feedback_handler, pattern="feedback"))

# Admin işlemleri
app.add_handler(admin_commands)

app.run_polling()
