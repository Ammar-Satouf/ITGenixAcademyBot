from telegram import Update
from telegram.ext import ContextTypes
from resources import resources

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        "مرحبًا! أنا بوت دراسة الهندسة المعلوماتية 🖥\n"
        "استخدم الأوامر التالية:\n"
        "/lectures [year] [semester] [type]\n"
        "/exams [year] [semester] [type]\n"
        "/notes [year] [semester] [type]\n"
        "استبدل [year] بـ 1، [semester] بـ 1 أو 2، و[type] بـ practical أو theoretical\n"
        "/help - لعرض التعليمات"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        "تعليمات الاستخدام:\n"
        "/lectures 1 1 practical - لمحاضرات المواد العملية\n"
        "/exams 1 2 theoretical - لأسئلة المواد النظرية\n"
        "/notes 1 1 practical - لملاحظات المواد العملية"
    )

async def lectures(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    args = context.args or []
    if len(args) < 3:
        await update.effective_message.reply_text("يرجى إدخال السنة، الفصل، ونوع المادة. مثال: /lectures 1 1 practical")
        return
    year, semester, subject_type = args[0], args[1], args[2]
    if year in resources and semester in resources[year] and subject_type in resources[year][semester]:
        response = "محاضرات:\n"
        for subject, data in resources[year][semester][subject_type].items():
            response += f"- {subject}: {data['lectures']}\n"
        await update.effective_message.reply_text(response)
    else:
        await update.effective_message.reply_text("خطأ: تحقق من السنة أو الفصل أو نوع المادة")

async def exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    args = context.args or []
    if len(args) < 3:
        await update.effective_message.reply_text("يرجى إدخال السنة، الفصل، ونوع المادة. مثال: /exams 1 1 practical")
        return
    year, semester, subject_type = args[0], args[1], args[2]
    if year in resources and semester in resources[year] and subject_type in resources[year][semester]:
        response = "أسئلة الامتحانات:\n"
        for subject, data in resources[year][semester][subject_type].items():
            response += f"- {subject}: {data['exams']}\n"
        await update.effective_message.reply_text(response)
    else:
        await update.effective_message.reply_text("خطأ: تحقق من السنة أو الفصل أو نوع المادة")

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    args = context.args or []
    if len(args) < 3:
        await update.effective_message.reply_text("يرجى إدخال السنة، الفصل، ونوع المادة. مثال: /notes 1 1 practical")
        return
    year, semester, subject_type = args[0], args[1], args[2]
    if year in resources and semester in resources[year] and subject_type in resources[year][semester]:
        response = "ملاحظات هامة:\n"
        for subject, data in resources[year][semester][subject_type].items():
            response += f"- {subject}: {data['notes']}\n"
        await update.effective_message.reply_text(response)
    else:
        await update.effective_message.reply_text("خطأ: تحقق من السنة أو الفصل أو نوع المادة")
