import os
from dotenv import load_dotenv

# تحميل المتغيرات من .env (في حالة التشغيل محليًا)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "5000"))  # 5000 افتراضي للتوافق مع Render

# تحقق من وجود القيم الأساسية
if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("❌ تأكد من ضبط BOT_TOKEN و WEBHOOK_URL في متغيرات البيئة أو ملف .env")
