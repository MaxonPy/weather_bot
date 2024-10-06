import os
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F, types, Bot
from app.messages import MESSAGES
import app.keyboards as kb
from app.weather import get_current_weather, get_forecast_weather, check_status
from app.filters import CombinedFilterCurWeat, CombinedFilterForecastWeat
from dotenv import load_dotenv
from aiogram.types.message import ContentType

PRICE1 = types.LabeledPrice(label='Премиум подписка', amount=42000)
PRICE2 = types.LabeledPrice(label='test', amount=123123)
router = Router()

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
PAYMENTS_PROVIDER_TOKEN = os.getenv('PAYMENTS_PROVIDER_TOKEN')
bot = Bot(token=TG_TOKEN)

# FSM
class Reg(StatesGroup):
    city = State()


@router.message(Command('buy'))
async def process_buy_command(message: Message):
    if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await message.answer(MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[PRICE1],
                               start_parameter='time-machine-example',
                               payload='some-invoice-payload-for-our-internal-use'
                               )

# Подтверждение платежа(ok=True)
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Обработчик получения успешного платежа
@router.message(F.successful_payment)
async def successful_payment(message: Message):
    print("Платеж прошел успешно:")
    for j, k in message.successful_payment:
        print(f"{j} = {k}")
    await message.answer("Спасибо за оплату! Ваш заказ обработан.")

@router.message(CommandStart())
async def hello(message: Message, state: FSMContext):
    '''
    Обработчик команды /start. Отправляет приветствие пользователю.

    Параметры:
        message (Message): Объект сообщения.
        state(FSMContext): Объект для управления состоянием бота
    '''
    await state.clear()
    await message.answer('Привет, напиши город или отправь свое местоположение по кнопке ниже', reply_markup=kb.location_button)
    await state.set_state(Reg.city)


# Отлавливает состояние
@router.message(Reg.city)
async def process_city(message: Message, state: FSMContext):
    '''
    Отлавливает состояние, когда пользователь вводит
    название города

    Параметры:
        message (Message): Объект сообщения.
        state(FSMContext): Объект для управления состоянием бота
    '''
    if message.content_type == 'text':
        city = message.text
        if await check_status(city):
            await state.update_data(city=city)
            await message.answer('Город установлен!', reply_markup=kb.weather_button)
            await state.set_state(None)
        else:
            await message.answer('Город не найден, введите другое название', reply_markup=kb.location_button)

    else:
        message.content_type == 'location'
        location = message.location
        await state.update_data(city=f'{location.latitude},{location.longitude}')
        await message.answer('Местоположение установлено!', reply_markup=kb.weather_button)
        await state.set_state(None)


# Прогноз на 4 дня вперед
@router.message(CombinedFilterForecastWeat())
async def forecast(message: Message, state: FSMContext):
    '''
    Обработчик прогноза погоды. Отлавливает команду /forecast
    или сообщение от пользователя "Прогноз на 4 дня"

    Параметры:
        message (Message): Объект сообщения.
        state(FSMContext): Объект для управления состоянием бота
    '''
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
    '''
    Обработчик для текущей погоды. Отлавливает команду /current
    или сообщение от пользователя "Текущая погода"

    Параметры:
        message (Message): Объект сообщения.
        state(FSMContext): Объект для управления состоянием бота
    '''
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
    '''
    Обработчик для команды /setlocation.
    Установка местоположения

    Параметры:
        message (Message): Объект сообщения.
        state(FSMContext): Объект для управления состоянием бота
    '''
    await message.answer('Введи город или отправь местоположение', reply_markup=kb.location_button)
    await state.set_state(Reg.city)
