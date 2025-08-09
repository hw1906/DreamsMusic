# db_helpers.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI  # Your Mongo URI from config

# Initialize MongoDB async client and DB
mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client["dreamsmusicdb"]  # Change to your actual DB name

# Collections (adjust as per your DB schema)
chats_col = db["chats"]
users_col = db["users"]
blocked_users_col = db["blocked_users"]
sudo_users_col = db["sudo_users"]
playlist_col = db["user_playlists"]  # For playlist feature

# ---- Count Functions ----

async def get_served_chats_count() -> int:
    """Return count of served chats/groups."""
    return await chats_col.count_documents({})

async def get_served_users_count() -> int:
    """Return count of served users."""
    return await users_col.count_documents({})

async def get_blocked_users_count() -> int:
    """Return count of blocked users."""
    return await blocked_users_col.count_documents({})

async def get_sudo_users_count() -> int:
    """Return count of sudo users."""
    return await sudo_users_col.count_documents({})

# ---- DB Size & Storage Stats ----

async def get_db_size_mb() -> float:
    """Return DB data size in MB."""
    stats = await db.command("dbstats")
    size_bytes = stats.get("dataSize", 0)
    return size_bytes / (1024 * 1024)

async def get_db_storage_mb() -> float:
    """Return DB allocated storage size in MB."""
    stats = await db.command("dbstats")
    storage_bytes = stats.get("storageSize", 0)
    return storage_bytes / (1024 * 1024)

async def get_db_collections_count() -> int:
    """Return number of collections in DB."""
    collections = await db.list_collection_names()
    return len(collections)

async def get_db_keys_count() -> int:
    """Return total number of indexes in all collections."""
    total_indexes = 0
    collections = await db.list_collection_names()
    for coll_name in collections:
        coll = db[coll_name]
        indexes = await coll.index_information()
        total_indexes += len(indexes)
    return total_indexes

# ---- Playlist Helpers ----

async def add_song_to_playlist(user_id: int, song_name: str, song_link: str):
    """Add a song to user's playlist."""
    await playlist_col.update_one(
        {"user_id": user_id},
        {"$push": {"songs": {"name": song_name, "link": song_link}}},
        upsert=True,
    )

async def get_user_playlist(user_id: int):
    """Get all songs in user's playlist."""
    doc = await playlist_col.find_one({"user_id": user_id})
    if doc and "songs" in doc:
        return doc["songs"]
    return []

async def clear_user_playlist(user_id: int):
    """Clear user's playlist."""
    await playlist_col.update_one({"user_id": user_id}, {"$set": {"songs": []}})

