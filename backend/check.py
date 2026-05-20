from urllib.parse import urlparse
import re

def normalize_url(url: str) -> str:
    if "://" not in url:
        return "http://" + url
    return url


def extract_features(url: str):
    url = normalize_url(url.strip())
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    return [
        len(url),
        url.count('.'),
        1 if url.startswith("https") else 0,
        1 if '@' in url else 0,
        1 if '-' in domain else 0,
        len(domain),
        sum(c.isdigit() for c in url),
        sum(not c.isalnum() for c in url),
        1 if re.match(r"\d+\.\d+\.\d+\.\d+", domain) else 0
    ]