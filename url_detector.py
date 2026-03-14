import tldextract
TRUSTED_DOMAINS = [
    "google", "facebook", "amazon", "microsoft", "apple", "netflix", 
    "twitter", "instagram", "linkedin", "wikipedia", "youtube", 
    "github", "gov", "edu", "org"
]

suspicious_keywords = [
    "free", "earn", "win", "offer", "lottery", "recharge", "gift", "login", "verify", "update"
]

def check_url(url):
    ext = tldextract.extract(url)
    domain = ext.domain.lower()
    suffix = ext.suffix.lower()

    if not domain:
        return " Invalid URL format."

    if domain.replace('.', '').isdigit():
        return " Highly Suspicious: URL uses an IP address instead of a domain name."

    
    suspicious_tld = ['top', 'xyz', 'icu', 'pw', 'bid', 'loan', 'click', 'site', 'online']
    if suffix in suspicious_tld:
        return f" High Risk: Uses a high-risk TLD (.{suffix}) often used for scams."

    for word in suspicious_keywords:
        if word in url.lower():
            return f" Suspicious: URL contains scam keyword '{word}'."

    
    if domain not in TRUSTED_DOMAINS:
    
        vowels = "aeiou"
        vowel_count = sum(1 for char in domain if char in vowels)
        if vowel_count == 0 or len(domain) > 15:
            return " Highly Suspicious: Domain looks like a random generation (gibberish)."
        
        return " Unverified Domain: This website is not on our trusted list. Proceed with caution."

    return " URL matches a trusted domain pattern."

