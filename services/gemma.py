import os
import json
import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from the .env file")

client = genai.Client(api_key=api_key)


async def get_local_weather(latitude: float | None, longitude: float | None) -> str:
    """
    Fetches real-time weather description based on GPS coordinates 
    using the free Open-Meteo API.
    """
    if latitude is None or longitude is None:
        return "Pleasant outdoor weather, mild conditions"

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code"
    
    weather_descriptions = {
        0: "Clear sky and bright sun",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast and cloudy",
        51: "Light drizzle and damp air",
        61: "Rain showers and wet conditions",
        71: "Snowing and crisp cold air",
        95: "Thunderstorm and stormy atmosphere"
    }

    try:
        async with httpx.AsyncClient() as client_http:
            response = await client_http.get(url, timeout=3.0)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current", {})
                temp = current.get("temperature_2m", 20)
                code = current.get("weather_code", 0)
                condition = weather_descriptions.get(code, "Mild outdoor conditions")
                return f"{condition}, {temp}°C"
    except Exception:
        pass
    
    return "Pleasant outdoor weather, mild conditions"


async def analyze_image(
    image_bytes: bytes, 
    mime_type: str, 
    latitude: float | None = None, 
    longitude: float | None = None
):
    # 1. Fetch real-time weather dynamically based on user's location
    weather_condition = await get_local_weather(latitude, longitude)

    # 2. Weather-aware & adventure-driven prompt
    prompt = f"""
    You are TrailLens, an elite outdoor exploration companion, wilderness guide, and witty nature adventurer.

    Current Environmental Weather: {weather_condition}

    Analyze the user's outdoor photograph and return ONLY valid JSON
    with exactly these fields:

    {{
        "observation": "What is visible in the photo",
        "description": "A short, vivid, and engaging explanation",
        "interesting_fact": "One mind-blowing, quirky, or fascinating natural fact",
        "mission": {{
            "title": "A thrilling, funny, or catchy mission title (e.g., 'The Stealthy Forest Ninja', 'Whispering Canopy Detective', 'Ancient Tree Historian')",
            "instruction": "A deeply immersive, adventurous, humorous, and sensory 5-minute screen-off outdoor challenge tailored specifically to the current weather ({weather_condition}). E.g., if raining, focus on listening to drops or damp scents; if sunny, focus on tracking leaf shadows or canopy light rays. The phone MUST stay in the pocket/screen-off.",
            "duration_minutes": 5
        }}
    }}

    CRITICAL RULES FOR MISSIONS:
    - Match the vibe and challenge to the current weather ({weather_condition}).
    - NEVER suggest boring tasks like 'match the color', 'find something red', or looking at phone screens. 
    - Make them playful, slightly adventurous, humorous, and deeply sensory.
    - Must be 100% safe: Never suggest touching unknown plants, approaching wild animals, climbing steep ledges, or leaving the trail.
    """

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.85,
            ),
        )

        if not response.text:
            raise ValueError("AI returned an empty response")

        result_text = response.text.strip()

        if result_text.startswith("```"):
            result_text = result_text.removeprefix("```json").removesuffix("```").strip()

        return json.loads(result_text)

    except Exception as e:
        print(f"❌ GEMINI API ERROR: {str(e)}")
        raise e


async def verify_mission_discovery(
    mission_title: str,
    mission_instruction: str,
    image_bytes: bytes,
    mime_type: str
):
    prompt = f"""
    You are TrailLens, an elite outdoor exploration companion and witty wilderness guide.

    The user was given this 5-minute outdoor mission:
    - Title: "{mission_title}"
    - Instruction: "{mission_instruction}"

    The user has now finished their 5-minute screen-off session and uploaded a photo of their "Discovery".
    Analyze the uploaded photo and return ONLY valid JSON with these fields:
    
    {{
        "verified": true/false (Does this photo reasonably match the spirit or target of the mission?),
        "feedback": "A witty, encouraging, or humorous critique of what they found and how well it fits the mission.",
        "points_earned": 10
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
            ),
        )

        if not response.text:
            return {"verified": True, "feedback": "Great effort out on the trail!", "points_earned": 10}

        result_text = response.text.strip()
        if result_text.startswith("```"):
            result_text = result_text.removeprefix("```json").removesuffix("```").strip()

        return json.loads(result_text)
        
    except Exception as e:
        print(f"❌ VERIFICATION ERROR: {str(e)}")
        return {"verified": True, "feedback": "Fantastic discovery on your journey!", "points_earned": 10}