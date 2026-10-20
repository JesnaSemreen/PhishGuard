import pandas as pd

file_path = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
print("\nLabel distribution:")
print(df["label"].value_counts())
print("\nDataset information:")
df.info()
print("\nDuplicate URLs:")
print(df["URL"].duplicated().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())
# Remove duplicate URLs
df = df.drop_duplicates(subset=["URL"])

print("\nAfter removing duplicate URLs:")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))