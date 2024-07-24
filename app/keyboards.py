from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Текущая погода')],
],                                  resize_keyboard=True,
                                    input_field_placeholder='Выберите пункт меню.')