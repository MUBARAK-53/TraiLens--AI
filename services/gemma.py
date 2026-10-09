
import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from the .env file")

client = genai.Client(api_key=api_key)


async def analyze_image(image_bytes: bytes, mime_type: str):
    prompt = """
    You are TrailLens, an outdoor exploration companion.

    Analyze the user's outdoor photograph and return ONLY valid JSON
    with exactly these fields:

    {
        "observation": "What is visible",
        "description": "A short explanation",
        "interesting_fact": "One useful fact",
        "mission": {
            "title": "Short mission title",
            "instruction": "A safe physical outdoor activity",
            "duration_minutes": 5
        }
    }

    The mission must encourage the user to explore outdoors without
    staring at the phone. It must be safe, require no special equipment,
    and take approximately 5 minutes.

    Never suggest touching unknown plants, approaching wildlife,
    climbing, or entering restricted areas.
    """

    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=[
            prompt,
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_bytes,
                }
            },
        ],
    )

    if not response.text:
        raise ValueError("Gemma returned an empty response")

    result_text = response.text.strip()

    if result_text.startswith("```"):
        result_text = result_text.removeprefix("```json")
        result_text = result_text.removesuffix("```").strip()

    return json.loads(result_text)
