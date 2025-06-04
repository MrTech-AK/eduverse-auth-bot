import telebot
import os
from datetime import datetime
import random
import string

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Main Channel Username
MAIN_CHANNEL = '@EduVerse_Network'

# Generate daily key
def generate_access_key():
    day = datetime.now().strftime("%a").upper()  # e.g., MON
    date = datetime.now().strftime("%-d%b").upper()  # e.g., 4JUN
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{day}-{date}/{rand_str}"

# Check membership in channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(MAIN_CHANNEL, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except Exception as e:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    full_name = message.from_user.first_name

    if is_user_in_channel(user_id):
        access_key = generate_access_key()
        bot.send_message(
            user_id,
            f"✅ *You are authorized to access the EduVerse site!*\n\n"
            f"🔐 *Your Access Key:*\n`{access_key}`\n\n"
            "_This key is valid only for today._",
            parse_mode="Markdown"
        )
    else:
        join_button = telebot.types.InlineKeyboardMarkup()
        join_button.add(
            telebot.types.InlineKeyboardButton("🚀 Join EduVerse Channel", url=f"https://t.me/{MAIN_CHANNEL[1:]}")
        )
        bot.send_message(
            user_id,
            "❌ *You're not a member of the EduVerse Network.*\n\n"
            "🔒 You must join the channel to access the website.",
            reply_markup=join_button,
            parse_mode="Markdown"
        )

print("🤖 Bot is running...")
bot.infinity_polling()
