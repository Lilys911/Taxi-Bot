from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.common_kb import main_menu, driver_menu, driver_menu_online, lang_keyboard
from database.queries import update_driver_online, get_order, update_order_status, get_driver_active_order, assign_driver, get_driver, update_phone, update_lang, get_user
from bot_instance import bot
from states.states import SettingsState
from utils.locales import _

router = Router()

@router.message(F.text == "🟢 Onlayn")
async def offline_handler(message: Message):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    await update_driver_online(user_id=message.from_user.id, is_online=1)
    await message.answer(f"🟢 {_(lang, 'online')}", reply_markup=driver_menu_online())

@router.message(F.text == "🔴 Oflayn")
async def online_handler(message: Message):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    await update_driver_online(user_id=message.from_user.id, is_online=0)
    await message.answer(f"🔴 {_(lang, 'offline')}", reply_markup=driver_menu())

@router.callback_query(F.data.startswith("accept_"))
async def accept_order(callback: CallbackQuery):
    order_id = callback.data.split("_")[1]
    await assign_driver(order_id=order_id, driver_id=callback.from_user.id)
    order = await get_order(order_id)
    passenger_id = order[1]
    await bot.send_message(passenger_id, "🚗 Haydovchi topildi! Yo'lda...")
    await callback.message.answer(f"✅ Buyurtma #{order_id} qabul qilindi!")
    await callback.answer()

@router.callback_query(F.data.startswith("reject_"))
async def reject_order(callback: CallbackQuery):
    order_id = callback.data.split("_")[1]
    await callback.message.answer(f"❌ Buyurtma #{order_id} rad etildi!")
    order = await get_order(order_id)
    passenger_id = order[1]
    await bot.send_message(passenger_id, "❌ Haydovchi rad etdi. Boshqa haydovchi qidirilmoqda...")
    await update_order_status(order_id=order_id, status="rejected")
    await callback.answer()

@router.message(F.text == "📦 Aktiv buyurtmalarim")
async def active_order_handler(message: Message):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    order = await get_driver_active_order(driver_id=message.from_user.id)
    if not order:
        await message.answer(_(lang, "no_active_order"))
        return
    await message.answer(
        f"📍 Qayerdan: {order[2]}\n"
        f"🏁 Qayerga: {order[3]}\n"
        f"🚖 Tarif: {order[4]}\n"
        f"📊 Status: {order[5]}"
    )

@router.message(F.text == "👤 Profilim")
async def profile_handler_driver(message: Message):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    driver = await get_driver(driver_id=message.from_user.id)
    if not driver:
        await message.answer(_(lang, "profile_not_found"))
        return
    await message.answer(
        f"👤 Ism: {user[1]}\n"
        f"📱 Telefon: {user[2]}\n"
        f"🚗 Mashina: {driver[1]} - {driver[2]}"
    )

@router.message(F.text == "⚙️ Sozlamalar")
async def settings_handler_driver(message: Message):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    setting = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="change-lang")],
            [InlineKeyboardButton(text="📱 Telefon o'zgartirish", callback_data="change-phone")],
        ]
    )
    await message.answer(_(lang, "settings"), reply_markup=setting)

@router.callback_query(F.data == "change-lang")
async def change_lang_handler(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    lang = user[4] if user else "uz"
    await callback.message.answer(_(lang, "choose_lang"), reply_markup=lang_keyboard())
    await callback.answer()

@router.callback_query(F.data.startswith("set_lang_"))
async def set_lang_handler(callback: CallbackQuery):
    lang = callback.data.split("_")[2]
    await update_lang(user_id=callback.from_user.id, lang=lang)
    await callback.message.answer(_(lang, "lang_updated"))
    await callback.answer()

@router.callback_query(F.data == "change-phone")
async def change_phone_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    lang = user[4] if user else "uz"
    await callback.message.answer(_(lang, "send_new_phone"), reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Telefon yuborish", request_contact=True)]],
        resize_keyboard=True
    ))
    await state.set_state(SettingsState.new_phone)
    await callback.answer()

@router.message(SettingsState.new_phone)
async def set_new_phone(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    phone = message.contact.phone_number
    await update_phone(user_id=message.from_user.id, phone=phone)
    await message.answer(_(lang, "phone_updated"), reply_markup=driver_menu())
    await state.clear()