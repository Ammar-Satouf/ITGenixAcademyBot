import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
from handlers import start, help_command, lectures, exams, notes
from dotenv import load_dotenv
from threading import Thread

load_dotenv()  # تحميل متغيرات البيئة من .env

app = Flask(__name__)
application = None

@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return 'OK', 200

@app.route('/ping', methods=['GET'])
def ping():
    return "Bot is alive!", 200

def run_flask(port):
    app.run(host='0.0.0.0', port=port)

def main():
    global application
    bot_token = os.getenv('BOT_TOKEN')
    webhook_url = os.getenv('WEBHOOK_URL')
    port = int(os.getenv('PORT', '8443'))

    if not bot_token or not webhook_url:
        print("تأكد من إعداد متغيرات البيئة BOT_TOKEN و WEBHOOK_URL")
        return

    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lectures", lectures))
    application.add_handler(CommandHandler("exams", exams))
    application.add_handler(CommandHandler("notes", notes))

    async def run_bot():
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(webhook_url)
        print(f"Webhook set to {webhook_url}")

    # تشغيل بوت تلغرام (async) و flask (في thread) معًا
    asyncio.run(run_bot())
    Thread(target=run_flask, args=(port,)).start()
    print("البوت شغال...")

if __name__ == "__main__":
    main()
