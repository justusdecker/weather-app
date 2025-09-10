from requests import get as rqget, post as rqpost
from requests.exceptions import HTTPError, RequestException, JSONDecodeError
from datetime import datetime
from src.ascii_art import c

"""

'cloud_cover' =
64
'visibility' =
26700
'condition' =
'dry'
'solar' =
0.0
"""

def get_hour() -> int:
    return datetime.today().hour

def zero_add(t: int) -> str:
    return f"{t}" if t >= 10 else f"0{t}"

def weather_api_access() -> bool | dict:
    dt = datetime.today()
    y,m,d = dt.year, zero_add(dt.month), zero_add(dt.day)
    print(f"Fetching weather for {y}-{m}-{d}")
    try:
        return rqget(f'https://api.brightsky.dev/weather?lat=53.36&lon=7.2&date={y}-{m}-{d}').json()
    except (HTTPError, RequestException, JSONDecodeError) as EX:
        print(EX)
        return False

def get_current_weather():
    """
    Fetches the current weather data from the Bright Sky API and returns the weather record for the current hour.
    Returns:
        dict: Weather record for the current hour if available, otherwise None.
    """
    result = weather_api_access()
    if not result: return
    for element in result['weather']:
        if tcond(element['timestamp']):
            return element

ICON_MAPPER = {
    'clear-day': '☀️',
    'clear-night': '🌙',
    'partly-cloudy-day': '⛅',
    'partly-cloudy-night': '🌙☁️',
    'cloudy': '🌥️',
    'fog': '🌫️',
    'wind': '💨',
    'sleet': '🌨️',
    'rain': '🌧️',
    'snow': '❄️',
    'hail': '🌨️',
    'overcast': '☁️',
    'thunderstorm': '⛈️',
    'None': '❓'
}

WIND_DIR_MAPPER = {
    (0, 22.5): '⬆️ N',
    (22.5, 67.5): '↗️ NE',
    (67.5, 112.5): '➡️ E',
    (112.5, 157.5): '↘️ SE',
    (157.5, 202.5): '⬇️ S',
    (202.5, 247.5): '↙️ SW',
    (247.5, 292.5): '⬅️ W',
    (292.5, 337.5): '↖️ NW',
    (337.5, 360): '⬆️ N'
}

EMOJI_NUMBER_MAPPER = {
    '0': '0️',
    '1': '1️',
    '2': '2️',
    '3': '3️',
    '4': '4️',
    '5': '5️',
    '6': '6️',
    '7': '7️',
    '8': '8️',
    '9': '9️'}

def convert_string_to_emoji_number(s: str) -> str:
    """
    Converts a string of digits to a string of corresponding emoji numbers.
    Args:
        s (str): Input string containing digits.
    Returns:
        str: String with digits replaced by their corresponding emoji numbers.
    """
    return ''.join(EMOJI_NUMBER_MAPPER.get(char, char) for char in s)

def get_wind_direction(degree: int | None) -> str:
    """
    Converts wind direction in degrees to a compass direction with an arrow.
    Args:
        degree (int | None): Wind direction in degrees (0-360) or None if not available.
        Returns:
            str: Compass direction with an arrow (e.g., '⬆️ N', '↗️ NE', etc.) or '❓' if degree is None.
    """
    for (low, high), direction in WIND_DIR_MAPPER.items():
        if low <= degree < high:
            return direction
    return '❓'

def prittify_weather():
    weather = get_current_weather()
    if not weather: return
    icon = weather['icon']
    temperature = weather['temperature']
    windspeed = weather['wind_speed']
    winddirection = weather['wind_direction']
    pressure = weather['pressure_msl']
    humidity = weather['relative_humidity']
    dt = convert_string_to_emoji_number(datetime.now().strftime("%H %M %S"))
    
    
    print(f""" 
🕐 {dt}

{ICON_MAPPER.get(icon, '❓')}  {temperature}°C

💨 {windspeed} km/h {get_wind_direction(winddirection)}
💧 {0 if humidity is None else humidity}%
pressure: {pressure} hPa
          """)

def tcond(t: str):
        match_hour = int(t.split('T')[1].split(':')[0])
        current_hour = get_hour()
        return match_hour == current_hour