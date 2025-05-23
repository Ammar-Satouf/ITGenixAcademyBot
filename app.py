import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
from handlers import start, help_command, lectures, exams, notes
from config import BOT_TOKEN, WEBHOOK_URL, PORT

app = Flask(__name__)
bot_app = None  # لمنع الخلط مع Flask app

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.run(bot_app.process_update(update))
    return 'OK', 200

@app.route('/ping', methods=['GET'])
def ping():
    return "✅ Bot is alive", 200

def main():
    global bot_app

    bot_app = Application.builder().token(BOT_TOKEN).build()

    # تسجيل الأوامر
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CommandHandler("lectures", lectures))
    bot_app.add_handler(CommandHandler("exams", exams))
    bot_app.add_handler(CommandHandler("notes", notes))

    # إعداد Webhook
    async def setup_webhook():
        await bot_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Webhook set: {WEBHOOK_URL}")

    asyncio.run(setup_webhook())

    print("🚀 Bot is running...")
    app.run(host="0.0.0.0", port=PORT)

if __name__ == '__main__':
    main()
