import telebot
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio

# بياناتك الخاصة
TOKEN = "8435266080:AAFwdKp1aMEqbiJeqe6SxO-uze52WKdfMKA"
API_ID = 31041524
API_HASH = 'fc223a5488d8742724d4104f63d63463'
ADMIN_ID = 8253672033

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "✅ البوت يعمل الآن من السيرفر! أرسل الرقم:")

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    if message.from_user.id != ADMIN_ID: return
    chat_id = message.chat.id
    if chat_id not in user_data:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        try:
            loop.run_until_complete(client.connect())
            send_code = loop.run_until_complete(client.send_code_request(message.text))
            user_data[chat_id] = {'client': client, 'phone': message.text, 'hash': send_code.phone_code_hash, 'loop': loop}
            bot.send_message(chat_id, "📩 أرسل كود التحقق:")
        except Exception as e:
            bot.send_message(chat_id, f"❌ خطأ: {e}")
    else:
        data = user_data[chat_id]
        try:
            data['loop'].run_until_complete(data['client'].sign_in(data['phone'], message.text, phone_code_hash=data['hash']))
            bot.send_message(chat_id, f"✅ الجلسة:\n`{data['client'].session.save()}`", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(chat_id, f"❌ فشل: {e}")
        finally:
            data['loop'].run_until_complete(data['client'].disconnect())
            del user_data[chat_id]

bot.infinity_polling()
