import os
from dotenv import load_dotenv

# تحميل المتغيرات من .env في بيئة التطوير
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "5000"))  # 5000 كخيار افتراضي لتوافق مع Render

# تحقق من القيم
if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("يرجى تحديد BOT_TOKEN و WEBHOOK_URL في البيئة أو ملف .env")
