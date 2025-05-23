import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "5000"))

if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("❌ تأكد من ضبط BOT_TOKEN و WEBHOOK_URL في متغيرات البيئة")
