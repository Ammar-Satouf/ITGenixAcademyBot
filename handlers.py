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

def validate_args(args):
    if len(args) < 3:
        return False, "يرجى إدخال السنة، الفصل، ونوع المادة. مثال: /command 1 1 practical"
    year, semester, subject_type = args[0], args[1], args[2]
    if year not in resources or semester not in resources[year] or subject_type not in resources[year][semester]:
        return False, "خطأ: تحقق من السنة أو الفصل أو نوع المادة"
    return True, (year, semester, subject_type)

async def lectures(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    args = context.args or []
    valid, result = validate_args(args)
    if not valid:
        await update.effective_message.reply_text(result)
        return
    year, semester, subject_type = result
    response = "محاضرات:\n"
    for subject, data in resources[year][semester][subject_type].items():
        response += f"- {subject}: {data.get('lectures', 'لا توجد محاضرات')}\n"
    await update.effective_message.reply_text(response)

async def exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    args = context.args or []
    valid, result = validate_args(args)
    if not valid:
        await update.effective_message.reply_text(result)
        return
    year, semester, subject_type = result
    response = "أسئلة الامتحانات:\n"
    for subject, data in resources[year][semester][subject_type].items():
        response += f"- {subject}: {data.get('exams', 'لا توجد أسئلة')}\n"
    await update.effective_message.reply_text(response)

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    args = context.args or []
    valid, result = validate_args(args)
    if not valid:
        await update.effective_message.reply_text(result)
        return
    year, semester, subject_type = result
    response = "ملاحظات هامة:\n"
    for subject, data in resources[year][semester][subject_type].items():
        response += f"- {subject}: {data.get('notes', 'لا توجد ملاحظات')}\n"
    await update.effective_message.reply_text(response)
