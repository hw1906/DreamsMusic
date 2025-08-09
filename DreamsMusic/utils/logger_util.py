# utils/logger_util.py
# Toggle logging status

logging_enabled = False

async def logger_toggle(client, message):
    global logging_enabled
    logging_enabled = not logging_enabled
    status = "enabled" if logging_enabled else "disabled"
    await message.reply(f"Logger {status}.")
