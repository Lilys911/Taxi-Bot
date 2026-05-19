import aiosqlite

DB_PATH = "taxi.db"

async def get_db():
    return  aiosqlite.connect(DB_PATH)