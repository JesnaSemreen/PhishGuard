
import joblib
import shap

# Load the trained email detection model
# Load the trained email detection model
model = joblib.load("email_model/email_phishing_model.pkl")




# Access the TF-IDF vectorizer and classifier
vectorizer = model.named_steps["tfidf"]
classifier = model.named_steps["classifier"]

# Reference emails for SHAP explanations
background_emails = [
    "Hi team, our meeting is scheduled for tomorrow.",
    "Please find the project report attached.",
    "Thank you for your response. Have a nice day.",
    "Your invoice for this month is attached.",
    "Please review the documents before the meeting."
]

background = vectorizer.transform(background_emails)

# Create the SHAP explainer once
explainer = shap.LinearExplainer(
    classifier,
    background
)


def analyze_email(email):
    email = email.strip()

    if not email:
        raise ValueError("Please enter an email to analyze.")

    prediction = int(model.predict([email])[0])
    probabilities = model.predict_proba([email])[0]

    # Label 0 = Legitimate, Label 1 = Phishing
    result = "Phishing" if prediction == 1 else "Legitimate"

    legitimate_probability = float(probabilities[0] * 100)
    phishing_probability = float(probabilities[1] * 100)

    # Generate SHAP explanations
    email_vector = vectorizer.transform([email])
    shap_values = explainer(email_vector)

    values = shap_values.values
    if values.ndim == 3:
        values = values[0, :, 1]
    else:
        values = values.reshape(-1)

    feature_names = vectorizer.get_feature_names_out()
    present_indices = email_vector.indices

    top_indices = sorted(
        present_indices,
        key=lambda i: abs(values[i]),
        reverse=True
    )[:10]

    explanations = []

    for i in top_indices:
        explanations.append({
            "word": feature_names[i],
            "value": float(values[i]),
            "direction": (
                "phishing" if values[i] > 0
                else "legitimate"
            )
        })

    return {
        "prediction": result,
        "legitimate_probability": round(
            legitimate_probability, 2
        ),
        "phishing_probability": round(
            phishing_probability, 2
        ),
        "explanations": explanations
    }
