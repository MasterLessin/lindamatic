
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

def handle_registration(update: Update, context: CallbackContext):
    """Handles user responses during the registration process."""
    state = context.user_data.get('registration_state', None)
    user = update.message.from_user
    telegram_id = user.id
    text = update.message.text

    if state == 'awaiting_first_name':
        context.user_data['first_name'] = text
        context.user_data['registration_state'] = 'awaiting_last_name'
        update.message.reply_text("Great! Now send me your *Last Name*.", parse_mode="Markdown")
    elif state == 'awaiting_last_name':
        context.user_data['last_name'] = text
        context.user_data['registration_state'] = 'awaiting_phone_number'
        update.message.reply_text("Thanks! What's your *Phone Number*?", parse_mode="Markdown")
    elif state == 'awaiting_phone_number':
        context.user_data['phone_number'] = text
        context.user_data['registration_state'] = 'awaiting_email'
        update.message.reply_text("Got it! Please send me your *Email Address*.", parse_mode="Markdown")
    elif state == 'awaiting_email':
        context.user_data['email'] = text
        context.user_data['registration_state'] = 'awaiting_county'
        update.message.reply_text(
            "Perfect! Now, select your *County* from the options below:",
            reply_markup=ReplyKeyboardMarkup(COUNTIES, one_time_keyboard=True, resize_keyboard=True),
            parse_mode="Markdown",
        )
    elif state == 'awaiting_county':
        context.user_data['county'] = text
        # Save the data to the database
        save_user_to_db(telegram_id, context.user_data)

        # Clear the registration state
        context.user_data.clear()
        update.message.reply_text("🎉 Registration complete! Welcome aboard!")
    else:
        update.message.reply_text("Please use /register to start the registration process.")

def save_user_to_db(telegram_id, user_data):
    """Saves user data to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (telegram_id, first_name, last_name, username, phone_number, email, county)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        telegram_id,
        user_data.get('first_name'),
        user_data.get('last_name'),
        user_data.get('username'),
        user_data.get('phone_number'),
        user_data.get('email'),
        user_data.get('county'),
    ))
    conn.commit()
    conn.close()
