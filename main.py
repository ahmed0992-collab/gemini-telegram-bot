import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# --- الإعدادات (مفتاح جديد تماماً) ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk" 
GEMINI_KEY = "AIzaSyDmk_gLK-FwkhX1VMnYfRajmh7EfeH7UZ0" 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text("⚡ جاري الاتصال بالذكاء الاصطناعي...")
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
        
        if res.text:
            await m.edit_text(res.text)
        else:
            await m.edit_text("⚠️ استلمت ردًا فارغًا من الخادم.")
            
    except Exception as e:
        print(f"Error details: {e}")
        await m.edit_text("⚠️ خطأ في المفتاح (API Key). يرجى التأكد من صلاحيته.")

async def main():
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    
    await app.initialize()
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    while True: await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
    
