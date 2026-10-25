import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from features.url_features import extract_basic_features


# ========================================
# 1. LOAD DATASET
# ========================================

file_path = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(file_path)

# Remove duplicate URLs
df = df.drop_duplicates(subset=["URL"])

print("========================================")
print("PHISHGUARD TRAINING")
print("========================================")
print("Unique URLs:", len(df))


# ========================================
# 2. EXTRACT URL FEATURES
# ========================================

print("\nExtracting features from URLs...")

all_features = []

for url in df["URL"]:
    all_features.append(extract_basic_features(url))

X = pd.DataFrame(all_features)
y = df["label"]
print("\nLabel counts:")
print(df["label"].value_counts())

print("\nMean URL features by label:")
print(X.groupby(y).mean().round(2).to_string())

print("Feature extraction completed!")
print("Features shape:", X.shape)
print("Target shape:", y.shape)


# ========================================
# 3. SPLIT DATA
# ========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ========================================
# 4. TRAIN RANDOM FOREST
# ========================================

print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model training completed!")


# ========================================
# 5. TEST MODEL
# ========================================

print("\nTesting model...")

y_pred = model.predict(X_test)

print("Testing completed!")


# ========================================
# 6. MODEL PERFORMANCE
# ========================================

accuracy = accuracy_score(y_test, y_pred)

phishing_precision = precision_score(
    y_test,
    y_pred,
    pos_label=0
)

phishing_recall = recall_score(
    y_test,
    y_pred,
    pos_label=0
)

phishing_f1 = f1_score(
    y_test,
    y_pred,
    pos_label=0
)

print("\n========================================")
print("PHISHGUARD MODEL PERFORMANCE")
print("========================================")

print(f"Accuracy          : {accuracy * 100:.2f} %")
print(f"Phishing Precision: {phishing_precision * 100:.2f} %")
print(f"Phishing Recall   : {phishing_recall * 100:.2f} %")
print(f"Phishing F1 Score : {phishing_f1 * 100:.2f} %")


# ========================================
# 7. CONFUSION MATRIX
# ========================================

cm = confusion_matrix(y_test, y_pred)

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================")

print(cm)

print("\nMatrix format:")
print("[[Phishing correctly classified, Phishing classified as Legitimate]")
print(" [Legitimate classified as Phishing, Legitimate correctly classified]]")


# ========================================
# 8. CLASSIFICATION REPORT
# ========================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Phishing", "Legitimate"]
    )
)


# ========================================
# 9. FEATURE IMPORTANCE
# ========================================

print("\n========================================")
print("FEATURE IMPORTANCE")
print("========================================")

for feature, importance in zip(
    X.columns,
    model.feature_importances_
):
    print(f"{feature}: {importance:.4f}")


# ========================================
# 10. SAVE MODEL
# ========================================

model_path = "model/phishguard_model.pkl"

joblib.dump(model, model_path)

print("\n========================================")
print("MODEL SAVED")
print("========================================")

print("Model saved successfully!")
print("Saved to:", model_path)


# ========================================
# 11. SAMPLE TEST URLs
# ========================================

legitimate_url = df[df["label"] == 1]["URL"].iloc[0]
phishing_url = df[df["label"] == 0]["URL"].iloc[0]

print("\n========================================")
print("SAMPLE TEST URLs")
print("========================================")

print("\nSample legitimate URL:")
print(legitimate_url)

print("\nSample phishing URL:")
print(phishing_url)

print("\n========================================")
print("TRAINING PIPELINE COMPLETED")
print("========================================")