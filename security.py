def security_info(update, context):
    message = """🔒 **Güvence Sistemi**
✅ Satın alınan tüm ürünler garantilidir.
✅ Her sipariş sonrası destek sağlanır.
✅ Güvenli ödeme yöntemleriyle çalışıyoruz.
✅ Adminler dolandırıcılık analizleri yapar."""
    update.message.reply_text(message)