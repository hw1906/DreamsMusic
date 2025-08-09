# handlers/start.py
# Handles /start command - sends welcome message

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start(client, message, lang):
    text = lang["start_message"]
    buttons = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Support", url="https://t.me/DreamsSupport")]
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))
