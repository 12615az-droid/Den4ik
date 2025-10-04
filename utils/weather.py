import requests

WEATHER_CODE_RU = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Морось слабая", 53: "Морось", 55: "Морось сильная",
    61: "Дождь слабый", 63: "Дождь", 65: "Дождь сильный",
    66: "Ледяной дождь слабый", 67: "Ледяной дождь",
    71: "Снег слабый", 73: "Снег", 75: "Снег сильный",
    77: "Снежные зерна",
    80: "Ливни слабые", 81: "Ливни", 82: "Ливни сильные",
    85: "Снегопад слабый", 86: "Снегопад сильный",
    95: "Гроза", 96: "Гроза с градом", 99: "Сильная гроза с градом",
}


def geocode_city(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1, "language": "ru", "format": "json"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        raise ValueError(f"Город '{city}' не найден")
    item = results[0]
    return item["latitude"], item["longitude"], item["name"], item.get("country", "")


def get_current_weather(city: str, tz: str = "auto"):
    lat, lon, name, country = geocode_city(city)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": tz,
        "hourly": "relativehumidity_2m",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    cw = data["current_weather"]
    code = int(cw.get("weathercode", -1))
    return {
        "city": f"{name}, {country}".strip().strip(","),
        "time": cw["time"],
        "temp_c": cw["temperature"],
        "wind_m_s": cw["windspeed"],
        "wind_dir_deg": cw["winddirection"],
        "weather": WEATHER_CODE_RU.get(code, f"Код погоды {code}"),
        "lat": lat,
        "lon": lon,
        "humidity": (data.get("hourly", {}).get("relativehumidity_2m") or [None])[0],
    }


