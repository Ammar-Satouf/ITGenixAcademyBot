
import threading
import time
import requests
import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد Flask
app = Flask(__name__)

# بيانات وهمية للسنة الأولى
resources = {
    "1": {
        "1": {
            "practical": {
                "programming1": {
                    "lectures": "https://drive.google.com/programming1_lectures",
                    "exams": "https://drive.google.com/programming1_exams",
                    "notes": "ركز على أساسيات C++ والخوارزميات."
                },
                "analysis1": {
                    "lectures": "https://drive.google.com/analysis1_lectures",
                    "exams": "https://drive.google.com/analysis1_exams",
                    "notes": "راجع النهايات والتفاضل."
                },
                "linear_algebra": {
                    "lectures": "https://drive.google.com/linear_algebra_lectures",
                    "exams": "https://drive.google.com/linear_algebra_exams",
                    "notes": "ركز على المصفوفات والمتجهات."
                },
                "computer_principles": {
                    "lectures": "https://drive.google.com/computer_principles_lectures",
                    "exams": "https://drive.google.com/computer_principles_exams",
                    "notes": "فهم المعالجات والهندسة."
                },
                "electrophysics": {
                    "lectures": "https://drive.google.com/electrophysics_lectures",
                    "exams": "https://drive.google.com/electrophysics_exams",
                    "notes": "راجع قوانين أوم وكيرشوف."
                },
            },
            "theoretical": {
                "arabic": {
                    "lectures": "https://drive.google.com/arabic_lectures",
                    "exams": "https://drive.google.com/arabic_exams",
                    "notes": "ركز على القواعد والنحو."
                },
                "english1": {
                    "lectures": "https://drive.google.com/english1_lectures",
                    "exams": "https://drive.google.com/english1_exams",
                    "notes": "مارس القراءة والكتابة."
                },
            },
        },
        "2": {
            "practical": {
                "programming2": {
                    "lectures": "https://drive.google.com/programming2_lectures",
                    "exams": "https://drive.google.com/programming2_exams",
                    "notes": "ركز على البرمجة الكائنية."
                },
                "analysis2": {
                    "lectures": "https://drive.google.com/analysis2_lectures",
                    "exams": "https://drive.google.com/analysis2_exams",
                    "notes": "راجع التكامل والمعادلات التفاضلية."
                },
                "linear_algebra2": {
                    "lectures": "https://drive.google.com/linear_algebra2_lectures",
                    "exams": "https://drive.google.com/linear_algebra2_exams",
                    "notes": "ركز على القيم الذاتية."
                },
                "semiconductors": {
                    "lectures": "https://drive.google.com/semiconductors_lectures",
                    "exams": "https://drive.google.com/semiconductors_exams",
                    "notes": "فهم الترانزستورات."
                },
            },
            "theoretical": {
                "english2": {
                    "lectures": "https://drive.google.com/english2_lectures",
                    "exams": "https://drive.google.com/english2_exams",
                    "notes": "ركز على المحادثة."
                },
            },
        },
    },
}

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا! أنا بوت دراسة الهندسة المعلوماتية 🖥\n"
        "استخدم الأوامر التالية:\n"
        "/lectures [year] [semester] [type]\n"
        "/exams [year] [semester] [type]\n"
        "/notes [year] [semester] [type]\n"
        "استبدل [year] بـ 1، [semester] بـ 1 أو 2، و[type] بـ practical أو theoretical\n"
        "/help - لعرض التعليمات"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "تعليمات الاستخدام:\n"
        "/lectures 1 1 practical - لمحاضرات المواد العملية\n"
        "/exams 1 2 theoretical - لأسئلة المواد النظرية\n"
        "/notes 1 1 practical - لملاحظات المواد العملية"
    )

async def lectures(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("يرجى إدخال السنة، الفصل، ونوع المادة. مثال: /lectures 1 1 practical")
        return
    year, semester, subject_type = context.args[0], context.args[1], context.args[2]
    if year in resources and semester in resources[year] and subject_type in resources[year][semester]:
        response = "محاضرات:\n"
        for subject, data in resources[year][semester][subject_type].items():
            response += f"- {subject}: {data['lectures']}\n"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("خطأ: تحقق من السنة أو الفصل أو نوع المادة")

async def exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("يرجى إدخال السنة، الفصل، ونوع المادة. مثال: /exams 1 1 practical")
        return
    year, semester, subject_type = context.args[0], context.args[1], context.args[2]
    if year in resources and semester in resources[year] and subject_type in resources[year][semester]:
        response = "أسئلة الامتحانات:\n"
        for subject, data in resources[year][semester][subject_type].items():
            response += f"- {subject}: {data['exams']}\n"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("خطأ: تحقق من السنة أو الفصل أو نوع المادة")

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("يرجى إدخال السنة، الفصل، ونوع المادة. مثال: /notes 1 1 practical")
        return
    year, semester, subject_type = context.args[0], context.args[1], context.args[2]
    if year in resources and semester in resources[year] and subject_type in resources[year][semester]:
        response = "ملاحظات هامة:\n"
        for subject, data in resources[year][semester][subject_type].items():
            response += f"- {subject}: {data['notes']}\n"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("خطأ: تحقق من السنة أو الفصل أو نوع المادة")

# إعداد Webhook
application = None
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return 'OK', 200

# نقطة فحص للحفاظ على البوت مستيقظًا
@app.route('/ping', methods=['GET'])
def ping():
    return 'Bot is alive!', 200

# وظيفة keep alive
def keep_alive():
    while True:
        try:
            requests.get("https://itgenixacademybot.onrender.com/ping")  # غيّرها للرابط الحقيقي
            print("Keep alive ping sent")
        except Exception as e:
            print(f"Keep alive error: {e}")
        time.sleep(600)

# دالة main
def main():
    global application
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("خطأ: لم يتم العثور على BOT_TOKEN")
        return

    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lectures", lectures))
    application.add_handler(CommandHandler("exams", exams))
    application.add_handler(CommandHandler("notes", notes))

    threading.Thread(target=keep_alive, daemon=True).start()

    # تهيئة Webhook
    async def setup_webhook():
        await application.bot.set_webhook(url="https://itgenixacademybot.onrender.com/webhook")  # غيّر الرابط
        print("Webhook set.")

    asyncio.run(setup_webhook())

    print("البوت يعمل...")
    app.run(host='0.0.0.0', port=8443)

if __name__ == '__main__':
    main()
