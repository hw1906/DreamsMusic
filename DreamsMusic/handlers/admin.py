# handlers/admin.py
# Handles admin commands: pause, resume, stop, skip, end

from pyrogram.types import Message

async def handle_commands(client, message: Message, lang):
    cmd = message.text.lower().split()[0][1:]
    if cmd == "pause":
        await message.reply(lang["paused"])
    elif cmd == "resume":
        await message.reply(lang["resumed"])
    elif cmd == "stop":
        await message.reply(lang["stopped"])
    elif cmd == "skip":
        await message.reply(lang["skipped"])
    elif cmd == "end":
        await message.reply(lang["ended"])
    else:
        await message.reply(lang["unknown_command"])
