from datetime import datetime
from pydantic import BaseModel, Field

class Location(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str = "India"
    timezone: str = "Asia/Kolkata"

class CurrentWeather(BaseModel):
    location: Location
    temperature_c: float
    apparent_temperature_c: float
    humidity_percent: int
    wind_kph: float
    precipitation_mm: float
    condition: str
    observed_at: datetime
    source: str
    is_mock: bool = False

class ForecastDay(BaseModel):
    date: str
    min_c: float
    max_c: float
    precipitation_probability: int
    precipitation_mm: float
    wind_kph: float
    condition: str

class Warning(BaseModel):
    severity: str = Field(pattern="^(info|advisory|watch|warning)$")
    title: str
    message: str
    rule_id: str
    official: bool = False

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    location: str = "Pune"
    language: str = Field(default="en", pattern="^(en|hi)$")

class AlertSubscription(BaseModel):
    location: str = "Pune"
    channel: str = Field(pattern="^(in_app|email)$")
    destination: str | None = None
    threshold: str = "warning"
