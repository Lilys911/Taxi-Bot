import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher

async def main():
   print("Bot ishga tushdi!")
   await dp.start_polling(bot)
if __name__ == "__main__":
   asyncio.run(main())
