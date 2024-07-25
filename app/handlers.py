from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F

import app.keyboards as kb
from app.weather import get_current_weather, get_forecast_weather
from app.filters import CombinedFilterLocation, CombinedFilterCurWeat, CombinedFilterForecastWeat

router = Router()

class Reg(StatesGroup):
    city = State()


@router.message(CommandStart())
async def hello(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, тебя приветствует бот WeatherWise. \
                          Отправь свое местоположение по кнопке ниже или напиши город', reply_markup=kb.location_button)


@router.message(CombinedFilterLocation())
async def setlocation(message: Message, state: FSMContext):
    await message.answer('Напиши свой город')
    await state.set_state(Reg.city)


@router.message(Reg.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Город установлен!', reply_markup=kb.weather_button)
    await state.set_state(None)


#  Прогноз на 4 дня вперед
@router.message(CombinedFilterForecastWeat())
async def forecast(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(get_forecast_weather(data['city']), parse_mode='html')


@router.message(CombinedFilterCurWeat())
async def current(message: Message, state: FSMContext):
    data = await state.get_data()
    city = data.get('city')
    if not city:
        await message.answer(
            "Город не установлен!", reply_markup=kb.location_button)
        return
    await message.answer(get_current_weather(data['city']), reply_markup=kb.weather_button)  # Получаем текущую погоду

