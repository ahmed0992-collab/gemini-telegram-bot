import asyncio, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# إعدادات ثابتة وقوية
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk"
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text("⚡ جاري التفكير...")
    try:
        # اتصال مباشر بسيرفرات جوجل (طريقة المحترفين)
        payload = {"contents": [{"parts": [{"text": update.message.text}]}]}
        res = requests.post(URL, json=payload, timeout=20)
        
        if res.status_code == 200:
            text = res.json()['candidates'][0]['content']['parts'][0]['text']
            await m.edit_text(text)
        else:
            await m.edit_text(f"⚠️ جوجل ردت بخطأ {res.status_code}. سأحاول مجدداً.")
    except Exception:
        await m.edit_text("❌ فشل الاتصال، أرسل الرسالة مرة أخرى.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.updater.start_polling()
    await app.start()
    while True: await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
