from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from bot.utils.db import initialize_database
from bot.handlers.commands import help_command  # Import the help command
from bot.handlers.gates import setup_gate, handle_gate_selection, save_gate


# Initialize the database
initialize_database()

# Telegram Bot Token (Replace this with your bot token)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the main menu to the user."""
    keyboard = [
        [InlineKeyboardButton("🔐 My Content", callback_data="my_content")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("🛠️ Help", callback_data="help")],
    ]
    await update.message.reply_text(
        "👋 Welcome to Lindamatic! Use the buttons below to navigate.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Callback Query Handler
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button interactions from the inline keyboard."""
    query = update.callback_query
    await query.answer()

    if query.data == "my_content":
        await query.edit_message_text("📝 You don't have any content yet!")
    elif query.data == "stats":
        await query.edit_message_text("📊 Stats feature is coming soon.")
    elif query.data == "help":
        await query.edit_message_text("🛠️ Contact @support for assistance.")

# Main Application
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setup_gate", setup_gate))  # Add the gate setup command
    app.add_handler(CallbackQueryHandler(handle_gate_selection, pattern="^gate_"))  # Handle gate selection
    app.add_handler(CommandHandler("save_gate", save_gate))  # Save the gate information

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
