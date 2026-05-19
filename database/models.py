from database.db import get_db

async def create_tables():
    async with await get_db() as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                phone TEXT,
                role TEXT,
                lang TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                passenger_id INTEGER,
                driver_id INTEGER,
                from_address TEXT,
                to_address TEXT,
                tariff TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        await db.commit()
        await db.execute('''
            CREATE TABLE IF NOT EXISTS drivers (
                 user_id INTEGER PRIMARY KEY REFERENCES users(id),
                 car_model TEXT, 
                 car_number TEXT,
                 is_online INTEGER DEFAULT 0,
                 rating FLOAT DEFAULT 5.0 
                 )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tariffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                base_price INTEGER,
                per_km INTEGER,
                is_active INTEGER DEFAULT 1
            )
        ''')
        await db.commit()