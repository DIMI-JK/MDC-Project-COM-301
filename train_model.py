import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# Load dataset
df = pd.read_csv("train_8000.csv")

# Required columns
required_columns = {"review_text", "rating", "label"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "dataset.csv must contain review_text, rating, and label columns"
    )

# Clean data
df = df.dropna(subset=["review_text", "label"])
df["review_text"] = df["review_text"].astype(str).str.strip()
df = df[df["review_text"] != ""]

# Convert ratings to numeric
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df = df.dropna(subset=["rating"])

# Keep ratings within the usual 1–5 scale
df = df[df["rating"].between(1, 5)]

# Normalize labels
df["label"] = df["label"].astype(str).str.strip().str.upper()

# CG = Fake, OG = Genuine
label_mapping = {
    "CG": 1,
    "OG": 0
}

df = df[df["label"].isin(label_mapping)]
df["label"] = df["label"].map(label_mapping)

if df["label"].nunique() != 2:
    raise ValueError("Dataset must contain both CG and OG labels.")

if df["label"].value_counts().min() < 2:
    raise ValueError("Need at least two examples of each label.")

# Features and target
X = df[["review_text", "rating"]]
y = df["label"].astype(int)

# Split data while preserving class proportions
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Process text and rating separately
preprocessor = ColumnTransformer(
    transformers=[
        (
            "text",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                max_features=50000,
                sublinear_tf=True
            ),
            "review_text"
        ),
        (
            "rating",
            StandardScaler(),
            ["rating"]
        )
    ]
)

# Build model pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )
    )
])

# Train
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, predictions), 4))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["OG (Genuine)", "CG (Fake)"],
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    )
)

# Save the trained pipeline
joblib.dump(model, "fake_review_model.joblib")

print("\nModel saved as fake_review_model.joblib")