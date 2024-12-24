from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.db import get_db_connection
import json

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the registration process by asking for user details."""
    user = update.message.from_user
    # Store the user's Telegram ID in the context for later use
    context.user_data['telegram_id'] = user.id
    await update.message.reply_text("Please provide your first name:")

async def handle_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the user's input during registration."""
    user_input = update.message.text
    telegram_id = context.user_data.get('telegram_id')

    # Handle first name
    if 'first_name' not in context.user_data:
        context.user_data['first_name'] = user_input
        await update.message.reply_text(f"Got it, {user_input}. Now, please provide your last name:")
        return

    # Handle last name
    if 'last_name' not in context.user_data:
        context.user_data['last_name'] = user_input
        await update.message.reply_text(f"Great! Now, please provide your phone number:")
        return

    # Handle phone number
    if 'phone_number' not in context.user_data:
        context.user_data['phone_number'] = user_input
        await update.message.reply_text("Thanks! Now, please provide your email:")
        return

    # Handle email
    if 'email' not in context.user_data:
        context.user_data['email'] = user_input
        await update.message.reply_text("Thanks! Now, please choose your county from the list below:")

        # Send a list of counties (simplified example)
        counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru"]
        keyboard = [[county] for county in counties]
        await update.message.reply_text("Select your county:", reply_markup=keyboard)
        return

    # Handle county selection
    if 'county' not in context.user_data:
        context.user_data['county'] = user_input
        # Store the user's details in the database
        await save_user_registration(context.user_data)
        await update.message.reply_text(f"Registration complete! Welcome {context.user_data['first_name']}!")
        return

async def save_user_registration(user_data):
    """Save the user's registration details to the database."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert into the users table
    cursor.execute('''
        INSERT INTO users (telegram_id, username, first_name, last_name, phone_number, email, county)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_data['telegram_id'],
        user_data.get('username', ''),
        user_data['first_name'],
        user_data['last_name'],
        user_data['phone_number'],
        user_data['email'],
        user_data['county']
    ))

    connection.commit()
    connection.close()
