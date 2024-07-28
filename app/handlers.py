from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F

import app.keyboards as kb
from app.weather import get_current_weather, get_forecast_weather
from app.filters import CombinedFilterCurWeat, CombinedFilterForecastWeat

router = Router()

# FSM
class Reg(StatesGroup):
    city = State()


# Старт
@router.message(CommandStart())
async def hello(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, напиши город или отправь свое местоположение по кнопке ниже', reply_markup=kb.location_button)
    await state.set_state(Reg.city)


# Отлавливает состояние
@router.message(Reg.city)
async def process_city(message: Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(city=message.text)
    elif message.content_type == 'location':
        await state.update_data(city=f'{message.location.latitude},{message.location.longitude}')
    else:
        await message.answer('Пожалуйста отправьте город или местоположение')
        return

    await message.answer('Город установлен!', reply_markup=kb.weather_button)
    await state.set_state(None)


# Прогноз на 4 дня вперед
@router.message(CombinedFilterForecastWeat())
async def forecast(message: Message, state: FSMContext):
    data = await state.get_data()
    city = data.get('city')
    if not city:
        await message.answer("Город не установлен!", reply_markup=kb.location_button)
        return

    forecast_weather = await get_forecast_weather(city)
    await message.answer(forecast_weather, parse_mode='html')


# Текущая погода
@router.message(CombinedFilterCurWeat())
async def current(message: Message, state: FSMContext):
    data = await state.get_data()
    city = data.get('city')
    if not city:
        await message.answer(
            "Город не установлен!", reply_markup=kb.location_button)
        return
    current_weather = await get_current_weather(city)
    await message.answer(current_weather, reply_markup=kb.weather_button)


@router.message(Command('setlocation'))
async def setlocation(message: Message, state:FSMContext):
    await message.answer('Введи город или отправь местоположение', reply_markup=kb.location_button)
    await state.set_state(Reg.city)
