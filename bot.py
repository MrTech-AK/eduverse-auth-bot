import telebot
from datetime import datetime
import random
import string
import hmac
import hashlib
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8040947061:AAH2q44giCsPOOp1-hWSWHSwQsQj6WQigtY'
CHANNELS = ['@EduVerse_Network', '@Topperz_Vault']  # ✅ Multiple channels
SECRET_KEY = b'EDUVERSE2025'

bot = telebot.TeleBot(API_TOKEN)

def generate_hmac_token():
    now = datetime.now()
    day = now.strftime("%a").upper()
    date = now.strftime("%d%b").upper()
    base_token = f"{day}-{date}"
    hmac_token = hmac.new(SECRET_KEY, base_token.encode(), hashlib.sha256).hexdigest()[:8].upper()
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{hmac_token}/{random_suffix}"

def is_user_in_all_channels(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    send_verification_prompt(message.chat.id, user_id)

@bot.callback_query_handler(func=lambda call: call.data == 'verify_now')
def verify_button_pressed(call):
    user_id = call.from_user.id
    if is_user_in_all_channels(user_id):
        token = generate_hmac_token()
        bot.send_message(call.message.chat.id,
            f"✅ *You are verified!*\n\n"
            f"🔑 *Token:* `{token}`\n"
            f"📅 Valid only for *today*\n\n"
            f"👉 Paste it at https://eduverse-official.netlify.app/main",
            parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "🚫 You haven't joined all channels yet!\nPlease Join Them to get your *Website Access Key*", show_alert=True)

def send_verification_prompt(chat_id, user_id):
    if not is_user_in_all_channels(user_id):
        markup = InlineKeyboardMarkup()
        for ch in CHANNELS:
            markup.add(InlineKeyboardButton(f"🔗 Join {ch}", url=f"https://t.me/{ch.strip('@')}"))
        markup.add(InlineKeyboardButton("✅ I Joined", callback_data="verify_now"))

        bot.send_message(chat_id,
            "🚫 *Website Access Denied!*\n\n"
            "⚠️ You must join all the required channels below to continue.",
            parse_mode="Markdown",
            reply_markup=markup)
    else:
        token = generate_hmac_token()
        bot.send_message(chat_id,
            f"✅ *You are verified!*\n\n"
            f"🔑 *Token:* `{token}`\n"
            f"📅 Valid only for *Today*\n\n"
            f"👉 Paste it at https://eduverse-official.netlify.app/main",
            parse_mode="Markdown")

bot.infinity_polling()
