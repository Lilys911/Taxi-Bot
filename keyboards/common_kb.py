from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚖 Taksi chaqirish")],
            [KeyboardButton(text="📋 Buyurtmalarim")],
            [KeyboardButton(text="💰 Tariflar")],
            [KeyboardButton(text="👤 Profilim")],
            [KeyboardButton(text="⚙️ Sozlamalar")]
        ],
        resize_keyboard=True
    )
def tariffs_text():
    return (
        "💰 Tariflar:\n\n"
                "🚖 Standart — 15,000 - 25,000 so'm\n"
                "🚗 Comfort — 25,000 - 40,000 so'm\n"
                "💼 Business — 40,000 - 60,000 so'm"
            )
def start_lang_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        ]
    )
def lang_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="set_lang_uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
        ]
    )
def driver_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🟢 Onlayn")],
            [KeyboardButton(text="📦 Aktiv buyurtmalarim")],
            [KeyboardButton(text="👤 Profilim")],
            [KeyboardButton(text="⚙️ Sozlamalar")],
        ],
        resize_keyboard=True
    )
def driver_menu_online():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔴 Oflayn")],
            [KeyboardButton(text="📦 Aktiv buyurtmalarim")],
            [KeyboardButton(text="👤 Profilim")],
            [KeyboardButton(text="⚙️ Sozlamalar")],
        ],
        resize_keyboard=True
    )
def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Buyurtmalar")],
            [KeyboardButton(text="👥 Haydovchilar")],
            [KeyboardButton(text="💰 Tariflar")],
            [KeyboardButton(text="📊 Statistika")]
        ]
    )