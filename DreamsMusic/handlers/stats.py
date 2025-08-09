import psutil
import platform
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import STATS_IMAGE_URL

import importlib.metadata

# Dummy DB functions — REPLACE these with your actual DB queries!
async def get_served_chats_count():
    # Example: return await db.chats.count_documents({})
    return 12

async def get_served_users_count():
    # Example: return await db.users.count_documents({})
    return 10

async def get_blocked_users_count():
    # Example: return await db.blocked_users.count_documents({})
    return 0

async def get_sudo_users_count():
    # Example: return await db.sudo_users.count_documents({})
    return 3

async def get_db_size_mb():
    # Example: calculate your DB size in MB
    return 1.98

async def get_db_storage_mb():
    # Example: your DB allocated storage in MB
    return 252.0

async def get_db_collections_count():
    # Example: your DB collection count
    return 7

async def get_db_keys_count():
    # Example: number of keys/indexes
    return 44

def get_python_version():
    return sys.version.split()[0]

def get_platform_info():
    return platform.system()

def get_cpu_freq():
    freq = psutil.cpu_freq()
    return freq.current / 1000 if freq else 0  # GHz

def get_cpu_cores():
    return psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)

def get_ram_info():
    mem = psutil.virtual_memory()
    return mem.total / (1024**3), mem.used / (1024**3), mem.available / (1024**3)  # in GB

def get_disk_info():
    disk = psutil.disk_usage('/')
    return disk.total / (1024**3), disk.used / (1024**3), disk.free / (1024**3)  # in GB

def get_package_version(pkg_name):
    try:
        return importlib.metadata.version(pkg_name)
    except importlib.metadata.PackageNotFoundError:
        return "Unknown"

# Async function to build general stats string
async def build_general_stats():
    total_ram, used_ram, free_ram = get_ram_info()
    total_disk, used_disk, free_disk = get_disk_info()
    physical_cores, total_cores = get_cpu_cores()
    cpu_freq = get_cpu_freq()
    platform_name = get_platform_info()
    python_ver = get_python_version()
    pyrogram_ver = get_package_version("pyrogram")
    pytgcalls_ver = get_package_version("pytgcalls")

    db_size = await get_db_size_mb()
    db_storage = await get_db_storage_mb()
    db_collections = await get_db_collections_count()
    db_keys = await get_db_keys_count()

    served_chats = await get_served_chats_count()
    served_users = await get_served_users_count()
    blocked_users = await get_blocked_users_count()
    sudo_users = await get_sudo_users_count()

    stats_text = f"""\
𝖬𝗈𝖽𝗎𝗅𝖾𝗌 : 39
𝖯𝗅𝖺𝗍𝖿𝗈𝗋𝗆𝗌 : {platform_name}
𝖱𝖠𝖬 : {total_ram:.2f} ɢʙ
𝖯𝗁𝗒𝗌𝗂𝖼𝖺𝗅 𝖢𝗈𝗋𝖾𝗌 : {physical_cores}
𝖳𝗈𝗍𝖺𝗅 𝖢𝗈𝗋𝖾𝗌 : {total_cores}
𝖢𝖯𝖴 𝖥𝗋𝖾𝗊𝗎𝖾𝗓𝗇𝖼𝗒 : {cpu_freq:.2f} ɢʜᴢ

𝖯𝗒𝗍𝗁𝗈𝗇 : {python_ver}
𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆 : {pyrogram_ver}
𝖯𝗒-𝖳𝗀𝖼𝖺𝗅𝗅𝗌 : {pytgcalls_ver}

𝖲𝗍𝗈𝗋𝖺𝗀𝖾 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 : {total_disk:.2f} ɢɪʙ
𝖲𝗍𝗈𝗋𝖺𝗀𝖾 𝖴𝗌𝖾𝖽 : {used_disk:.2f} ɢɪʙ
𝖲𝗍𝗈𝗋𝖺𝗀𝖾 𝖫𝖾𝖿𝗍 : {free_disk:.2f} ɢɪʙ

𝖲𝖾𝗋𝗏𝖾𝖽 𝖢𝗁𝖺𝗍𝗌 : {served_chats}
𝖲𝖾𝗋𝗏𝖾𝖽 𝖴𝗌𝖾𝗋𝗌 : {served_users}
𝖡𝗅𝗈𝖼𝗄𝖾𝖽 𝖴𝗌𝖾𝗋𝗌 : {blocked_users}
𝖲𝗎𝖽𝗈 𝖴𝗌𝖾𝗋𝗌 : {sudo_users}

𝖳𝗈𝗍𝖺𝗅 𝖣𝖡 𝖲𝗂𝗓𝖾 : {db_size:.4f} ᴍʙ
𝖳𝗈𝗍𝖺𝗅 𝖣𝖡 𝖲𝗍𝗈𝗋𝖺𝗀𝖾 : {db_storage:.1f} ᴍʙ
𝖳𝗈𝗍𝖺𝗅 𝖣𝖡 𝖢𝗈𝗅𝗅𝖾𝖼𝗍𝗂𝗈𝗇𝗌 : {db_collections}
𝖳𝗈𝗍𝖺𝗅 𝖣𝖡 𝖪𝖾𝗒𝗌 : {db_keys}
"""
    return stats_text


