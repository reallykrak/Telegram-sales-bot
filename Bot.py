from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import json
from datetime import datetime

BOT_TOKEN = "7982398630:AAHlh2apXUtrdaOv44_P7sRka0HelKtFlnk"
ADMIN_ID = 8121637254

DATA_FILE = "data.json"
LOG_DIR = "logs"
USER_LOG = os.path.join(LOG_DIR, "users.log")
PURCHASE_LOG = os.path.join(LOG_DIR, "purchases.log")

# Dil tercihlerini tut
user_languages = {}

# Verileri yükle/kaydet
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

os.makedirs(LOG_DIR, exist_ok=True)

def log_user(user):
    with open(USER_LOG, "a") as f:
        f.write(f"{datetime.now()} - {user.id} | {user.full_name}\n")

def log_purchase(user, item):
    with open(PURCHASE_LOG, "a") as f:
        f.write(f"{datetime.now()} - {user.id} | {user.full_name} satın aldı: {item}\n")

# Diller
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
        "admin_panel": "Yönetici Paneli:\n\n/toplam_kodlar\n/kodlar\n/sifirla",
        "purchase_notify": "Yeni satın alma bildirimi: {} kullanıcısı '{}' ürününü aldı.",
        "lang_btn": [  # Inline dil butonları
            [InlineKeyboardButton("Türkçe 🇹🇷", callback_data="setlang_tr"),
             InlineKeyboardButton("English 🇬🇧", callback_data="setlang_en")]
        ]
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
        "admin_panel": "Admin Panel:\n\n/total_codes\n/codes\n/reset",
        "purchase_notify": "New purchase: User {} bought '{}'.",
        "lang_btn": [
            [InlineKeyboardButton("Türkçe 🇹🇷", callback_data="setlang_tr"),
             InlineKeyboardButton("English 🇬🇧", callback_data="setlang_en")]
        ]
    }
}

# Komut: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_user(user)
    lang = user_languages.get(user.id, "tr")
    l = LANGUAGES[lang]
    await update.message.reply_text(
        l["start"],
        reply_markup=ReplyKeyboardMarkup(l["menu"], resize_keyboard=True)
    )

# /admin
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        lang = user_languages.get(update.effective_user.id, "tr")
        await update.message.reply_text(LANGUAGES[lang]["admin_panel"])

# Kod komutları
async def toplam_kodlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(f"Kullanılmış toplam kod: {len(used_gift_codes)}")

async def kodlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Kullanılmış Kodlar:\n" + "\n".join(used_gift_codes) if used_gift_codes else "Hiç kod kullanılmamış.")

async def sifirla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        used_gift_codes.clear()
        save_data()
        await update.message.reply_text("Tüm kodlar sıfırlandı.")

# Mesaj cevaplayıcı
async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()
    lang = user_languages.get(user.id, "tr")
    l = LANGUAGES[lang]

    if text == l["menu"][0][0]:  # Ödeme
        await update.message.reply_text(l["payment"])

    elif text == l["menu"][0][1]:  # Keys
        await update.message.reply_text(
            l["choose_key"],
            reply_markup=ReplyKeyboardMarkup(l["keys_menu"], resize_keyboard=True)
        )

    elif text == l["menu"][1][0]:  # Hediye
        await update.message.reply_text(l["gift_prompt"])
        context.user_data["awaiting_gift"] = True

    elif text == l["menu"][1][1]:  # İstatistik
        await update.message.reply_text(l["stats"])

    elif text == l["menu"][2][0]:  # Botu güncelle
        if user.id == ADMIN_ID:
            await update.message.reply_text(l["restart_ok"])
            os.system("bash restart.sh")
        else:
            await update.message.reply_text(l["restart_fail"])

    elif text == l["menu"][2][1]:  # Dil Değiştir (inline)
        await update.message.reply_text(
            l["lang_select"],
            reply_markup=InlineKeyboardMarkup(l["lang_btn"])
        )

    elif context.user_data.get("awaiting_gift"):
        context.user_data["awaiting_gift"] = False
        if text == "FREE123" and text not in used_gift_codes:
            used_gift_codes.append(text)
            save_data()
            await update.message.reply_text(l["gift_success"])
        else:
            await update.message.reply_text(l["gift_fail"])

    elif text in sum(l["keys_menu"], []):
        if "Ana Menü" in text or "Main Menu" in text:
            await update.message.reply_text(l["start"],
                                            reply_markup=ReplyKeyboardMarkup(l["menu"], resize_keyboard=True))
        else:
            log_purchase(user, text)
            await context.bot.send_message(chat_id=ADMIN_ID, text=l["purchase_notify"].format(user.full_name, text))
            await update.message.reply_text(l["product_info"].format(text))

    else:
        await update.message.reply_text(l["invalid"])

# Callback (inline butonlara yanıt)
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    if query.data == "setlang_tr":
        user_languages[user.id] = "tr"
    elif query.data == "setlang_en":
        user_languages[user.id] = "en"

    lang = user_languages[user.id]
    l = LANGUAGES[lang]
    await query.answer("Dil değiştirildi.")
    await query.edit_message_text(
        text=l["start"],
        reply_markup=ReplyKeyboardMarkup(l["menu"], resize_keyboard=True)
    )

# Botu başlat
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("toplam_kodlar", toplam_kodlar))
    app.add_handler(CommandHandler("kodlar", kodlar))
    app.add_handler(CommandHandler("sifirla", sifirla))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))
    app.add_handler(MessageHandler(filters.COMMAND, cevapla))  # Diğer komutlar da filtrelensin
    app.add_handler(MessageHandler(filters.ALL, cevapla))       # Güvenlik için fallback
    app.add_handler(filters.CallbackQueryHandler(handle_callback))  # Inline butonlar
    print("Bot çalışıyor.")
    app.run_polling()
