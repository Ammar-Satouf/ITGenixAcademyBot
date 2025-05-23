import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
from handlers import start, help_command, lectures, exams, notes
from config import BOT_TOKEN, WEBHOOK_URL, PORT

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

def main():
    global application

    if not BOT_TOKEN or not WEBHOOK_URL:
        print("تأكد من إعداد متغيرات البيئة BOT_TOKEN و WEBHOOK_URL")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lectures", lectures))
    application.add_handler(CommandHandler("exams", exams))
    application.add_handler(CommandHandler("notes", notes))

    async def set_webhook():
        await application.bot.set_webhook(WEBHOOK_URL)
        print(f"Webhook set to {WEBHOOK_URL}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())

    print("البوت شغال...")

    app.run(host='0.0.0.0', port=PORT)

if __name__ == "__main__":
    main()
