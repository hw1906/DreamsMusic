# utils/maintenance_util.py
# Maintenance mode toggle and check

maintenance = False

async def maintenance_toggle(client, message):
    global maintenance
    text = message.text.lower()
    if "/maintenance enable" in text:
        maintenance = True
        await message.reply("Maintenance mode enabled. Bot will not play music.")
    elif "/maintenance disable" in text:
        maintenance = False
        await message.reply("Maintenance mode disabled. Bot is back online.")

def is_maintenance():
    return maintenance
