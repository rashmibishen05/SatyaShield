import tldextract

TRUSTED_DOMAINS = [
    "google", "facebook", "amazon", "microsoft", "apple", "netflix",
    "twitter", "instagram", "linkedin", "wikipedia", "youtube",
    "github", "stackoverflow", "reddit", "spotify", "adobe",
    "paypal", "ebay", "flipkart", "myntra", "zomato", "swiggy",
    "paytm", "phonepe", "razorpay", "hdfc", "sbi", "icici", "axis"
]

TRUSTED_TLDS = ["gov", "edu", "ac", "org", "co"]

SUSPICIOUS_TLDS = [
    "top", "xyz", "icu", "pw", "bid", "loan", "click", "site",
    "online", "info", "biz", "ws", "tk", "ml", "ga", "cf", "gq"
]

SCAM_KEYWORDS = [
    "free", "earn", "win", "offer", "lottery", "recharge", "gift",
    "login-verify", "secure-update", "account-confirm", "verify-now",
    "claim-prize", "lucky-draw", "otp", "phish", "hack", "scam"
]


def check_url(url):
    url = url.strip()
    if not url:
        return "⚠️ Please enter a URL to scan."

    # Add scheme if missing for proper parsing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    ext = tldextract.extract(url)
    domain = ext.domain.lower()
    suffix = ext.suffix.lower()
    subdomain = ext.subdomain.lower()

    if not domain:
        return "❌ Invalid URL format. Please enter a valid web address."

    # IP address detection
    domain_parts = ext.registered_domain or domain
    if all(part.isdigit() for part in domain.replace('.', ' ').split()):
        return (
            "🚨 High Risk: IP Address URL Detected\n"
            "This URL uses a raw IP address instead of a domain name — "
            "a common technique used by phishing sites to hide their identity."
        )

    # Suspicious TLD check
    if suffix in SUSPICIOUS_TLDS:
        return (
            f"🚨 High Risk: Suspicious Domain Extension (.{suffix})\n"
            f"The '.{suffix}' extension is frequently used in scam and phishing websites. "
            f"Avoid clicking this link unless you are absolutely certain of the source."
        )

    # Trusted domain check (do this before keyword check)
    if domain in TRUSTED_DOMAINS or suffix in TRUSTED_TLDS:
        # Check for suspicious subdomains that mimic trusted brands (e.g., google.phish.com)
        if subdomain and any(brand in subdomain for brand in TRUSTED_DOMAINS):
            return (
                f"🚨 High Risk: Subdomain Spoofing Detected\n"
                f"The subdomain '{subdomain}' mimics a trusted brand but the actual domain is '{domain}.{suffix}'. "
                f"This is a classic phishing technique."
            )
        return (
            f"✅ URL Appears Safe\n"
            f"'{domain}.{suffix}' matches a verified, trusted domain. "
            f"Always ensure you are on the correct website before entering credentials."
        )

    # Scam keyword check
    full_url_lower = url.lower()
    for word in SCAM_KEYWORDS:
        if word in full_url_lower:
            return (
                f"🚨 High Risk: Scam Keyword Detected ('{word}')\n"
                f"This URL contains the keyword '{word}' which is commonly used in phishing "
                f"and online scam campaigns. Do not enter personal information on this site."
            )

    # Domain pattern analysis (gibberish detection)
    vowels = set("aeiou")
    vowel_count = sum(1 for c in domain if c in vowels)
    consonant_ratio = (len(domain) - vowel_count) / max(len(domain), 1)

    if len(domain) > 20:
        return (
            f"⚠️ Suspicious: Unusually Long Domain Name\n"
            f"The domain '{domain}.{suffix}' is very long ({len(domain)} characters), "
            f"which is a common trait of auto-generated phishing domains."
        )

    if consonant_ratio > 0.75 or vowel_count == 0:
        return (
            f"⚠️ Suspicious: Domain Looks Auto-Generated\n"
            f"The domain '{domain}' has an unusual letter pattern (no vowels or very few). "
            f"This is a common trait of randomly generated scam domains."
        )

    return (
        f"⚠️ Unverified Domain: Proceed With Caution\n"
        f"'{domain}.{suffix}' is not on our trusted domain list. "
        f"This does not mean it is harmful, but exercise caution — "
        f"do not enter passwords or payment information unless you trust this site."
    )
