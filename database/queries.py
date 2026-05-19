import aiosqlite
from database.db import DB_PATH
async def create_user(user_id, full_name, phone, role, lang):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (id, full_name, phone, role, lang) VALUES (?,?,?,?,?)",
            (user_id, full_name, phone, role, lang)
        )
        await db.commit()
async def create_order(user_id, from_address, to_address, tariff, status):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT OR IGNORE INTO orders(passenger_id, from_address, to_address, tariff, status) VALUES (?,?,?,?,?)",
            (user_id, from_address, to_address, tariff, status)
        )
        await db.commit()
        return cursor.lastrowid
async def get_orders(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM orders WHERE passenger_id = ?",
                (user_id,)
            ) as cursor:
            return await cursor.fetchall()
async def get_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM users WHERE id = ?",
                (user_id,)
            ) as cursor:
            return await cursor.fetchone()
async def get_driver(driver_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM drivers WHERE user_id = ?",
                (driver_id)
        ) as cursor:
            return await cursor.fetchone()
async def update_lang(user_id, lang):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET lang = ? WHERE id=?",
                (lang, user_id)
        )
        await db.commit()
async def update_phone(user_id, phone):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET phone = ? WHERE id=?",
            (phone, user_id)
        )
        await db.commit()
async def create_driver(user_id, car_model, car_number):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO drivers (user_id, car_model, car_number) VALUES (?,?,?)",
            (user_id, car_model, car_number)
        )
        await db.commit()
async def update_driver_online(user_id, is_online):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE drivers SET is_online = ? WHERE user_id = ?",
            (is_online, user_id)
        )
        await db.commit()
async def get_online_drivers():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT user_id FROM drivers WHERE is_online = 1"
        ) as cursor:
            return await cursor.fetchall()

async def get_order(order_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM orders WHERE id = ?",
                (order_id,)
        ) as cursor:
            return await cursor.fetchone()
async def update_order_status(order_id, status):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET status = ? WHERE id =?",
            (status, order_id)
        )
        await db.commit()

async def get_driver_active_order(driver_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with  db.execute(
            "SELECT * FROM orders WHERE driver_id =? AND status = 'accepted'",
            (driver_id,)
        ) as cursor:
          return await cursor.fetchone()
async def assign_driver(order_id, driver_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET driver_id =?, status = 'accepted' WHERE id = ?",
            (driver_id, order_id)
        )
        await db.commit()
async def get_all_orders():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM orders"

        ) as cursor:
            return await cursor.fetchall()

async def get_all_drivers():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            """SELECT users.full_name, users.phone, drivers.car_model,
              drivers.car_number, drivers.is_online
              FROM drivers JOIN users ON drivers.user_id = users.id"""
        ) as cursor:
            return await cursor.fetchall()
async def get_all_tariffs():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM tariffs"
        ) as cursor:
            return await cursor.fetchall()
async def add_tariff(name, base_price, per_km):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO tariffs (name, base_price, per_km) VALUES (?,?,?)",
            (name, base_price, per_km)
        )
        await db.commit()
async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            users_count = (await cursor.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM orders") as cursor:
            orders_count = (await cursor.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM drivers") as cursor:
            drivers_count = (await cursor.fetchone())[0]
        return users_count, orders_count, drivers_count