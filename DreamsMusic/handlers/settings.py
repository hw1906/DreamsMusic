from DreamsMusic.utils.language_util import get_chat_language

async def settings(client, message):
    chat_id = message.chat.id
    lang = get_chat_language(chat_id)

    # Load language dictionary depending on lang
    texts = {
        "no_query": {
            "english": "Please provide a song name or URL to play.",
            "hindi": "कृपया बजाने के लिए गाने का नाम या यूआरएल दें।"
        },
        # add more messages here
    }

    if no_query_condition:
        await message.reply(texts["no_query"][lang])
