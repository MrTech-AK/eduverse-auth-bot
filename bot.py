from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random, string, os

# Store tokens in memory (for demo)
tokens = {}

CHANNEL_USERNAME = "@EduVerse_Network"

def generate_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

    if chat_member.status not in ["member", "administrator", "creator"]:
        await update.message.reply_text("❗Please join our main channel first to get access.")
        return

    contact_btn = KeyboardButton("📞 Verify Yourself", request_contact=True)
    markup = ReplyKeyboardMarkup([[contact_btn]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please share your contact number to continue.", reply_markup=markup)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    token = generate_token()
    tokens[token] = contact.phone_number

    await update.message.reply_text(
        f"✅ Here is your token: `{token}`\nGo to page and paste it there.",
        parse_mode="Markdown"
    )

# App setup
BOT_TOKEN = os.environ.get("7733917285:AAFqPbB5VLV07SCnX-SwoMumPp9uQ_qWEsk")
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

if __name__ == '__main__':
    app.run_polling()
