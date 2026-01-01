import telebot
from telethon import TelegramClient, errors
import sqlite3, os, asyncio

# --- ضع بياناتك هنا ---
TOKEN = "8283286308:AAGTHqVl-BOSFI5TcfFWKSLKjsKAKghdkF4"
API_ID = 31041524
API_HASH = 'fc223a5488d8742724d4104f63d63463'
ADMIN_ID = 8253672033

bot = telebot.TeleBot(TOKEN)

# التأكد من وجود مجلد للجلسات
if not os.path.exists('sessions'): os.makedirs('sessions')

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("➕ إضافة جلسة جديدة")
        bot.send_message(message.chat.id, "✅ البوت يعمل الآن على Koyeb باتصال مباشر!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "➕ إضافة جلسة جديدة")
def ask_phone(message):
    msg = bot.send_message(message.chat.id, "📱 أرسل الرقم (مثال: +964xxx):")
    bot.register_next_step_handler(msg, process_phone)

def process_phone(message):
    phone = message.text.replace(" ", "")
    client = TelegramClient(f"sessions/{phone}", API_ID, API_HASH)
    
    async def run_auth():
        try:
            await client.connect()
            await client.send_code_request(phone)
            bot.send_message(message.chat.id, "📩 أرسل الكود الآن:")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ خطأ في الاتصال: {e}")

    asyncio.run(run_auth())

bot.infinity_polling()
