from aiogram.filters import BaseFilter
from aiogram.types import Message


class CombinedFilterCurWeat(BaseFilter):
    """
        Класс фильтрации сообщений для определения запроса текущей погоды.

        Этот класс наследуется от BaseFilter и переопределяет метод __call__, чтобы
        проверять текст сообщения. Сообщение считается соответствующим фильтру, если его текст
        равен 'Текущая погода' или '/current'.

        Methods:
        --------
        __call__(message: Message):
            Проверяет, соответствует ли текст сообщения одному из предопределенных значений.
        """
    async def __call__(self, message: Message) -> bool:
        return message.text == 'Текущая погода' or message.text == '/current'


class CombinedFilterForecastWeat(BaseFilter):
    """
        Класс фильтрации сообщений для определения запроса прогноза погоды на 4 дня.

        Этот класс наследуется от BaseFilter и переопределяет метод __call__, чтобы
        проверять текст сообщения. Сообщение считается соответствующим фильтру, если его текст
        равен 'Прогноз на 4 дня' или '/forecast'.

        Methods:
        --------
        __call__(message: Message):
            Проверяет, соответствует ли текст сообщения одному из предопределенных значений.
        """
    async def __call__(self, message: Message) -> bool:
        return message.text == 'Прогноз на 4 дня' or message.text == '/forecast'
