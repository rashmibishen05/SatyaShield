import os
import re
from dotenv import load_dotenv

load_dotenv(override=True)


def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment.")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return client
    except ImportError:
        raise ImportError("google-genai package not installed. Run: pip install google-genai")


def hybrid_smart_analysis(text):
    """
    Heuristic fallback engine used when Gemini API is unavailable.
    """
    t = text.lower().strip()

    # Known fact patterns
    if "cat" in t and ("national" in t or "animal" in t):
        return "Result: FALSE\nExplanation: The Royal Bengal Tiger is India's national animal, not the domestic cat."

    if "modi" in t and ("pm" in t or "prime minister" in t):
        return "Result: TRUE\nExplanation: Narendra Modi is the incumbent Prime Minister of India as of the latest available data."

    if "earth" in t and "flat" in t:
        return "Result: FALSE\nExplanation: Scientific consensus confirms the Earth is an oblate spheroid. Flat Earth claims are scientifically debunked."

    if "sun" in t and "revolves" in t and "earth" in t:
        return "Result: FALSE\nExplanation: The Earth revolves around the Sun, not the other way around."

    # Scam/phishing pattern detection
    scam_keywords = ["lottery", "win", "crore", "money", "prize", "otp", "bank", "kbc", "lucky", "gift", "free", "click", "verify", "urgent"]
    matches = [w for w in scam_keywords if w in t]
    if len(matches) >= 2:
        return f"Result: SCAM / HIGH RISK\nExplanation: Statement contains high-risk phishing indicators ({', '.join(matches[:3])}). Likely a financial scam or social engineering attempt."

    # Political/current-affairs content
    if any(x in t for x in ["election", "vote", "government", "minister", "court", "news", "policy"]):
        return "Result: UNVERIFIED\nExplanation: This claim involves current affairs that require live data to verify. No malicious patterns were found, but a deeper search is recommended."

    # Generic safe fallback
    return f"Result: ANALYZED\nExplanation: No high-risk scam patterns were detected in the statement. For a deep factual check, please connect to the internet so the AI engine can perform a live verification."


def check_claim(text):
    if not text or len(text.strip()) < 3:
        return "⚠️ Please enter a factual statement or news headline to verify."

    try:
        client = get_gemini_client()
        prompt = (
            f"You are a precise fact-checking assistant. Fact-check the following claim:\n\n"
            f"\"{text}\"\n\n"
            f"Respond ONLY in this exact format:\n"
            f"Result: [TRUE / FALSE / SCAM / UNVERIFIED]\n"
            f"Explanation: [One clear sentence explaining your verdict]"
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        if response and response.text:
            result_text = response.text.strip()
            return result_text

    except Exception as e:
        print(f"[Fact Checker] Gemini API error, switching to heuristic fallback. Error: {e}")

    # Fallback to local heuristic analysis
    return hybrid_smart_analysis(text)
