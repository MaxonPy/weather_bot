import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

#  Функция определения направление ветра по градусу
def wind_direction(degrees):
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

# Функция для определения текущей погоды
def get_current_weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_TOKEN}&q={city}&aqi=no&lang=ru'
    response = requests.get(url)
    data = response.json()
    temp = data['current']['temp_c']
    wind_speed = data['current']['wind_mph']
    wind_deg = data['current']['wind_degree']
    weat_description= data['current']['condition']['text']
    return (f'Температура в вашем городе равна: {int(temp)}°С.\nНа улице {weat_description}.\n'
                         f'Скорость ветра {wind_speed} м/c, направление: {wind_direction(wind_deg)}')

# Функция для определения прогноза на 4 дня
def get_forecast_weather(city): # Прогноз на 4 дня вперед
    url = f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={city}&days=4&aqi=no&alerts=no&lang=ru'
    response = requests.get(url)
    data = response.json()
    forecast_days = data['forecast']['forecastday']
    forecast_message = "Прогноз погоды на 4 дня:\n\n"

    for day in forecast_days:
        date = day['date']
        morning = day['hour'][8]  # 08:00
        afternoon = day['hour'][13]  # 13:00
        evening = day['hour'][20]  # 20:00

        forecast_message += f"{date}\n"
        forecast_message += (
            f"<b>Утром 08:00</b>. Температура - {morning['temp_c']}°C. "
            f"{morning['condition']['text']}. Ветер {morning['wind_dir']} {morning['wind_kph']} м/с\n"
        )
        forecast_message += (
            f"<b>Днем 13:00</b>. Температура - {afternoon['temp_c']}°C. "
            f"{afternoon['condition']['text']}. Ветер {afternoon['wind_dir']} {afternoon['wind_kph']} м/с\n"
        )
        forecast_message += (
            f"<b>Вечером 20:00</b>. Температура - {evening['temp_c']}°C. "
            f"{evening['condition']['text']}. Ветер {evening['wind_dir']} {evening['wind_kph']} м/с\n"
        )
        forecast_message += "\n"

    return forecast_message




