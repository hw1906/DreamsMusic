# utils/maintenance_util.py
# Toggle maintenance mode on/off

maintenance = False

async def maintenance_toggle(client, message):
    global maintenance
    cmd = message.text.lower()
    if cmd == "/maintenance":
        maintenance = True
        await message.reply("Maintenance mode enabled. Bot is now offline for users.")
    elif cmd == "/unmaintenance":
        maintenance = False
        await message.reply("Maintenance mode disabled. Bot is now online.")

def is_maintenance():
    return maintenance
