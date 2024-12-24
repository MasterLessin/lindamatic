from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message to the user."""
    help_text = (
        "🛠️ *Help Menu*\n\n"
        "Here are the commands you can use:\n"
        "/start - Display the main menu\n"
        "/help - Show this help message\n"
        "/stats - View your stats (coming soon!)\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")
