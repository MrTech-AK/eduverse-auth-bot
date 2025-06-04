import telebot
from datetime import datetime
import random
import string
import hmac
import hashlib
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7733917285:AAFqPbB5VLV07SCnX-SwoMumPp9uQ_qWEsk'
CHANNEL_USERNAME = '@EduVerse_Network'
SECRET_KEY = b'EDUVERSE2025'  # bytes key

bot = telebot.TeleBot(API_TOKEN)

def generate_hmac_token():
    now = datetime.now()
    day = now.strftime("%a").upper()       # MON
    date = now.strftime("%d%b").upper()    # 03JUN
    base_token = f"{day}-{date}"           # MON-03JUN

    hmac_token = hmac.new(SECRET_KEY, base_token.encode(), hashlib.sha256).hexdigest()[:8].upper()

    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    full_token = f"{hmac_token}/{random_suffix}"
    return full_token

def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def welcome_user(message):
    user_id = message.from_user.id

    if not is_user_in_channel(user_id):
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton("🔗 Join EduVerse Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")
        markup.add(btn)

        bot.send_message(message.chat.id,
            "🚫 *Access Denied!*\n\n"
            "⚠️ You must join our official channel to continue.\n"
            "🔓 Join and come back!",
            parse_mode="Markdown",
            reply_markup=markup
        )
    else:
        token = generate_hmac_token()
        bot.send_message(message.chat.id,
            f"✅ *You are verified!*\n\n"
            f"🔑 *Token:* `{token}`\n"
            "📅 Valid only for *today*\n\n"
            "👉 Paste it at https://eduverse-official.netlify.app/verify",
            parse_mode="Markdown"
        )

bot.infinity_polling()
