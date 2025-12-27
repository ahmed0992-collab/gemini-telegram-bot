import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# --- إعدادات Hamill Smart Assistant ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk" 
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw" 

genai.configure(api_key=GEMINI_KEY)

# تم تعديل الاسم هنا بدقة حسب تحديث جوجل الأخير لعام 2025
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text("⚡ جاري التفكير...")
    try:
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            img_data = await file.download_as_bytearray()
            res = model.generate_content([
                update.message.caption or "حلل هذه الصورة", 
                {'mime_type': 'image/jpeg', 'data': bytes(img_data)}
            ])
        else:
            res = model.generate_content(update.message.text)
        await m.edit_text(res.text)
    except Exception as e:
        await m.edit_text(f"⚠️ خطأ: {e}")

async def main():
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    
    # هذه الخطوة ستحل مشكلة Conflict نهائياً
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("🚀 Hamill Smart Assistant is Starting...")
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    while True: await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
    
