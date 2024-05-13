import re

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_ID = os.getenv("APP_ID")
API_HASH = os.getenv("API_HASH")

bot = Client(
    "replacer",
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@bot.on_message(filters.command('replace'))
async def replace_button_text(client, message):
    chat_id = message.chat.id
    message_id = message.reply_to_message.id
    old_bot_name = message.command[1]
    new_bot_name = message.command[2]

    message = message.reply_to_message
    new_keyboard = []
    for button in message.reply_markup.inline_keyboard:
        new_row = []
        for inline_button in button:
            if re.search(old_bot_name, inline_button.url):
                new_url = re.sub(old_bot_name, new_bot_name, inline_button.url)
                new_inline_button = InlineKeyboardButton(
                    text=inline_button.text, url=new_url)
                new_row.append(new_inline_button)
            else:
                new_row.append(inline_button)
        new_keyboard.append(new_row)

    # Check if the replied message is a photo
    if message.photo:
        caption = message.caption
    else:
        caption = message.text

    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=caption,
        reply_markup=InlineKeyboardMarkup(new_keyboard))


print("The Bot is Now Online!!!!")
bot.run()
