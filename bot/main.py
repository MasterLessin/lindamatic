from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
)
from bot.utils.db import initialize_database
from bot.handlers.commands import help_command  # Import the help command
from bot.handlers.gates import setup_gate, handle_gate_selection, save_gate
from bot.handlers.registration import start_registration, handle_registration

# Initialize the database
initialize_database()

# Telegram Bot Token (Replace this with your bot token)
BOT_TOKEN = "7554597661:AAHazGKItoIF1w9NfftdJgbXhw5wmJFFN9g"

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot."""
    print(f"Error occurred: {context.error}")
    await update.message.reply_text("An error occurred. Please try again later.")

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

    # Add error handler
    app.add_error_handler(error_handler)

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setup_gate", setup_gate))  # Add the gate setup command
    app.add_handler(CommandHandler("register", start_registration))  # Add the registration start command

    # Callback Query Handlers
    app.add_handler(CallbackQueryHandler(handle_gate_selection, pattern="^gate_"))  # Handle gate selection

    # Registration Flow Handler (text messages for user input during registration)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_registration))

    # Save Gate Command
    app.add_handler(CommandHandler("save_gate", save_gate))  # Save the gate information

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
