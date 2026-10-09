
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

print("\n--- Checking available Gemma models ---")

try:
    for model in client.models.list():
        if "gemma" in model.name.lower():
            print(model.name, model.supported_actions)
except Exception as exc:
    print("Could not list models:", repr(exc))

print("\n--- Testing Gemma 4 ---")

try:
    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents="Reply with exactly: TrailLens is working"
    )
    print("SUCCESS:", response.text)
except Exception as exc:
    print("FAILED:", repr(exc))