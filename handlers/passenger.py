from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states.states import OrderState, SettingsState
from database.queries import create_order, get_orders, get_user, update_lang, update_phone, get_online_drivers
from utils.distance import calculate_price
from keyboards.common_kb import main_menu, tariffs_text, lang_keyboard
from bot_instance import bot
from utils.locales import _

router = Router()

@router.message(F.text == "🚖 Taksi chaqirish")
async def taxi_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Lokatsiyamni yuborish", request_location=True)],
            [KeyboardButton(text="✏️ Manzil yozish")]
        ],
        resize_keyboard=True
    )
    await message.answer(_(lang, "from_where"), reply_markup=location_keyboard)
    await state.set_state(OrderState.fromWhere)

@router.message(OrderState.fromWhere, F.location)
async def from_location_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(from_lat=lat, from_lon=lon, fromWhere=f"{lat}, {lon}")
    await message.answer(_(lang, "to_where"), reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.toWhere)

@router.message(OrderState.fromWhere)
async def from_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    if message.text == "✏️ Manzil yozish":
        await message.answer(_(lang, "from_where"), reply_markup=ReplyKeyboardRemove())
        return
    await state.update_data(fromWhere=message.text)
    await message.answer(_(lang, "to_where"), reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.toWhere)

@router.message(OrderState.toWhere)
async def to_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    if message.text == "✏️ Manzil yozish":
        await message.answer(_(lang, "to_where"))
        return
    await state.update_data(toWhere=message.text)
    tariff = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Standart", callback_data="standart")],
            [InlineKeyboardButton(text="Comfort", callback_data="comfort")],
            [InlineKeyboardButton(text="Business", callback_data="business")]
        ]
    )
    await message.answer(_(lang, "choose_tariff"), reply_markup=tariff)
    await state.set_state(OrderState.tariff)

@router.callback_query(F.data.in_({"standart", "comfort", "business"}))
async def tariff_choice(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    lang = user[4] if user else "uz"
    tariff = callback.data
    await state.update_data(tariff=tariff)
    confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no"),
        ]]
    )
    await callback.message.answer(_(lang, "confirm"), reply_markup=confirm_kb)
    await callback.answer()

@router.callback_query(F.data == "confirm_yes")
async def confirm_yes(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    lang = user[4] if user else "uz"
    data = await state.get_data()
    narx = calculate_price(data["tariff"])
    type_money = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💵 Naqd pul", callback_data="pay_cash"),
            InlineKeyboardButton(text="💳 Karta", callback_data="pay_card"),
        ]]
    )
    await callback.message.answer(
        f"📍 Qayerdan: {data['fromWhere']}\n"
        f"🏁 Qayerga: {data['toWhere']}\n"
        f"🚖 Tarif: {data['tariff']}\n"
        f"💵 Taxminiy narx: {narx}\n\n"
        f"{_(lang, 'choose_payment')}",
        reply_markup=type_money
    )
    order_id = await create_order(
        user_id=callback.from_user.id,
        from_address=data["fromWhere"],
        to_address=data["toWhere"],
        tariff=data["tariff"],
        status="pending",
    )
    drivers = await get_online_drivers()
    accept_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"accept_{order_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{order_id}"),
        ]]
    )
    for driver in drivers:
        await bot.send_message(
            driver[0],
            f"🆕 Yangi buyurtma!\n"
            f"📍 Qayerdan: {data['fromWhere']}\n"
            f"🏁 Qayerga: {data['toWhere']}\n"
            f"🚖 Tarif: {data['tariff']}",
            reply_markup=accept_keyboard
        )
    await state.clear()
    await callback.answer()

@router.callback_query(F.data.in_({"pay_cash", "pay_card"}))
async def payment_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    lang = user[4] if user else "uz"
    tolov = "💵 Naqd pul" if callback.data == "pay_cash" else "💳 Karta"
    await callback.message.answer(
        f"{_(lang, 'order_done')}\n💳 To'lov usuli: {tolov}\n🚗 Haydovchi yo'lda...",
        reply_markup=main_menu()
    )
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "confirm_no")
async def confirm_no(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    lang = user[4] if user else "uz"
    await callback.message.answer(_(lang, "order_cancelled"), reply_markup=main_menu())
    await state.clear()
    await callback.answer()

@router.message(F.text == "📋 Buyurtmalarim")
async def orders_handler(message: Message):
    user = await get_user(message.from_user.id)
    lang = user[4] if user else "uz"
    orders = await get_orders(user_id=message.from_user.id)
    if not orders:
        await message.answer(_(lang, "no_orders"))
        return
    for order in orders:
        await message.answer(
            f"📍 Qayerdan: {order[2]}\n"
            f"🏁 Qayerga: {order[3]}\n"
            f"🚖 Tarif: {order[4]}\n"
            f"📊 Status: {order[5]}"
        )

@router.message(F.text == "💰 Tariflar")
async def tariff_handler(message: Message):
    await message.answer(tariffs_text())

@router.message(F.text == "👤 Profilim")
async def profile_handler(message: Message):
    user = await get_user(user_id=message.from_user.id)
    lang = user[4] if user else "uz"
    if not user:
        await message.answer(_(lang, "profile_not_found"))
        return
    await message.answer(
        f"👤 Ism: {user[1]}\n"
        f"📱 Telefon: {user[2]}\n"
        f"🚖 Rol: {user[3]}"
    )

@router.message(F.text == "⚙️ Sozlamalar")
async def settings_handler(message: Message):
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
    await message.answer(_(lang, "phone_updated"), reply_markup=main_menu())
    await state.clear()