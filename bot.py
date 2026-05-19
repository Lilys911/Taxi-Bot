import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import common, passenger, drivers, admin
from database.models import create_tables
from bot_instance import bot

dp = Dispatcher()

dp.include_router(common.router)
dp.include_router(passenger.router)
dp.include_router(drivers.router)
dp.include_router(admin.router)
async def main():
   await create_tables()
   print("Bot ishga tushdi!")
   await dp.start_polling(bot)
if __name__ == "__main__":
   asyncio.run(main())

