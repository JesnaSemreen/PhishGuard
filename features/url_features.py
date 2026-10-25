
from urllib.parse import urlparse, urlunparse
import ipaddress


def extract_basic_features(url):
    url = str(url).strip() if url is not None else ""

    candidate = url if "://" in url else "https://" + url
    parsed = urlparse(candidate)

    hostname = (parsed.hostname or "").lower()
    path = parsed.path or ""

    if path == "/" and not parsed.query and not parsed.fragment:
        parsed = parsed._replace(path="")
        path = ""

    normalized_url = urlunparse(parsed)

    # Canonical hostname: ignore an optional leading www.
    domain = hostname.removeprefix("www.")
    domain_parts = [part for part in domain.split(".") if part]

    # Use a consistent hostname when calculating URL features.
    canonical_netloc = domain
    if parsed.port is not None:
        canonical_netloc = f"{domain}:{parsed.port}"

    canonical_parsed = parsed._replace(netloc=canonical_netloc)
    canonical_url = urlunparse(canonical_parsed)
    # Use a consistent scheme for structural URL features.
    
    canonical_url = urlunparse(canonical_parsed)

    features = {}

    features["URLLength"] = len(canonical_url)
    features["DomainLength"] = len(domain)

    try:
        ipaddress.ip_address(domain)
        is_ip = 1
    except ValueError:
        is_ip = 0

    features["IsDomainIP"] = is_ip
    features["NoOfSubDomain"] = max(len(domain_parts) - 2, 0)
    features["IsHTTPS"] = int(parsed.scheme.lower() == "https")
    features["NoOfLettersInURL"] = sum(c.isalpha() for c in canonical_url)
    features["NoOfDegitsInURL"] = sum(c.isdigit() for c in canonical_url)
    features["NoOfQMarkInURL"] = canonical_url.count("?")
    features["NoOfEqualsInURL"] = canonical_url.count("=")
    features["NoOfAmpersandInURL"] = canonical_url.count("&")
    features["NoOfOtherSpecialCharsInURL"] = sum(
        not c.isalnum() and c not in "?=&"
        for c in canonical_url
    )

    features["HostnameLabelCount"] = len(domain_parts)
    features["HyphensInHostname"] = domain.count("-")
    features["DigitsInHostname"] = sum(c.isdigit() for c in domain)
    features["PathLength"] = len(path)
    features["QueryLength"] = len(parsed.query)
    features["FragmentPresent"] = int(bool(parsed.fragment))
    features["AtSymbolPresent"] = int("@" in parsed.netloc)
    features["PercentEncodingCount"] = canonical_url.count("%")

    try:
        features["HasPort"] = int(parsed.port is not None)
    except ValueError:
        features["HasPort"] = 0

    return features
