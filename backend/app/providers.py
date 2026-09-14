from datetime import datetime, timezone
import os, httpx
from .models import Location, CurrentWeather, ForecastDay

PUNE = Location(name="Pune", latitude=18.5204, longitude=73.8567)

class MockWeatherProvider:
    name = "Mock / deterministic demo"
    async def current(self, location=PUNE):
        return CurrentWeather(location=location, temperature_c=29.0, apparent_temperature_c=31.0, humidity_percent=68, wind_kph=14, precipitation_mm=0.0, condition="Partly cloudy", observed_at=datetime.now(timezone.utc), source=self.name, is_mock=True)
    async def forecast(self, location=PUNE):
        return [ForecastDay(date="Today", min_c=23, max_c=31, precipitation_probability=35, precipitation_mm=1.0, wind_kph=14, condition="Partly cloudy"), ForecastDay(date="Tomorrow", min_c=24, max_c=30, precipitation_probability=65, precipitation_mm=8.0, wind_kph=18, condition="Showers possible"), ForecastDay(date="Day 3", min_c=23, max_c=29, precipitation_probability=45, precipitation_mm=3.0, wind_kph=12, condition="Cloudy")]

class OpenMeteoProvider:
    name = "Open-Meteo"
    async def current(self, location=PUNE):
        params={"latitude":location.latitude,"longitude":location.longitude,"current":"temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,wind_speed_10m,weather_code","timezone":"Asia/Kolkata"}
        async with httpx.AsyncClient(timeout=8) as client: data=(await client.get("https://api.open-meteo.com/v1/forecast",params=params)).raise_for_status().json()["current"]
        return CurrentWeather(location=location, temperature_c=data["temperature_2m"], apparent_temperature_c=data["apparent_temperature"], humidity_percent=data["relative_humidity_2m"], wind_kph=data["wind_speed_10m"], precipitation_mm=data["precipitation"], condition="Weather code " + str(data["weather_code"]), observed_at=datetime.fromisoformat(data["time"]), source=self.name)
    async def forecast(self, location=PUNE):
        params={"latitude":location.latitude,"longitude":location.longitude,"daily":"temperature_2m_min,temperature_2m_max,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,weather_code","timezone":"Asia/Kolkata","forecast_days":3}
        async with httpx.AsyncClient(timeout=8) as client: d=(await client.get("https://api.open-meteo.com/v1/forecast",params=params)).raise_for_status().json()["daily"]
        return [ForecastDay(date=d["time"][i],min_c=d["temperature_2m_min"][i],max_c=d["temperature_2m_max"][i],precipitation_probability=d["precipitation_probability_max"][i] or 0,precipitation_mm=d["precipitation_sum"][i],wind_kph=d["wind_speed_10m_max"][i],condition="Weather code "+str(d["weather_code"][i])) for i in range(3)]

def provider(): return OpenMeteoProvider() if os.getenv("WEATHER_PROVIDER", "mock").lower() == "openmeteo" else MockWeatherProvider()
