import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# --- الإعدادات النهائية ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk" 
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw" 

genai.configure(api_key=GEMINI_KEY)
# تم التعديل ليكون 'models/gemini-1.5-flash' كما طلبت السجلات
model = genai.GenerativeModel('models/gemini-1.5-flash')

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text("⚡ جارٍ التحليل...")
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
        await m.edit_text(f"⚠️ حدث خطأ: {e}")

async def main():
    t_request = HTTPXRequest(connect_timeout=40, read_timeout=40)
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    
    print("🚀 البدء النهائي...")
    await app.initialize()
    # تنظيف التحديثات لقتل أي نسخة قديمة (حل Conflict)
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    while True: await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
            
