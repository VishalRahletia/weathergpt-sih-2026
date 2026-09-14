from datetime import datetime, timezone
from .models import Warning

def freshness(weather):
    age=(datetime.now(timezone.utc)-weather.observed_at.replace(tzinfo=weather.observed_at.tzinfo or timezone.utc)).total_seconds()
    return {"fresh": age <= 3600, "age_seconds": max(0, int(age)), "checked_at": datetime.now(timezone.utc).isoformat()}

def warnings(current, forecast):
    out=[]
    if current.temperature_c >= 40 or any(d.max_c >= 40 for d in forecast): out.append(Warning(severity="warning",title="Heat risk",message="Avoid prolonged afternoon exposure; hydrate and check vulnerable people.",rule_id="heat_40c"))
    if any(d.precipitation_probability >= 70 or d.precipitation_mm >= 20 for d in forecast): out.append(Warning(severity="advisory",title="Rain advisory",message="Rain is possible. Carry protection and allow extra travel time.",rule_id="rain_probability_70"))
    if current.wind_kph >= 50 or any(d.wind_kph >= 50 for d in forecast): out.append(Warning(severity="watch",title="Strong wind watch",message="Secure loose items and use caution outdoors.",rule_id="wind_50kph"))
    return out

def reply(message, current, forecast, ws, language):
    rain=max(forecast, key=lambda x:x.precipitation_probability)
    if language == "hi":
        return f"{current.location.name} में तापमान {current.temperature_c}°C है और स्थिति {current.condition} है। सबसे अधिक बारिश की संभावना {rain.date} को {rain.precipitation_probability}% है। " + (ws[0].message if ws else "कोई नियम-आधारित चेतावनी सक्रिय नहीं है।")
    return f"In {current.location.name}, it is {current.temperature_c}°C and {current.condition.lower()}. The highest rain chance is {rain.date} at {rain.precipitation_probability}%. " + (ws[0].message if ws else "No rule-based weather advisory is active.")
