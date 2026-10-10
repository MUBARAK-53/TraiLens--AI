import httpx

async def get_local_weather(latitude: float, longitude: float) -> str:
    """
    Fetches real-time weather description based on GPS coordinates 
    using the free Open-Meteo API.
    """
    if not latitude or not longitude:
        return "Pleasant outdoor weather"

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code"
    
    # Simple weather code mapping
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        51: "Light drizzle",
        61: "Rain showers",
        71: "Snowing",
        95: "Thunderstorm"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=3.0)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current", {})
                temp = current.get("temperature_2m", 20)
                code = current.get("weather_code", 0)
                condition = weather_descriptions.get(code, "Mild outdoor conditions")
                return f"{condition}, {temp}°C"
    except Exception:
        pass
    
    return "Pleasant outdoor weather"