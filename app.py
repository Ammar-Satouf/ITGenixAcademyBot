import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
from handlers import start, help_command, lectures, exams, notes
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
bot_app = None  # Renamed to avoid confusion

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.run(bot_app.process_update(update))
    return 'OK', 200

@app.route('/ping', methods=['GET'])
def ping():
    return "Bot is alive!", 200

def main():
    global bot_app
    bot_token = os.getenv('BOT_TOKEN')
    webhook_url = os.getenv('WEBHOOK_URL')
    port = int(os.environ.get("PORT", 5000))  # Render يوفر PORT

    if not bot_token or not webhook_url:
        raise Exception("يرجى تحديد BOT_TOKEN و WEBHOOK_URL في متغيرات البيئة")

    bot_app = Application.builder().token(bot_token).build()

    # Register handlers
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CommandHandler("lectures", lectures))
    bot_app.add_handler(CommandHandler("exams", exams))
    bot_app.add_handler(CommandHandler("notes", notes))

    async def set_webhook():
        await bot_app.bot.set_webhook(url=webhook_url)
        print(f"✅ Webhook set: {webhook_url}")

    asyncio.run(set_webhook())

    print("🚀 Bot is running...")
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    main()
