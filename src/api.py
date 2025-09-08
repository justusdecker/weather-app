from requests import get as rqget, post as rqpost
from requests.exceptions import HTTPError, RequestException, JSONDecodeError
from datetime import datetime
from src.ascii_art import c
def get_hour() -> int:
    return datetime.today().hour

def zero_add(t: int) -> str:
    return f"{t}" if t > 10 else f"0{t}"

def weather_api_access() -> bool | dict:
    dt = datetime.today()
    y,m,d = dt.year, zero_add(dt.month), zero_add(dt.day)
    try:
        return rqget(f'https://api.brightsky.dev/weather?lat=53.36&lon=7.2&date={y}-{m}-{d}').json()
    except (HTTPError, RequestException, JSONDecodeError) as EX:
        print(EX)
        return False

def prittify_weather():
    result = weather_api_access()
    if not result: return
    for element in result['weather']:
        temp = element['temperature']
        cond = element['condition']
        sun = element['sunshine']
        wind_s = element['wind_speed']
        pressure = element['pressure_msl']
        
        if temp > 30:
            temp = c(str(temp),252, 144, 3)
        elif temp > 15:
            temp = c(str(temp),169, 252, 3)
        elif temp > 0:
            temp = c(str(temp),3, 219, 252)
        else:
            temp = c(str(temp),3, 78, 252)
        
        if tcond(element['timestamp']):
            print(f'The temperature is {temp}°C {sun=} {wind_s=} {pressure=}')
def tcond(t: str):
        match_hour = int(t.split('T')[1].split(':')[0])
        current_hour = get_hour()
        return match_hour == current_hour

        





