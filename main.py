
import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.get("/")
def home():
    return "Cyber Guardian EG is running!"

@app.post("/telegram")
def telegram_webhook():
    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "").strip()

    if not chat_id:
        return {"ok": True}

    if text == "/start":
        reply = (
            "أهلاً بيك في Cyber Guardian EG 🛡️\n\n"
            "اختار خدمة:\n"
            "/help - المساعدة\n"
            "/security - نصائح حماية الحسابات\n"
            "/tools - أدوات أمن سيبراني آمنة"
        )
    elif text == "/help":
        reply = "ابعت /security للحماية أو /tools لقائمة الأدوات."
    elif text == "/security":
        reply = (
            "🔐 نصائح حماية:\n"
            "1. استخدم كلمة مرور فريدة.\n"
            "2. فعّل التحقق بخطوتين.\n"
            "3. لا تشارك رموز الدخول.\n"
            "4. افحص الروابط قبل فتحها."
        )
    elif text == "/tools":
        reply = (
            "🛡️ أدوات للتعلّم والاختبار المصرّح:\n"
            "• OWASP ZAP لفحص مواقعك.\n"
            "• OWASP Juice Shop للتدريب.\n"
            "• VirusTotal لفحص الملفات والروابط."
        )
    else:
        reply = "مش فاهم الأمر. ابعت /help لعرض الأوامر."

    if BOT_TOKEN:
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": reply},
            timeout=15
        )

    return {"ok": True}
      
