import os
from dotenv import load_dotenv
from datetime import datetime
import aiohttp

load_dotenv()
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')


def format_date(date_str: str) -> str:
    '''
    Функция для форматирования даты.
    Преобразует даты из формата "2024-07-12" в "12 июля"

    Параметры:
        date_str(str): cтрока даты в формате "2024-07-12"

    Возвращаемое значение:
        form_date(str): отформатированная строка
    '''
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    date = datetime.strptime(date_str, '%Y-%m-%d')
    day = date.day
    month = months[date.month]
    form_date = f"{day} {month}"
    return form_date


def wind_direction(degrees: int) -> str:
    '''
    Функция преобразования градуса направления ветра
    в привычный для человека формат

    :param degrees: значение в градусах
    :return: направление ветра
    '''
    degrees = int(degrees)
    if (degrees >= 0 and degrees <= 22.5) or (degrees > 337.5 and degrees <= 360):
        return "северное"
    elif degrees > 22.5 and degrees <= 67.5:
        return "северо-восточное"
    elif degrees > 67.5 and degrees <= 112.5:
        return "восточное"
    elif degrees > 112.5 and degrees <= 157.5:
        return "юго-восточное"
    elif degrees > 157.5 and degrees <= 202.5:
        return "южное"
    elif degrees > 202.5 and degrees <= 247.5:
        return "юго-западное"
    elif degrees > 247.5 and degrees <= 292.5:
        return "западное"
    elif degrees > 292.5 and degrees <= 337.5:
        return "северо-западное"
    else:
        return "некорректное значение градусов"  #


async def check_status(city):
    '''
    Функия проверки корректности введеного города
    :param city: название города
    :return:
        True - если город введен корректно
        False - если город введен некорректно

    '''
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_TOKEN}&q={city}&aqi=no&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            status = response.status
            if status == 200:
                return True


async def get_current_weather(city: str) -> str:
    '''
    Функция определения текущей погоды
    :param city: название города
    :return: строка с текущей погодой
    '''
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_TOKEN}&q={city}&aqi=no&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return 'Введите корректное название города'
            data = await response.json()
            temp = data['current']['temp_c']
            wind_speed = data['current']['wind_mph']
            wind_deg = data['current']['wind_degree']
            weat_description = data['current']['condition']['text']
            return (f'Температура в вашем городе равна: {int(temp)}°С.\nНа улице {weat_description}.\n'
                    f'Скорость ветра {wind_speed} м/c, направление: {wind_direction(wind_deg)}')


async def get_forecast_weather(city):
    '''
    Функция для определения прогноза на 4 дня
    :param city: название города
    :return: строка с текущей погодой
    '''
    url = f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={city}&days=4&aqi=no&alerts=no&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return 'Введите корректное название города'
            data = await response.json()
            forecast_days = data['forecast']['forecastday']
            forecast_message = "Прогноз погоды на 4 дня:\n\n"

        for day in forecast_days:
            date = format_date(day['date'])
            morning = day['hour'][8]  # 08:00
            afternoon = day['hour'][13]  # 13:00
            evening = day['hour'][20]  # 20:00

            forecast_message += f"📌{date}\n"
            forecast_message += (
                f"<b>☀️Утром 08:00</b>. Температура - <b><i>{morning['temp_c']}°C</i></b>. "
                f"{morning['condition']['text']}. Направление ветра - <i>{wind_direction(morning['wind_degree'])}</i> {morning['wind_kph']} м/с\n"
            )
            forecast_message += (
                f"<b>🌤️Днем 13:00</b>. Температура - <b><i>{afternoon['temp_c']}°C</i></b>. "
                f"{afternoon['condition']['text']}. Направление ветра - <i>{wind_direction(afternoon['wind_degree'])}</i> {afternoon['wind_kph']} м/с\n"
            )
            forecast_message += (
                f"<b>🌙Вечером 20:00</b>. Температура - <b><i>{evening['temp_c']}°C</i></b>. "
                f"{evening['condition']['text']}. Направление ветра - <i>{wind_direction(evening['wind_degree'])}</i> {evening['wind_kph']} м/с\n"
            )
            forecast_message += "\n"

        return forecast_message
