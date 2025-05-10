from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def generate_main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Ödeme Seçenekleri", callback_data="payment")],
        [InlineKeyboardButton("🔒 Güvence", callback_data="security")],
        [InlineKeyboardButton("📊 İstatistikler", callback_data="stats")],
        [InlineKeyboardButton("🎁 Referans Sistemi", callback_data="referral")]
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_key_menu():
    keyboard = []
    with open("stok.json") as file:
        stok = json.load(file)
        for key_name, key_data in stok.items():
            if key_data["stock"] > 0:
                keyboard.append([InlineKeyboardButton(key_name, callback_data=f"buy_{key_name}")])
            else:
                keyboard.append([InlineKeyboardButton(f"{key_name} (Tükendi)", callback_data="none", disabled=True)])
    return InlineKeyboardMarkup(keyboard)