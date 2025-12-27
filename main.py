import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- إعدادات Hamill Smart Assistant ---
TOKEN = "8495625436:AAFGtPieNxQWtwhRGqBvdSd5cEEeInC5Smk"
GEMINI_KEY = "AIzaSyBHQmX71kDfD4McCJ-3w10s6VOum8ncyHw"

genai.configure(api_key=GEMINI_KEY)
# استخدمنا هذا المسمى لأنه الأكثر استقراراً لتجنب خطأ 404
model = genai.GenerativeModel('gemini-pro') 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    waiting_msg = await update.message.reply_text("🤖 جاري التفكير...")
    try:
        # محاولة التحدث مع جوجل
        response = model.generate_content(update.message.text)
        await waiting_msg.edit_text(response.text)
    except Exception as e:
        # محاولة بديلة بموديل آخر إذا فشل الأول
        try:
            alt_model = genai.GenerativeModel('gemini-1.5-pro')
            res = alt_model.generate_content(update.message.text)
            await waiting_msg.edit_text(res.text)
        except:
            await waiting_msg.edit_text("❌ واجهت مشكلة في الاتصال بمحرك جوجل، سأحاول مجدداً.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.updater.start_polling()
    await app.start()
    while True: await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
    
