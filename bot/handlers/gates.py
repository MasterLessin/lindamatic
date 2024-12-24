from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
from bot.utils.db import get_db_connection

async def setup_gate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to set up a social gate."""
    keyboard = [
        [InlineKeyboardButton("Instagram", callback_data="gate_instagram")],
        [InlineKeyboardButton("TikTok", callback_data="gate_tiktok")],
        [InlineKeyboardButton("Facebook", callback_data="gate_facebook")],
        [InlineKeyboardButton("YouTube", callback_data="gate_youtube")],
        [InlineKeyboardButton("Telegram", callback_data="gate_telegram")],
        [InlineKeyboardButton("Email", callback_data="gate_email")],
    ]
    await update.message.reply_text(
        "🔒 Select the social gate you want to set up:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_gate_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles social gate selection."""
    query = update.callback_query
    await query.answer()

    gate_type = query.data.split("_")[1]  # Extract gate type (e.g., 'instagram')
    context.user_data['gate_type'] = gate_type

    # Ask for the required value (e.g., username, group link)
    if gate_type in ["instagram", "tiktok", "facebook", "youtube"]:
        await query.edit_message_text(
            f"💡 Enter the username or profile link for the {gate_type.capitalize()} gate:"
        )
    elif gate_type == "telegram":
        await query.edit_message_text(
            "💡 Enter the Telegram group/channel invite link:"
        )
    elif gate_type == "email":
        await query.edit_message_text(
            "💡 Enter the email address required for verification:"
        )

async def save_gate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saves the social gate information to the database."""
    gate_type = context.user_data.get('gate_type')
    gate_value = update.message.text  # The user's input

    if not gate_type or not gate_value:
        await update.message.reply_text("❌ Invalid input. Please try again.")
        return

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO content (client_id, type, value, gate_type, gate_value)
        VALUES (?, ?, ?, ?, ?)
        ''', (1, "link", "locked", gate_type, gate_value))  # Replace `1` with the actual client_id
        conn.commit()

    await update.message.reply_text(
        f"✅ {gate_type.capitalize()} gate has been set up successfully!"
    )
