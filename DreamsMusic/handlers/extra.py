# handlers/extra.py
# Welcome new users in groups

async def welcome(client, message, lang):
    for new_user in message.new_chat_members:
        await message.reply(lang["welcome_message"].format(name=new_user.mention))
