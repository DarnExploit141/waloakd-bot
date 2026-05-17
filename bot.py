# =========================================
# WaloAkd Security Bot
# Telegram Pentesting Service Bot
# Python + pyTelegramBotAPI
# =========================================

import telebot
from telebot import types
from datetime import datetime
import os

# =========================================
# BOT TOKEN & ADMIN ID (طريقة المتغيرات الآمنة)
# =========================================
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 6343356275)) # الأيدي الخاص بك كقيمة احتياطية

if not TOKEN:
    # ملاحظة: عند التجربة محلياً على جهازك قبل الرفع لـ Railway، 
    # يمكنك وضع التوكن مؤقتاً هنا بدلاً من الـ raise لو أردت الاختيار المحلي.
    raise ValueError("🚨 خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")

bot = telebot.TeleBot(TOKEN)

# =========================================
# دوال الكيبورد (قوالب الأزرار)
# =========================================
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🛡 الخدمات")
    btn2 = types.KeyboardButton("💰 الأسعار")
    btn3 = types.KeyboardButton("📩 طلب فحص")
    btn4 = types.KeyboardButton("📞 التواصل")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

def get_cancel_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ إلغاء الطلب"))
    return markup

# =========================================
# ذاكرة مؤقتة لحفظ مسار الأسئلة
# =========================================
user_requests = {}

# =========================================
# START
# =========================================
@bot.message_handler(commands=['start'])
def start(message):
    text = f"""
👋 مرحباً بك في WaloAkd Security

خدمات احترافية في:
• Web Pentesting
• API Security Testing
• Vulnerability Assessment
• Security Reports

اختر من القائمة أدناه.
"""
    bot.send_message(message.chat.id, text, reply_markup=get_main_markup())

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
# REQUEST (الطلب خطوة بخطوة)
# =========================================
@bot.message_handler(func=lambda m: m.text == "📩 طلب فحص")
def request_start(message):
    chat_id = message.chat.id
    user_requests[chat_id] = {} 
    
    msg = bot.send_message(
        chat_id, 
        "🔗 ممتاز! يرجى إرسال **رابط الموقع** أو الـ IP المراد فحصه:", 
        parse_mode="Markdown",
        reply_markup=get_cancel_markup()
    )
    bot.register_next_step_handler(msg, process_url_step)

def process_url_step(message):
    chat_id = message.chat.id
    
    if message.text == "❌ إلغاء الطلب":
        bot.send_message(chat_id, "🚫 تم إلغاء الطلب بنجاح.", reply_markup=get_main_markup())
        user_requests.pop(chat_id, None)
        return

    user_requests[chat_id]['url'] = message.text
    msg = bot.send_message(
        chat_id, 
        "🛠️ ما هو **نوع الفحص** المطلوب؟\n(مثال: فحص سريع، فحص واجهات API، فحص شامل...)", 
        parse_mode="Markdown",
        reply_markup=get_cancel_markup()
    )
    bot.register_next_step_handler(msg, process_type_step)

def process_type_step(message):
    chat_id = message.chat.id
    
    if message.text == "❌ إلغاء الطلب":
        bot.send_message(chat_id, "🚫 تم إلغاء الطلب بنجاح.", reply_markup=get_main_markup())
        user_requests.pop(chat_id, None)
        return

    user_requests[chat_id]['type'] = message.text
    msg = bot.send_message(
        chat_id, 
        "⚖️ هل تملك **تصريحاً رسمياً** (Authorization) لفحص هذا الهدف؟\n(نعم / لا)", 
        parse_mode="Markdown",
        reply_markup=get_cancel_markup()
    )
    bot.register_next_step_handler(msg, process_auth_step)

def process_auth_step(message):
    chat_id = message.chat.id
    
    if message.text == "❌ إلغاء الطلب":
        bot.send_message(chat_id, "🚫 تم إلغاء الطلب بنجاح.", reply_markup=get_main_markup())
        user_requests.pop(chat_id, None)
        return

    user_requests[chat_id]['auth'] = message.text
    msg = bot.send_message(
        chat_id, 
        "📝 هل لديك أي **ملاحظات إضافية**؟\n(إذا لم يوجد، اكتب 'لا يوجد')", 
        parse_mode="Markdown",
        reply_markup=get_cancel_markup()
    )
    bot.register_next_step_handler(msg, process_final_step)

def process_final_step(message):
    chat_id = message.chat.id
    user = message.from_user
    
    if message.text == "❌ إلغاء الطلب":
        bot.send_message(chat_id, "🚫 تم إلغاء الطلب بنجاح.", reply_markup=get_main_markup())
        user_requests.pop(chat_id, None)
        return

    user_requests[chat_id]['notes'] = message.text
    data = user_requests[chat_id]
    
    # تنسيق رسالة التقرير للأدمن
    request_text = f"""
🚨 **طلب فحص جديد مكتمل** 🚨

👤 **الاسم:** {user.first_name}
🆔 **اليوزر:** @{user.username if user.username else 'لا يوجد'}
📌 **ID:** {user.id}
🕒 **الوقت:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🌐 **الرابط/الهدف:** {data['url']}
🛠️ **نوع الفحص:** {data['type']}
⚖️ **التصريح:** {data['auth']}
📝 **ملاحظات:** {data['notes']}
"""

    bot.send_message(ADMIN_ID, request_text)

    bot.send_message(
        chat_id, 
        "✅ **تم استلام طلبك بالكامل وبنجاح!**\nسيقوم الفريق بمراجعة التفاصيل والتواصل معك قريباً.", 
        parse_mode="Markdown",
        reply_markup=get_main_markup()
    )
    
    user_requests.pop(chat_id, None)

# =========================================
# UNKNOWN MESSAGE
# =========================================
@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(
        message.chat.id,
        "❌ اختر من الأزرار المتوفرة.",
        reply_markup=get_main_markup()
    )

# =========================================
# RUN BOT
# =========================================
print("Bot Running...")
bot.infinity_polling()
