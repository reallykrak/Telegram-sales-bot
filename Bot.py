from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import json
from datetime import datetime

BOT_TOKEN = "7982398630:AAHCt_rIF2Gs3u_nrliVE7iHlfO-AmzgUho"
ADMIN_ID = 8121637254

DATA_FILE = "data.json"
LOG_DIR = "logs"
USER_LOG = os.path.join(LOG_DIR, "users.log")
PURCHASE_LOG = os.path.join(LOG_DIR, "purchases.log")

# Kullanıcı verilerini yükle/kaydet
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"used_gift_codes": [], "languages": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()
used_gift_codes = data["used_gift_codes"]
user_languages = data.get("languages", {})

os.makedirs(LOG_DIR, exist_ok=True)

def log_user(user):
    with open(USER_LOG, "a") as f:
        f.write(f"{datetime.now()} - {user.id} | {user.full_name}\n")

def log_purchase(user, item):
    with open(PURCHASE_LOG, "a") as f:
        f.write(f"{datetime.now()} - {user.id} | {user.full_name} satın aldı: {item}\n")

# Dil verileri
LANGUAGES = {
    "tr": {
        "start": "Lütfen bir seçenek seç:",
        "language_changed": "Dil başarıyla Türkçe olarak ayarlandı.",
        "menu": [
            ["👥 Referans & Bakiye 💰"],
            ["🎁 Bonus", "❌ Logo Menu", "⚙️ İsim Ayarla"],
            ["🎁 Hediye Kodu", "📊 İstatistikler"],
            ["🔄 Botu Güncelle"],
            ["🌐 Dil Değiştir", "❓ Yardım"]
        ]
    },
    "en": {
        "start": "Please select an option:",
        "language_changed": "Language changed to English successfully.",
        "menu": [
            ["👥 Referral & Balance 💰"],
            ["🎁 Bonus", "❌ Logo Menu", "⚙️ Set Name"],
            ["🎁 Gift Code", "📊 Statistics"],
            ["🔄 Update Bot"],
            ["🌐 Change Language", "❓ Help"]
        ]
    }
}

# Kullanıcının dilini al (varsayılan Türkçe)
def get_user_language(user_id):
    return user_languages.get(str(user_id), "tr")

# Kullanıcının dilini ayarla
def set_user_language(user_id, lang_code):
    user_languages[str(user_id)] = lang_code
    data["languages"] = user_languages
    save_data()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_user(user)
    lang = get_user_language(user.id)
    await update.message.reply_text(
        LANGUAGES[lang]["start"],
        reply_markup=ReplyKeyboardMarkup(LANGUAGES[lang]["menu"], resize_keyboard=True)
    )

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    current = get_user_language(user.id)
    new_lang = "en" if current == "tr" else "tr"
    set_user_language(user.id, new_lang)
    await update.message.reply_text(
        LANGUAGES[new_lang]["language_changed"],
        reply_markup=ReplyKeyboardMarkup(LANGUAGES[new_lang]["menu"], resize_keyboard=True)
    )

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    text = update.message.text

    if text == "🌐 Dil Değiştir" or text == "🌐 Change Language":
        await change_language(update, context)
        return

    await update.message.reply_text(f"{LANGUAGES[lang]['start']}")

# Diğer admin komutları
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Admin paneline hoş geldiniz.")
    else:
        await update.message.reply_text("Bu komut yalnızca yöneticilere özeldir.")

async def toplam_kodlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(f"Kullanılmış toplam hediye kodu: {len(used_gift_codes)}")

async def kodlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Kullanılmış kodlar:\n" + "\n".join(used_gift_codes))

async def sifirla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        data["used_gift_codes"] = []
        save_data()
        await update.message.reply_text("Kullanılmış kodlar sıfırlandı.")

# Botu başlat
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("toplam_kodlar", toplam_kodlar))
    app.add_handler(CommandHandler("kodlar", kodlar))
    app.add_handler(CommandHandler("sifirla", sifirla))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))
    print("Bot çalışıyor.")
    app.run_polling()
