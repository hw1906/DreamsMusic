# handlers/stats.py
# Sends uptime, user count, chat count stats (static placeholders)

async def stats(client, message, lang):
    text = lang["stats_message"].format(uptime="1h23m", users=1234, chats=56)
    await message.reply(text)
