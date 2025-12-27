import asyncio, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- الإعدادات القوية والنهائية ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk"
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw"

# تم تغيير الموديل إلى gemini-pro لتجنب خطأ 404 الذي ظهر في تلغرام
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text("🤖 جاري الاتصال بالعقل الاصطناعي...")
    try:
        # إرسال البيانات مباشرة لجوجل
        payload = {"contents": [{"parts": [{"text": update.message.text}]}]}
        res = requests.post(URL, json=payload, timeout=25)
        
        if res.status_code == 200:
            data = res.json()
            # استخراج النص من رد جوجل
            text = data['candidates'][0]['content']['parts'][0]['text']
            await m.edit_text(text)
        elif res.status_code == 404:
            await m.edit_text("❌ جوجل تقول أن هذا النموذج غير متاح لمفتاحك، سأقوم بتحديثه لك.")
        else:
            await m.edit_text(f"⚠️ خطأ من المصدر (رمز {res.status_code})، جرب مرة أخرى.")
    except Exception as e:
        await m.edit_text("❌ حدث خطأ في الشبكة، يرجى المحاولة بعد قليل.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.updater.start_polling()
    await app.start()
    
    # إبقاء البوت يعمل باستمرار على سيرفر Koyeb
    while True: await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
    
