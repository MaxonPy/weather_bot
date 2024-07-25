from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

weather_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Текущая погода')],
    [KeyboardButton(text='Прогноз на 4 дня')]
],                                  resize_keyboard=True,
                                    input_field_placeholder='Выберите пункт меню.')


location_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить местоположение', request_location=True)],
    [KeyboardButton(text='Ввести город вручную')],
], resize_keyboard=True)

