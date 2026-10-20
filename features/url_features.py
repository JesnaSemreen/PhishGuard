from urllib.parse import urlparse


def extract_basic_features(url):
    parsed_url = urlparse(url)

    features = {}

    # 1. Total URL length
    features["URLLength"] = len(url)

    # 2. Domain
    domain = parsed_url.netloc

    # Remove port if present
    domain = domain.split(":")[0]

    # 3. Domain length
    features["DomainLength"] = len(domain)

    # 4. Check whether domain is an IP address
    try:
        parts = domain.split(".")
        is_ip = len(parts) == 4 and all(
            part.isdigit() and 0 <= int(part) <= 255
            for part in parts
        )
    except Exception:
        is_ip = False

    features["IsDomainIP"] = int(is_ip)

    # 5. Number of subdomains
    domain_parts = domain.split(".")
    features["NoOfSubDomain"] = max(len(domain_parts) - 2, 0)

    # 6. HTTPS
    features["IsHTTPS"] = int(parsed_url.scheme.lower() == "https")

    # 7. Number of letters in URL
    features["NoOfLettersInURL"] = sum(char.isalpha() for char in url)

    # 8. Number of digits in URL
    features["NoOfDegitsInURL"] = sum(char.isdigit() for char in url)

    # 9. Number of '?'
    features["NoOfQMarkInURL"] = url.count("?")

    # 10. Number of '='
    features["NoOfEqualsInURL"] = url.count("=")

    # 11. Number of '&'
    features["NoOfAmpersandInURL"] = url.count("&")

    # 12. Number of special characters
    features["NoOfOtherSpecialCharsInURL"] = sum(
        not char.isalnum() and char not in "?=&"
        for char in url
    )

    return features