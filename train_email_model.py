
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# File paths
DATASET_PATH = "dataset/Balanced_Dataset.csv"
MODEL_DIR = "email_model"
MODEL_PATH = os.path.join(MODEL_DIR, "email_phishing_model.pkl")

# Create the model folder if it does not exist
os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading email dataset...")

df = pd.read_csv(DATASET_PATH, usecols=["body", "label"])

# Remove empty email bodies
df = df.dropna(subset=["body"])
df["body"] = df["body"].astype(str).str.strip()
df = df[df["body"] != ""]

# Remove exact duplicate email bodies before splitting
df = df.drop_duplicates(subset=["body"]).reset_index(drop=True)

# Confirm labels
df["label"] = df["label"].astype(int)

print("\nDataset size after cleaning:", len(df))
print("Label counts:")
print(df["label"].value_counts())

# 0 = legitimate, 1 = phishing
X = df["body"]
y = df["label"]

# Split before fitting the vectorizer to avoid test-data leakage
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Text preprocessing and classification in one pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
            max_features=100000,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )
    )
])

print("\nTraining email detection model...")
model.fit(X_train, y_train)

print("Evaluating model...")
y_pred = model.predict(X_test)

print("\nEmail Model Performance")
print("-----------------------")
print(f"Accuracy : {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
print(f"Recall   : {recall_score(y_test, y_pred, zero_division=0):.4f}")
print(f"F1 Score : {f1_score(y_test, y_pred, zero_division=0):.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Legitimate", "Phishing"],
    zero_division=0
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save the complete pipeline so prediction uses the same TF-IDF settings
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved successfully: {MODEL_PATH}")
