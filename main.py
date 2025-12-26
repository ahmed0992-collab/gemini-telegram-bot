import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- الإعدادات (ضع مفاتيحك هنا) ---
TOKEN = "8495625436:AAGiPMK-m5yp7pforkw2LGtCkX1z209jcsQ" 
GEMINI_KEY = "AIzaSyDmk_gLK-FwkhX1VMnYfRajmh7EfeH7UZ0" 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text("⚡ جارٍ التحليل...")
    try:
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            img_data = await file.download_as_bytearray()
            res = model.generate_content([update.message.caption or "ما هذا؟", 
                                        {'mime_type': 'image/jpeg', 'data': bytes(img_data)}])
        else:
            res = model.generate_content(update.message.text)
        await m.edit_text(res.text)
    except:
        await m.edit_text("⚠️ تأكد من المفاتيح.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    print("🚀 البوت متصل الآن!")
    await app.initialize()
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    while True: await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
          
