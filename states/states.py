from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    phone = State()
    name = State()
class OrderState(StatesGroup):
    fromWhere = State()
    toWhere = State()
    tariff = State()
    confirm = State()
class SettingsState(StatesGroup):
    new_phone = State()
class DriverRegisterState(StatesGroup):
    car_model = State()
    car_number = State()
