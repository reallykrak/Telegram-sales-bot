from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def payment_options():
    keyboard = [
        [InlineKeyboardButton("💳 Stripe", url="https://stripe.com")],
        [InlineKeyboardButton("💰 PayPal", url="https://paypal.com")],
        [InlineKeyboardButton("₿ Kripto Ödeme", callback_data="crypto_payment")]
    ]
    return InlineKeyboardMarkup(keyboard)

def handle_payment(update, context):
    query = update.callback_query
    query.message.reply_text("Ödeme seçenekleri:", reply_markup=payment_options())