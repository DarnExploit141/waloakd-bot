# =========================================
# WaloAkd Security Bot
# Telegram Pentesting Service Bot
# Python + pyTelegramBotAPI
# =========================================

import telebot
from telebot import types
from datetime import datetime
import os # جلب مكتبة النظام لقراءة المتغيرات

# =========================================
# BOT TOKEN & ADMIN ID (طريقة المتغيرات)
# =========================================
# سيقوم البوت بقراءة التوكن والأيدي من إعدادات Railway مباشرة
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 6343356275))

# التحقق من وجود التوكن لتجنب توقف البوت
if not TOKEN:
    raise ValueError("🚨 خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")

bot = telebot.TeleBot(TOKEN)

# =========================================
# START
# =========================================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🛡 الخدمات")
    btn2 = types.KeyboardButton("💰 الأسعار")
    btn3 = types.KeyboardButton("📩 طلب فحص")
    btn4 = types.KeyboardButton("📞 التواصل")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    text = f"""
👋 مرحباً بك في WaloAkd Security

خدمات احترافية في:
• Web Pentesting
• API Security Testing
• Vulnerability Assessment
• Security Reports

اختر من القائمة أدناه.
"""
    bot.send_message(message.chat.id, text, reply_markup=markup)

# =========================================
# SERVICES
# =========================================
@bot.message_handler(func=lambda m: m.text == "🛡 الخدمات")
def services(message):
    text = """
🛡 الخدمات المتوفرة

• Web Pentesting
• API Testing
• Vulnerability Assessment
• Security Reports PDF
• Security Consultation
"""
    bot.send_message(message.chat.id, text)

# =========================================
# PRICES
# =========================================
@bot.message_handler(func=lambda m: m.text == "💰 الأسعار")
def prices(message):
    text = """
💰 الأسعار

• فحص سريع — 5,000 IQD
• فحص متوسط — 15,000 IQD
• فحص متقدم — يبدأ من 25,000 IQD
"""
    bot.send_message(message.chat.id, text)

# =========================================
# CONTACT
# =========================================
@bot.message_handler(func=lambda m: m.text == "📞 التواصل")
def contact(message):
    text = """
📞 التواصل

Telegram:
@YOUR_USERNAME
"""
    bot.send_message(message.chat.id, text)

# =========================================
# REQUEST
# =========================================
@bot.message_handler(func=lambda m: m.text == "📩 طلب فحص")
def request(message):
    msg = bot.send_message(
        message.chat.id,
        """
📩 أرسل المعلومات التالية:

1- رابط الموقع
2- نوع الفحص
3- هل يوجد تصريح؟
4- ملاحظات إضافية
"""
    )
    bot.register_next_step_handler(msg, forward_request)

# =========================================
# FORWARD REQUEST TO ADMIN
# =========================================
def forward_request(message):
    user = message.from_user
    request_text = f"""
🚨 طلب فحص جديد

👤 الاسم:
{user.first_name}

🆔 اليوزر:
@{user.username}

📌 ID:
{user.id}

🕒 الوقت:
{datetime.now()}

📩 الطلب:
{message.text}
"""
    # إرسال إلى الأدمن (الأيدي الخاص بك)
    bot.send_message(ADMIN_ID, request_text)

    # رد على المستخدم
    bot.send_message(
        message.chat.id,
        "✅ تم إرسال طلبك بنجاح.\nسيتم التواصل معك قريباً."
    )

# =========================================
# UNKNOWN MESSAGE
# =========================================
@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(
        message.chat.id,
        "❌ اختر من الأزرار المتوفرة."
    )

# =========================================
# RUN BOT
# =========================================
print("Bot Running...")
bot.infinity_polling()