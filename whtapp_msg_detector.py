scam_keywords = [
    "share with", "forward to", "get free recharge", "win money", "lottery",
    "urgent forward", "bank details", "otp", "kbc", "selection", "congratulations"
]

def detect_whatsapp_scam(text):
    text = text.lower()
    
    match_count = 0
    for word in scam_keywords:
        if word in text:
            match_count += 1

    if match_count >= 2:
        return " High Risk: This message shows multiple signs of being a WhatsApp scam."
    elif match_count == 1:
        return " Caution: This message contains suspicious keywords found in typical scams."
    else:
        return "Message looks normal."
