from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import json

# A list of Kenyan counties
COUNTIES = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kiambu", "Uasin Gishu", 
    "Machakos", "Meru", "Nyeri", "Eldoret", "Kakamega", "Kericho"
]

# A temporary dictionary to store user registration states
user_registration_states = {}

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the registration process."""
    telegram_id = update.message.from_user.id
    user_registration_states[telegram_id] = {}  # Clear any previous registration state
    await update.message.reply_text("👤 Let's start your registration! What's your first name?")

async def handle_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the registration process."""
    telegram_id = update.message.from_user.id
    user_data = user_registration_states.get(telegram_id, None)

    if user_data is None:
        # If no state exists, restart the registration
        await start_registration(update, context)
        return

    # Determine what step of the registration the user is in
    if "first_name" not in user_data:
        user_data["first_name"] = update.message.text
        await update.message.reply_text("Great! What's your last name?")
    elif "last_name" not in user_data:
        user_data["last_name"] = update.message.text
        await update.message.reply_text("Got it! What's your phone number?")
    elif "phone_number" not in user_data:
        user_data["phone_number"] = update.message.text
        await update.message.reply_text("Please provide your email address.")
    elif "email" not in user_data:
        user_data["email"] = update.message.text

        # Display county options
        keyboard = [
            [InlineKeyboardButton(county, callback_data=f"county_{county}")] for county in COUNTIES
        ]
        await update.message.reply_text(
            "Which county are you in? Select from the list below:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("⚠️ Unexpected input. Please try again.")

async def handle_county_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the county selection."""
    query = update.callback_query
    telegram_id = query.from_user.id

    # Extract county from callback data
    county = query.data.replace("county_", "")
    user_data = user_registration_states.get(telegram_id, None)

    if user_data is not None:
        user_data["county"] = county

        # Save registration data to the database
        from bot.utils.db import save_user_to_db
        save_user_to_db(
            telegram_id=telegram_id,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone_number=user_data["phone_number"],
            email=user_data["email"],
            county=user_data["county"]
        )
        await query.edit_message_text("✅ Registration completed successfully! 🎉")
        del user_registration_states[telegram_id]  # Clear state after completion
    else:
        await query.edit_message_text("⚠️ Something went wrong. Please try /register again.")
