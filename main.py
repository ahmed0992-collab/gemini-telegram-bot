import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# --- الإعدادات النهائية (تم وضع مفتاحك الخاص) ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk" 
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw" 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إشعار المستخدم بدء المعالجة
    m = await update.message.reply_text("⚡ جاري التفكير...")
    try:
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            img_data = await file.download_as_bytearray()
            res = model.generate_content([
                update.message.caption or "حلل هذه الصورة بالتفصيل", 
                {'mime_type': 'image/jpeg', 'data': bytes(img_data)}
            ])
        else:
            res = model.generate_content(update.message.text)
        
        # إرسال الرد النهائي
        await m.edit_text(res.text)
            
    except Exception as e:
        print(f"Error details: {e}")
        await m.edit_text("⚠️ المعذرة، حدث خطأ فني بسيط. حاول مرة أخرى.")

async def main():
    # رفع مهلة الانتظار لضمان استقرار الاتصال من سيرفرات Koyeb
    t_request = HTTPXRequest(connect_timeout=35, read_timeout=35)
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    
    print("🚀 تشغيل البوت بمفتاحك الخاص...")
    await app.initialize()
    # تنظيف أي تحديثات قديمة لمنع خطأ Conflict الشهير
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    
    # حلقة تشغيل مستمرة
    while True: 
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
    
