import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
load_dotenv()

# Defining the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # The keyboard commands
    url = os.getenv('TELEGRAM_URL')
    url2 = os.getenv('WEBSITE_URL')
    keyboard = [
        [InlineKeyboardButton("Join our Community", url=url)],
        [InlineKeyboardButton("Visit our website", url=url2)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)

# The button callback
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == '1':
        await query.edit_message_text(text="You clicked Button 1")
    elif query.data == '2':
        await query.edit_message_text(text="You clicked Button 2")

def mainFunc():
    token = os.getenv("BOT_ID")

    if not token:
        logger.error("Bot token is missing! Make sure it's set in your .env file.")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    logger.info("Bot is starting...")
    application.run_polling()


