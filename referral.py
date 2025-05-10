import json
from telegram import Update
from telegram.ext import CallbackContext

def check_referral(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)

    with open("database.json", "r+") as file:
        data = json.load(file)
        referrals = data["users"].get(user_id, {}).get("referrals", 0)
        
        if referrals >= 15:
            update.message.reply_text("🎁 Tebrikler! 15 kişi davet ettiniz, %5 indirim kazandınız!")
        else:
            update.message.reply_text(f"📢 Şu ana kadar {referrals}/15 kişiyi davet ettiniz. 15 kişiye ulaştığınızda %5 indirim alacaksınız!")