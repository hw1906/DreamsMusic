from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

# Initialize MongoDB client and database
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["dreamsmusicdb"]  # Change to your actual DB name

# Collections
chats_col = db["chats"]
users_col = db["users"]
blocked_users_col = db["blocked_users"]
sudo_users_col = db["sudo_users"]

async def get_served_chats_count() -> int:
    """Return the count of served chats/groups."""
    return await chats_col.count_documents({})

async def get_served_users_count() -> int:
    """Return the count of served users."""
    return await users_col.count_documents({})

async def get_blocked_users_count() -> int:
    """Return the count of blocked users."""
    return await blocked_users_col.count_documents({})

async def get_sudo_users_count() -> int:
    """Return the count of sudo users."""
    return await sudo_users_col.count_documents({})

async def get_db_size_mb() -> float:
    """Calculate approximate DB data size in MB."""
    stats = await db.command("dbstats")
    size_bytes = stats.get("dataSize", 0)
    return size_bytes / (1024 * 1024)

async def get_db_storage_mb() -> float:
    """Calculate allocated DB storage size in MB."""
    stats = await db.command("dbstats")
    storage_bytes = stats.get("storageSize", 0)
    return storage_bytes / (1024 * 1024)

async def get_db_collections_count() -> int:
    """Return the number of collections in the DB."""
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
