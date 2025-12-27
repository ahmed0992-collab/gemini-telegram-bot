import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# --- الإعدادات النهائية ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk" 
GEMINI_KEY = "AIzaSyDmk_gLK-FwkhX1VMnYfRajmh7EfeH7UZ0" 

# إعداد نموذج جمناي
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text("⚡ جارٍ التحليل، انتظر قليلاً...")
    try:
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            img_data = await file.download_as_bytearray()
            res = model.generate_content([
                update.message.caption or "ماذا يوجد في هذه الصورة؟", 
                {'mime_type': 'image/jpeg', 'data': bytes(img_data)}
            ])
        else:
            res = model.generate_content(update.message.text)
        await m.edit_text(res.text)
    except Exception as e:
        print(f"Error: {e}")
        await m.edit_text("⚠️ عذراً، حدث خطأ أثناء المعالجة.")

async def main():
    # حل مشكلة الـ Timeout بزيادة وقت الانتظار إلى 30 ثانية
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    
    # بناء التطبيق مع إعدادات الاتصال الجديدة
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    
    print("🚀 محاولة الاتصال بتلغرام...")
    
    await app.initialize()
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    
    while True: 
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
    
