import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# Load labelled dataset
df = pd.read_csv("dataset.csv")

required_columns = {"review_text", "label"}
if not required_columns.issubset(df.columns):
    raise ValueError(
        "dataset.csv must contain review_text and label columns"
    )

df = df.dropna(subset=["review_text", "label"])
df["review_text"] = df["review_text"].astype(str).str.strip()
df = df[df["review_text"] != ""]
df["label"] = pd.to_numeric(df["label"], errors="raise")

if not set(df["label"].unique()).issubset({0, 1}):
    raise ValueError("Labels must be 0 (genuine) or 1 (fake)")

if df["label"].nunique() != 2 or df["label"].value_counts().min() < 2:
    raise ValueError("Need at least two examples of each label")

X = df["review_text"]
y = df["label"].astype(int)

# Keep both classes represented in train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Text classification pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=50000,
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

# Train
model.fit(X_train, y_train)

# Evaluate on unseen test data
predictions = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, predictions), 4))
print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Genuine", "Fake"],
        zero_division=0
    )
)

print("\nConfusion matrix:")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))

# Save trained pipeline
joblib.dump(model, "fake_review_model.joblib")
print("\nModel saved as fake_review_model.joblib")
