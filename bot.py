import telebot
import os
from datetime import datetime
import random
import string

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

MAIN_CHANNEL = '@EduVerse_Network'
EXTRA_CHANNEL = '@TopperZ_Vault'

def generate_access_key():
    day = datetime.now().strftime("%a").upper()
    date = datetime.now().strftime("%-d%b").upper()
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{day}-{date}/{rand_str}"

def is_user_in_channel(user_id):
    try:
        main = bot.get_chat_member(MAIN_CHANNEL, user_id)
        extra = bot.get_chat_member(EXTRA_CHANNEL, user_id)
        return (main.status in ['member', 'administrator', 'creator'] and
                extra.status in ['member', 'administrator', 'creator'])
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    show_join_prompt(user_id)

@bot.callback_query_handler(func=lambda call: call.data == 'check_join')
def check_join_status(call):
    user_id = call.from_user.id
    if is_user_in_channel(user_id):
        access_key = generate_access_key()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ *You are now authorized!*\n\n🔐 Your Access Key:\n`{access_key}`\n\n_Use it on the EduVerse website._",
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "❌ You're still not in both channels!", show_alert=True)

def show_join_prompt(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("📢 Join Main Channel", url=f"https://t.me/{MAIN_CHANNEL[1:]}"),
        telebot.types.InlineKeyboardButton("📰 Join Updates Channel", url=f"https://t.me/{EXTRA_CHANNEL[1:]}")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("✅ I Joined", callback_data="check_join")
    )
    bot.send_message(
        user_id,
        "🚫 *Access Denied:*\nYou need to join both channels to access the EduVerse site.\n\nOnce you've joined, click the ✅ button below.",
        reply_markup=markup,
        parse_mode="Markdown"
    )

print("🤖 Bot running with channel check + join confirmation...")
bot.infinity_polling()