async def build_overall_stats():
    # For overall stats, you can add more if you want, or summarize like this:
    served_chats = await get_served_chats_count()
    served_users = await get_served_users_count()
    blocked_users = await get_blocked_users_count()
    sudo_users = await get_sudo_users_count()

    # Dummy count for assistants (update with your logic)
    assistants = 1

    # Example settings, replace with your actual config values
    auto_leave_vc = False
    auto_leave_groups = False
    play_duration_limit = 60  # in minutes

    stats_text = f"""\
𝖠𝗌𝗌𝗂𝖲𝗍𝖺𝗇𝗍𝗌 : {assistants}
𝖡𝗅𝗈𝖼𝗄𝖾𝖽 : {blocked_users}
𝖢𝗁𝖺𝗍𝗌 : {served_chats}
𝖴𝗌𝖾𝗋𝗌 : {served_users}
𝖬𝗈𝖽𝗎𝗅𝖾𝗌 : 39
𝖲𝗎𝖽𝗈𝖾𝗋𝗌 : {sudo_users}

𝖠𝗎𝗍𝗈 𝖫𝖾𝖺𝗏𝗂𝗇𝗀 VideoChat : {auto_leave_vc}
𝖠𝗎𝗍𝗈 𝖫𝖾𝖺𝗏𝗂𝗇𝗀 Groups : {auto_leave_groups}
𝖯𝗅𝖺𝗒 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇 𝖫𝗂𝗆𝗂𝗍 : {play_duration_limit} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌
"""
    return stats_text


def stats_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("General", callback_data="stats_general"),
            InlineKeyboardButton("Overall", callback_data="stats_overall"),
        ],
        [
            InlineKeyboardButton("Close", callback_data="stats_close")
        ]
    ])

from pyrogram.types import CallbackQuery

@Client.on_message(filters.command("stats"))
async def stats_cmd(client: Client, message: Message):
    general_text = await build_general_stats()
    await message.reply_photo(
        photo="https://i.imgur.com/YourStatsImage.png",  # Replace with your image URL
        caption=general_text,
        reply_markup=stats_keyboard(),
        parse_mode="markdown"
    )

@Client.on_callback_query(filters.regex(r"stats_(general|overall|close)"))
async def stats_button_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data

    if data == "stats_general":
        general_text = await build_general_stats()
        await callback_query.edit_message_caption(
            caption=general_text,
            reply_markup=stats_keyboard(),
            parse_mode="markdown"
        )
        await callback_query.answer()

    elif data == "stats_overall":
        overall_text = await build_overall_stats()
        await callback_query.edit_message_caption(
            caption=overall_text,
            reply_markup=stats_keyboard(),
            parse_mode="markdown"
        )
        await callback_query.answer()

    elif data == "stats_close":
        try:
            await callback_query.message.delete()
        except:
            pass
        await callback_query.answer("Closed")
