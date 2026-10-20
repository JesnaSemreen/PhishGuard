from features.url_features import extract_basic_features

url = "https://example.com/login?id=123"

features = extract_basic_features(url)

print("URL:", url)
print("\nExtracted Features:")

for name, value in features.items():
    print(f"{name}: {value}")