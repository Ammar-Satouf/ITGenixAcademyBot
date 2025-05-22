import threading
import time
import requests
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد Flask
app = Flask(name)

# بيانات وهمية للسنة الأولى
resources = {
    "1": {
        "1": {
            "practical": {
                "programming1": {
                    "lectures": "رابط محاضرات برمجة 1: https://drive.google.com/programming1_lectures",
                    "exams": "أسئلة برمجة 1: https://drive.google.com/programming1_exams",
                    "notes": "ملاحظات برمجة 1: ركز على أساسيات C++ والخوارزميات."
                },
                "analysis1": {
                    "lectures": "رابط محاضرات تحليل 1: https://drive.google.com/analysis1_lectures",
                    "exams": "أسئلة تحليل 1: https://drive.google.com/analysis1_exams",
                    "notes": "ملاحظات تحليل 1: راجع النهايات والتفاضل."
                },
                "linear_algebra": {
                    "lectures": "رابط محاضرات جبر لاخطي: https://drive.google.com/linear_algebra_lectures",
                    "exams": "أسئلة جبر لاخطي: https://drive.google.com/linear_algebra_exams",
                    "notes": "ملاحظات جبر لاخطي: ركز على المصفوفات والمتجهات."
                },
                "computer_principles": {
                    "lectures": "رابط محاضرات مبادئ عمل الحاسوب: https://drive.google.com/computer_principles_lectures",
                    "exams": "أسئلة مبادئ عمل الحاسوب: https://drive.google.com/computer_principles_exams",
                    "notes": "ملاحظات مبادئ عمل الحاسوب: فهم المعالجات والهندسة."
                },
                "electrophysics": {
                    "lectures": "رابط محاضرات الفيزياء الكهربائية: https://drive.google.com/electrophysics_lectures",
                    "exams": "أسئلة الفيزياء الكهربائية: https://drive.google.com/electrophysics_exams",
                    "notes": "ملاحظات الفيزياء الكهربائية: راجع قوانين أوم وكيرشوف."
                },
            },
            "theoretical": {
                "arabic": {
                    "lectures": "رابط محاضرات اللغة العربية: https://drive.google.com/arabic_lectures",
                    "exams": "أسئلة اللغة العربية: https://drive.google.com/arabic_exams",
                    "notes": "ملاحظات اللغة العربية: ركز على القواعد والنحو."
                },
                "english1": {
                    "lectures": "رابط محاضرات اللغة الإنجليزية 1: https://drive.google.com/english1_lectures",
                    "exams": "أسئلة اللغة الإنجليزية 1: https://drive.google.com/english1_exams",
                    "notes": "ملاحظات اللغة الإنجليزية 1: مارس القراءة والكتابة."
                },
            },
        },
        "2": {
            "practical": {
                "programming2": {
                    "lectures": "رابط محاضرات برمجة 2: https://drive.google.com/programming2_lectures",
                    "exams": "أسئلة برمجة 2: https://drive.google.com/programming2_exams",
                    "notes": "ملاحظات برمجة 2: ركز على البرمجة الكائنية."
                },
                "analysis2": {
                    "lectures": "رابط محاضرات تحليل 2: https://drive.google.com/analysis2_lectures",
                    "exams": "أسئلة تحليل 2: https://drive.google.com/analysis2_exams",
                    "notes": "ملاحظات تحليل 2: راجع التكامل والمعادلات التفاضلية."
                },
                "linear_algebra2": {
                    "lectures": "رابط محاضرات جبر خطي: https://drive.google.com/linear_algebra2_lectures",
                    "exams": "أسئلة جبر خطي: https://drive.google.com/linear_algebra2_exams",
                    "notes": "ملاحظات جبر خطي: ركز على القيم الذاتية."
                },
                "semiconductors": {"lectures": "رابط محاضرات فيزياء أنصاف نواقل: https://drive.google.com/semiconductors_lectures",
                    "exams": "أسئلة فيزياء أنصاف نواقل: https://drive.google.com/semiconductors_exams",
                    "notes": "ملاحظات فيزياء أنصاف نواقل: فهم الترانزستورات."
                },
            },
            "theoretical": {
                "english2": {
                    "lectures": "رابط محاضرات اللغة الإنجليزية 2: https://drive.google.com/english2_lectures",
                    "exams": "أسئلة اللغة الإنجليزية 2: https://drive.google.com/english2_exams",
                    "notes": "ملاحظات اللغة الإنجليزية 2: ركز على المحادثة."
                },
            },
        },
    },
}

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "مرحبًا! أنا بوت دراسة الهندسة المعلوماتية 🖥️\n"
        "استخدم الأوامر التالية:\n"
        "/lectures [year] [semester] [type] - لمحاضرات (مثل /lectures 1 1 practical)\n"
        "/exams [year] [semester] [type] - لأسئلة الامتحانات\n"
        "/notes [year] [semester] [type] - لملاحظات هامة\n"
        "استبدل [year] بـ 1، [semester] بـ 1 أو 2، و[type] بـ practical أو theoretical\n"
        "/help - لعرض التعليمات"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "تعليمات الاستخدام:\n"
        "استخدم الأوامر مع السنة (1)، الفصل (1 أو 2)، ونوع المادة (practical أو theoretical).\n"
        "مثال:\n"
        "/lectures 1 1 practical - لمحاضرات المواد العملية والنظرية\n"
        "/exams 1 2 theoretical - لأسئلة المواد النظرية\n"
        "/notes 1 1 practical - لملاحظات المواد العملية والنظرية"
    )
    await update.message.reply_text(help_message)

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
        await update.message.reply_text("خطأ: تحقق من السنة (1)، الفصل (1 أو 2)، أو نوع المادة (practical أو theoretical)")

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
        await update.message.reply_text("خطأ: تحقق من السنة (1)، الفصل (1 أو 2)، أو نوع المادة (practical أو theoretical)")

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
        await update.message.reply_text("خطأ: تحقق من السنة (1)، الفصل (1 أو 2)، أو نوع المادة (practical أو theoretical)")

# إعداد Webhook لتلقي تحديثات تلغرام
application = None
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return 'OK', 200

# وظيفة keep alive
def keep_alive():
    while True:
        try:
            # استبدل بـ URL الخاص بخادمك بعد النشر
            requests.get("https://your-app-name.onrender.com/ping")
            print("Keep alive ping sent")
        except Exception as e:
            print(f"Keep alive error: {e}")
        time.sleep(600)  # إرسال طلب كل 10 دقائق

# نقطة نهاية ping لـ keep alive
@app.route('/ping', methods=['GET'])
def ping():
    return 'Bot is alive!', 200

def main():
    global application
    # قراءة الـ Token من متغير بيئي
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة")
        return

    application = Application.builder().token(bot_token).build()

    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lectures", lectures))
    application.add_handler(CommandHandler("exams", exams))
    application.add_handler(CommandHandler("notes", notes))

    # بدء خيط keep alive
    threading.Thread(target=keep_alive, daemon=True).start()

    # تشغيل Flask
    print("البوت يعمل...")
    app.run(host='0.0.0.0', port=8443)

if name == 'main':
    main()
