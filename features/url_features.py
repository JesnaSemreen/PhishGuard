
from urllib.parse import urlparse, urlunparse
import ipaddress


def extract_basic_features(url):
    # Safely handle empty or non-string values
    url = str(url).strip() if url is not None else ""

    # Parse consistently, even if the URL has no scheme
    candidate = url if "://" in url else "https://" + url
    parsed = urlparse(candidate)

    hostname = parsed.hostname or ""
    path = parsed.path or ""

    # Treat an optional root slash consistently
    if path == "/" and not parsed.query and not parsed.fragment:
        parsed = parsed._replace(path="")
        path = ""

    normalized_url = urlunparse(parsed)
    domain = hostname.lower()

    features = {}

    # Existing features
    features["URLLength"] = len(normalized_url)
    features["DomainLength"] = len(domain)

    try:
        ipaddress.ip_address(domain)
        is_ip = 1
    except ValueError:
        is_ip = 0

    features["IsDomainIP"] = is_ip

    domain_parts = [part for part in domain.split(".") if part]
    features["NoOfSubDomain"] = max(len(domain_parts) - 2, 0)

    features["IsHTTPS"] = int(parsed.scheme.lower() == "https")
    features["NoOfLettersInURL"] = sum(c.isalpha() for c in normalized_url)
    features["NoOfDegitsInURL"] = sum(c.isdigit() for c in normalized_url)
    features["NoOfQMarkInURL"] = normalized_url.count("?")
    features["NoOfEqualsInURL"] = normalized_url.count("=")
    features["NoOfAmpersandInURL"] = normalized_url.count("&")
    features["NoOfOtherSpecialCharsInURL"] = sum(
        not c.isalnum() and c not in "?=&"
        for c in normalized_url
    )

    # Additional structural features
    features["HostnameLabelCount"] = len(domain_parts)
    features["HyphensInHostname"] = domain.count("-")
    features["DigitsInHostname"] = sum(c.isdigit() for c in domain)
    features["PathLength"] = len(path)
    features["QueryLength"] = len(parsed.query)
    features["FragmentPresent"] = int(bool(parsed.fragment))
    features["AtSymbolPresent"] = int("@" in parsed.netloc)
    features["PercentEncodingCount"] = normalized_url.count("%")

    try:
        features["HasPort"] = int(parsed.port is not None)
    except ValueError:
        features["HasPort"] = 0

    return features
