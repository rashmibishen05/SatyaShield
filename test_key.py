import os
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.environ.get("GEMINI_API_KEY")
print(f"Using API Key: {api_key[:10]}...{api_key[-5:] if api_key else ''}")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hello, is this API key working?"
    )
    print("Success! Response:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
