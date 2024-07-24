import asyncio
import os
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, CommandObject, Filter
from aiogram.types import Message, CallbackQuery, TelegramObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ChatAction, ParseMode

from aiogram import Router, F, BaseMiddleware

import app.keyboards as kb
from app.weather import wind_direction, get_current_weather, get_forecast_weather

router = Router()

class Reg(StatesGroup):
    city = State()


@router.message(CommandStart())
async def hello(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, тебя приветствует бот WeatherWise. \
                          Используй команды в шапке или кнопки ниже', reply_markup=kb.start)


#  Прогноз на 4 дня вперед
@router.message(Command('forecast'), )
async def forecast(message: Message, state: FSMContext):
    await message.answer('Прогноз на 4 дня вперед')
    data = await state.get_data()
    await message.answer(get_forecast_weather(data['city']), parse_mode='html')



@router.message(Command('setlocation'))
async def setlocation(message: Message, state: FSMContext):
    await message.answer('Напиши свой город')
    await state.set_state(Reg.city)


@router.message(Reg.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Город установлен!')
    await state.set_state(None)


@router.message(Command('current'))
async def current(message: Message, state: FSMContext):
    data = await state.get_data()
    city = data.get('city')
    if not city:
        await message.answer(
            "Город не установлен. Пожалуйста, используйте команду /setlocation, чтобы установить ваш город.")
        return
    await message.answer(get_current_weather(data['city']))  # Получаем текущую погоду

