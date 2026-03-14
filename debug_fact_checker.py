from fact_checker import check_claim
import os

print(f"Testing with API Key: {os.environ.get('GEMINI_API_KEY')[:10]}...")
result = check_claim("Is the earth flat?")
print("\n--- RESULT ---")
print(result)
print("--------------")
