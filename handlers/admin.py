from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from keyboards.common_kb import main_menu, admin_menu
from aiogram.filters import Command
from database.queries import get_all_orders, get_all_drivers, get_all_tariffs, get_stats
router = Router()
@router.message(Command("admin"))
async def admin_handler(message:Message):
      if message.from_user.id != ADMIN_ID:
          await message.answer("❌ Sizda ruxsat yo'q!")
          return
      await message.answer("👨‍💼 Admin panel:", reply_markup=admin_menu())
@router.message(F.text == "📦 Buyurtmalar")
async def orders_handler(message:Message):
    orders = await get_all_orders()
    if not orders:
        await message.answer("Hozircha  buyurtma yo'q")
        return
    for order in orders:
        await message.answer(
            f"📍 Qayerdan: {order[2]}\n"
            f"🏁 Qayerga: {order[3]}\n"
            f"🚖 Tarif: {order[4]}\n"
            f"📊 Status: {order[5]}"

        )
@router.message(F.text == "👥 Haydovchilar")
async def drivers_handler(message:Message):
    drivers = await get_all_drivers()
    if not drivers:
        await message.answer("Hozircha haydovchilar yo'q")
        return
    for driver in drivers:
        await message.answer(
        f"👤 Ism: {driver[0]}\n"
        f"📱 Telefon: {driver[1]}\n"
        f"🚗 Mashina: {driver[2]} - {driver[3]}\n"
        f"🟢 Onlayn: {'Ha' if driver[4] else 'Yoq'}"
        )
@router.message(F.text == "💰 Tariflar")
async def tariffs_handler(message:Message):
    tariffs = await get_all_tariffs()
    if not tariffs:
        await message.answer("Hozircha tariflar yo'q!")
        return
    for tarif in tariffs:
        await message.answer(
            f"🚖 Tarif: {tarif[1]}\n"
            f"💰 Boshlang'ich narx: {tarif[2]} so'm\n"
            f"📏 Km narxi: {tarif[3]} so'm\n"
            f"✅ Aktiv: {'Ha' if tarif[4] else 'Yoq'}"
        )
@router.message(F.text == "📊 Statistika")
async def stats_handler(message: Message):
    users, orders, drivers = await get_stats()
    await message.answer(
        f"📊 Statistika:\n\n"
        f"👥 Foydalanuvchilar: {users}\n"
        f"📦 Buyurtmalar: {orders}\n"
        f"🚗 Haydovchilar: {drivers}"
    )