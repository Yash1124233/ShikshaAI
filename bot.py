import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ===== SETUP LOGGING =====
logging.basicConfig(level=logging.INFO)

# ===== YOUR CREDENTIALS =====
TELEGRAM_BOT_TOKEN = "7516426079:AAHMheK8nFgVg1Oe0L-Vokmo-YiRsfImFIk"
GEMINI_API_KEY = "AIzaSyDK5XSq7v2nB53-tsZkU43LGGtpoEabR4w"  # Replace later

# ===== INIT GEMINI =====
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # use this for free plan

# ===== BOT COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "👋 Hello! I'm ShikshaAI, your education helper powered by Gemini.\n"
        "You can ask me any learning-related question!"
    )
    await update.message.reply_text(welcome)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        logging.error(f"Gemini Error: {e}")
        reply = "⚠️ Sorry, I couldn't connect to Gemini. Please try again later."

    await update.message.reply_text(reply)

# ===== RUN BOT =====
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 ShikshaAI Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
