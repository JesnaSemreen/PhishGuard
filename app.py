from flask import Flask, render_template, request
import joblib
import pandas as pd

from features.url_features import extract_basic_features
from urllib.parse import urlparse
from email_detector import analyze_email
print("All imports completed")

app = Flask(__name__)

# Load the trained PhishGuard model
model = joblib.load("model/phishguard_model.pkl")

print("PhishGuard model loaded successfully!")

def normalize_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():

    # Get URL entered by the user
    url = request.form["url"].strip()

    if not url:
        return render_template(
            "index.html",
            error="Please enter a URL."
        )

    url = normalize_url(url)

    parsed_url = urlparse(url)

    if not parsed_url.netloc or "." not in parsed_url.netloc:
        return render_template(
            "index.html",
         error="Please enter a valid URL."
        )

    print("\nURL received:", url)

    # Extract features from the URL
    features = extract_basic_features(url)

    # Display extracted features in terminal
    print("Extracted Features:", features)

    # Convert features into a DataFrame
    input_data = pd.DataFrame([features]).drop(columns=["IsHTTPS"])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Label 0 = Phishing
    # Label 1 = Legitimate
    phishing_probability = probabilities[0] * 100

    # Convert prediction into readable text
    if prediction == 0:
        prediction_text = "Phishing"
    else:
        prediction_text = "Legitimate"

    # Project-defined risk classification
    if phishing_probability < 30:
        risk = "Low Risk"
    elif phishing_probability < 70:
        risk = "Medium Risk"
    else:
        risk = "High Risk"
        # Generate reasons for the prediction
    reasons = []

    if features["IsHTTPS"] == 0:
        reasons.append(
            "The URL does not use HTTPS, which is an important security signal."
        )

    if features["NoOfOtherSpecialCharsInURL"] >= 8:
        reasons.append(
            "The URL contains several special characters, which can be associated with suspicious URLs."
        )

    if features["NoOfDegitsInURL"] >= 3:
        reasons.append(
            "The URL contains several digits, which can be a suspicious characteristic."
        )

    if features["NoOfSubDomain"] >= 2:
        reasons.append(
            "The URL contains multiple subdomains, which can sometimes be used in deceptive URLs."
        )

    if features["URLLength"] >= 75:
        reasons.append(
            "The URL is unusually long, which can be a characteristic of phishing URLs."
        )

    if features["DomainLength"] >= 30:
        reasons.append(
            "The domain is relatively long, which can be associated with suspicious URLs."
        )

    if features["NoOfLettersInURL"] >= 40:
        reasons.append(
            "The URL contains a large number of letters."
        )

    # Fallback explanation
    if not reasons:
        reasons.append(
            "The URL does not show strong warning signs among the analyzed features."
        )
    # Security recommendation
    if risk == "High Risk":
        recommendation = (
            "This URL shows characteristics associated with phishing. "
            "Avoid entering passwords, payment details, or other sensitive information."
        )

    elif risk == "Medium Risk":
        recommendation = (
            "This URL has some suspicious characteristics. "
            "Verify the website carefully before entering sensitive information."
        )

    else:
        recommendation = (
            "This URL has a low estimated phishing risk based on the analyzed features. "
            "Still verify the website before entering sensitive information."
        )

    # Send all information to the result page
    return render_template(
        "result.html",
        url=url,
        prediction=prediction_text,
        phishing_probability=f"{phishing_probability:.2f}",
        risk=risk,
        features=features,
        recommendation=recommendation,
        reasons=reasons
    )


@app.route("/scan-email", methods=["POST"])
def scan_email():
    email = request.form.get("email", "").strip()

    if not email:
        return render_template(
            "index.html",
            email_error="Please paste an email message to analyze."
        )

    try:
        result = analyze_email(email)
    except ValueError as error:
        return render_template(
            "index.html",
            email_error=str(error)
        )

    return render_template(
        "email_result.html",
        result=result
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)