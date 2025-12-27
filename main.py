import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# --- الإعدادات النهائية (تم تحديث المفاتيح) ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk" 
# تم وضع مفتاح جديد هنا لحل مشكلة Expired API Key
GEMINI_KEY = "AIzaSyDmk_gLK-FwkhX1VMnYfRajmh7EfeH7UZ0" 

genai.configure(api_key=GEMINI_KEY)
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
        await m.edit_text("⚠️ حدث خطأ، يرجى المحاولة لاحقاً.")

async def main():
    # رفع مهلة الانتظار لحل مشكلة التوقف
    t_request = HTTPXRequest(connect_timeout=40, read_timeout=40)
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    
    print("🚀 تشغيل البوت وطرد النسخ القديمة...")
    await app.initialize()
    # هذا السطر (drop_pending_updates) هو الحل لمشكلة الـ Conflict التي ظهرت عندك
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    
    while True: 
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
