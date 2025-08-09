from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db_helpers import add_song_to_playlist, get_user_playlist
import asyncio

# Temporary storage for add song flow state (you can replace with DB/session)
user_adding_song = {}

# Keyboard for playlist main panel
def playlist_main_kb():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕ Add Song", callback_data="playlist_add")],
            [InlineKeyboardButton("🎵 My Playlist", callback_data="playlist_show")],
            [InlineKeyboardButton("❌ Close", callback_data="playlist_close")],
        ]
    )

@Client.on_message(filters.command("playlist") & filters.private)
async def playlist_cmd(client: Client, message: Message):
    await message.reply_text(
        "🎶 Playlist Menu",
        reply_markup=playlist_main_kb()
    )

@Client.on_callback_query(filters.regex(r"playlist_"))
async def playlist_cb_handler(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "playlist_add":
        user_adding_song[user_id] = True
        await callback_query.message.edit_text(
            "Send me the song in this format:\n\n`Song Name - Song Link`",
            parse_mode="markdown"
        )
        await callback_query.answer()

    elif data == "playlist_show":
        songs = await get_user_playlist(user_id)
        if not songs:
            await callback_query.message.edit_text("Your playlist is empty.")
            await callback_query.answer()
            return

        # Build list of songs with buttons to play each
        buttons = []
        for idx, song in enumerate(songs, 1):
            buttons.append([InlineKeyboardButton(f"{idx}. {song['name']}", callback_data=f"playlist_play_{idx-1}")])
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="playlist_back")])
        buttons.append([InlineKeyboardButton("❌ Close", callback_data="playlist_close")])

        await callback_query.message.edit_text(
            "🎵 Your Playlist:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await callback_query.answer()

    elif data == "playlist_close":
        await callback_query.message.delete()
        await callback_query.answer("Closed playlist panel.")

    elif data == "playlist_back":
        await callback_query.message.edit_text(
            "🎶 Playlist Menu",
            reply_markup=playlist_main_kb()
        )
        await callback_query.answer()

    elif data.startswith("playlist_play_"):
        songs = await get_user_playlist(user_id)
        index = int(data.split("_")[-1])
        if index >= len(songs):
            await callback_query.answer("Invalid song index.", show_alert=True)
            return
        song = songs[index]

        # Here call your play logic (like /play command but with song['link'])
        # For example, call a helper function play_song(chat_id, song_link)
        # For demo:
        await callback_query.answer(f"Playing: {song['name']}")

        # You can replace below with your play command or function call
        chat_id = callback_query.message.chat.id
        # await play_handler.play_song_by_link(client, chat_id, song['link']) 
        # Or send a message:
        await callback_query.message.reply(f"Playing [{song['name']}]({song['link']})", parse_mode="markdown")

        # Optionally close playlist panel or keep open
