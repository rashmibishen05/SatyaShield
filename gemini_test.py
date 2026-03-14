import os
from dotenv import load_dotenv
from google import genai


load_dotenv(override=True)
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


user_query = input("Enter the information you want to verify: ")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"Tell whether the following information is TRUE or FALSE and explain briefly: {user_query}"
)

print("\nResult:\n")
print(response.text)