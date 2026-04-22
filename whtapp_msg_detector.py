import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Massively expanded scam keyword database
SCAM_KEYWORDS = [
    "share with", "forward to", "get free recharge", "win money", "lottery",
    "urgent forward", "bank details", "otp", "kbc", "congratulations you have won",
    "click the link", "claim your prize", "free gift", "lucky winner",
    "100% free", "act now", "limited time", "verify your account",
    "send this to", "your account will be blocked", "government scheme",
    "pm kisan", "modi free", "jio free", "airtel free recharge",
    "won 6 crore", "won 5 crore", "won 1 crore", "crore lottery", "amount credited",
    "scan and use", "scan this qr", "payment received", "cash prize"
]

SUSPICIOUS_KEYWORDS = [
    "congratulations", "selection", "recharge", "free", "win", "prize",
    "urgent", "click here", "verify", "confirm", "expire", "blocked",
    "warning", "alert", "lottery", "lucky", "won", "amount", "crore", "scan"
]


def heuristic_scam_check(text):
    """Keyword-based heuristic scam detection."""
    t = text.lower()

    hard_matches = [kw for kw in SCAM_KEYWORDS if kw in t]
    soft_matches = [kw for kw in SUSPICIOUS_KEYWORDS if kw in t]

    # If it contains "won" and "lottery" or "crore", it's an immediate High Risk
    if ("won" in t and ("lottery" in t or "crore" in t or "prize" in t)):
        return (
            f"🚨 Result: HIGH RISK SCAM\n"
            f"Explanation: Message follows a classic lottery/prize scam pattern. "
            f"Promises of large sums of money ({' ,'.join(soft_matches[:2])}) are 100% fraudulent."
        )

    if len(hard_matches) >= 2 or (len(hard_matches) >= 1 and len(soft_matches) >= 2):
        matched = list(set(hard_matches + soft_matches))[:4]
        return (
            f"🚨 Result: HIGH RISK SCAM\n"
            f"Explanation: Message contains multiple scam indicators: {', '.join(matched)}.\n"
            f"This appears to be a WhatsApp scam designed to steal personal information or money."
        )
    elif len(hard_matches) == 1 or len(soft_matches) >= 2:
        matched = list(set(hard_matches + soft_matches))[:3]
        return (
            f"⚠️ Result: SUSPICIOUS\n"
            f"Explanation: Message contains suspicious keywords ({', '.join(matched)}) "
            f"commonly found in phishing or scam messages. Proceed with caution."
        )
    else:
        return (
            f"✅ Result: LOOKS SAFE\n"
            f"Explanation: No known scam patterns detected in this message. "
            f"However, always be cautious with messages asking for personal or financial information."
        )


def detect_whatsapp_scam(text):
    if not text or len(text.strip()) < 3:
        return "⚠️ Please enter a message to analyze."

    # --- Try Gemini AI first ---
    try:
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            client = genai.Client(api_key=api_key)
            prompt = (
                f"You are an expert in detecting WhatsApp scams, phishing messages, and social engineering attacks. "
                f"Analyze the following message:\n\n\"{text}\"\n\n"
                f"Look for: lottery scams, OTP fraud, fake government schemes, prize winning hoaxes, "
                f"urgent forwarding requests, bank/credential phishing, and fake job offers. "
                f"Respond ONLY in this format:\n"
                f"Result: [SAFE / SUSPICIOUS / HIGH RISK SCAM]\n"
                f"Explanation: [One clear sentence explaining your verdict]"
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            if response and response.text:
                res = response.text.strip()
                # Ensure the emoji is present for the JS coloring
                if "HIGH RISK" in res and "🚨" not in res: res = "🚨 " + res
                if "SUSPICIOUS" in res and "⚠️" not in res: res = "⚠️ " + res
                if "SAFE" in res and "✅" not in res: res = "✅ " + res
                return res
    except Exception as e:
        print(f"[WhatsApp Detector] Gemini error, using heuristic fallback. Error: {e}")

    # --- Fallback: Heuristic analysis ---
    return heuristic_scam_check(text)
