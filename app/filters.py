from aiogram.filters import BaseFilter
from aiogram.types import Message


class CombinedFilterCurWeat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == 'Текущая погода' or message.text == '/current'


class CombinedFilterForecastWeat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == 'Прогноз на 4 дня' or message.text == '/forecast'
