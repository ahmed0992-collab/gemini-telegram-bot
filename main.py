import os
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- الإعدادات (ضع التوكن والكي الخاص بك) ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk"
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw"

# إعداد الذكاء الاصطناعي بنسخة مستقرة
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رسالة ترحيبية باسم مشروعك
    waiting_msg = await update.message.reply_text("🤖 **Hamill Pro** | جاري المعالجة...")
    
    try:
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            img_byte = await file.download_as_bytearray()
            response = model.generate_content(["حلل هذه الصورة بالتفصيل", {"mime_type": "image/jpeg", "data": bytes(img_byte)}])
        else:
            response = model.generate_content(update.message.text)
        
        await waiting_msg.edit_text(response.text)
    except Exception as e:
        await waiting_msg.edit_text(f"❌ عذراً، حاول مجدداً خلال لحظات.")

async def main():
    # بناء البوت بنظام يتفادى التعارض (Conflict)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    
    print("✅ البوت الربحي جاهز للعمل مجاناً...")
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.updater.start_polling()
    await app.start()
    
    # إبقاء السيرفر مستيقظاً
    while True: await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
        
