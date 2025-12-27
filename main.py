import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# --- إعدادات بوتك الخاص (Hamill Smart Assistant) ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk" 
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw" 

# إعداد محرك جيمني
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إرسال رسالة انتظار
    m = await update.message.reply_text("⚡ جاري التفكير...")
    try:
        # إذا أرسل المستخدم صورة
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            img_data = await file.download_as_bytearray()
            res = model.generate_content([
                update.message.caption or "حلل هذه الصورة", 
                {'mime_type': 'image/jpeg', 'data': bytes(img_data)}
            ])
        # إذا أرسل المستخدم نصاً
        else:
            res = model.generate_content(update.message.text)
        
        # تعديل رسالة الانتظار بالرد النهائي
        await m.edit_text(res.text)
    except Exception as e:
        print(f"Error: {e}")
        await m.edit_text(f"⚠️ عذراً، حدث خطأ: {e}")

async def main():
    # إعداد الطلبات مع وقت انتظار طويل لضمان الاستقرار
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    
    app = ApplicationBuilder().token(TOKEN).request(t_request).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_all))
    
    print("🚀 جاري تشغيل Hamill Smart Assistant...")
    
    # أهم خطوة: تنظيف أي جلسات قديمة (حل مشكلة Conflict)
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    # بدء استقبال الرسائل
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()
    
    # إبقاء البوت يعمل للأبد على السيرفر
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
