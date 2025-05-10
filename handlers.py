import keyboards

def register_handlers(bot):
    # /start komutunu yakala ve kullanıcıya menüyü göster
    @bot.message_handler(commands=['start'])
    def start_handler(message):
        bot.send_message(
            message.chat.id, 
            "Merhaba! Butona bas ve mesajı al!", 
            reply_markup=keyboards.main_menu()
        )

    # Inline buton tıklamalarını yakala
    @bot.callback_query_handler(func=lambda call: call.data == "button_pressed")
    def button_handler(call):
        bot.send_message(call.message.chat.id, "denem1234 baba")
