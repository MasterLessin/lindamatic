
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils.db import get_db_connection

# List of Kenyan counties for registration
COUNTIES = [
    ["Nairobi", "Mombasa"],
    ["Kisumu", "Nakuru"],
    ["Kiambu", "Machakos"],
    ["Other"],
]

def start_registration(update: Update, context: CallbackContext):
    """Handles the /register command and starts the registration process."""
    user = update.message.from_user
    telegram_id = user.id

    # Check if the user is already registered
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        update.message.reply_text("✅ You are already registered!")
        return

    # Start the registration process
    update.message.reply_text(
        "👋 Welcome! Please send me your *First Name* to start registration.",
        parse_mode="Markdown",
    )

    # Set the bot's state to 'awaiting_first_name'
    context.user_data['registration_state'] = 'awaiting_first_name'
