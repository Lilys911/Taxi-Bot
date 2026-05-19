from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states.states import RegisterState, DriverRegisterState
from database.queries import create_user, create_driver, get_user
from keyboards.common_kb import main_menu, start_lang_keyboard, driver_menu, lang_keyboard
from utils.locales import _

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Tilni tanlang / Выберите язык / Choose language", reply_markup=start_lang_keyboard())

@router.callback_query(F.data.startswith("lang_"))
async def lang_handler(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(lang=lang)
    role_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="👤 Yo'lovchi", callback_data="role_passenger"),
        InlineKeyboardButton(text="🚗 Haydovchi", callback_data="role_driver"),
    ]])
    await callback.message.answer(_(lang, "who_are_you"), reply_markup=role_keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("role_"))
async def role_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )
    await state.update_data(role=callback.data.split("_")[1])
    await callback.message.answer(_(lang, "send_phone"), reply_markup=phone_keyboard)
    await state.set_state(RegisterState.phone)
    await callback.answer()

@router.message(RegisterState.phone)
async def phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer(_(lang, "send_name"), reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await create_user(
        user_id=message.from_user.id,
        full_name=name,
        phone=data["phone"],
        role=data["role"],
        lang=lang,
    )
    if data["role"] == "driver":
        await message.answer(_(lang, "car_model"))
        await state.set_state(DriverRegisterState.car_model)
    else:
        await state.clear()
        await message.answer(f"{_(lang, 'welcome')}, {name}!")
        await message.answer(_(lang, "what_to_do"), reply_markup=main_menu())

@router.message(DriverRegisterState.car_model)
async def car_model_handler(message: Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await message.answer(_(lang, "car_number"))
    await state.set_state(DriverRegisterState.car_number)

@router.message(DriverRegisterState.car_number)
async def car_number_handler(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await create_driver(
        user_id=message.from_user.id,
        car_model=data["car_model"],
        car_number=data["car_number"]
    )
    await state.clear()
    await message.answer(f"{_(lang, 'welcome')}!")
    await message.answer(_(lang, "what_to_do"), reply_markup=driver_menu())