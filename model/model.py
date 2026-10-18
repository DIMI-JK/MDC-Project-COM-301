import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# Load the separate datasets
train_df = pd.read_csv("fake_reviews_train.csv")
test_df = pd.read_csv("fake_reviews_test.csv")

required = {"review_text", "rating", "label"}

for name, data in [("Training", train_df), ("Testing", test_df)]:
    if not required.issubset(data.columns):
        raise ValueError(f"{name} CSV must contain {required}")

def clean_data(df):
    df = df.dropna(subset=["review_text", "rating", "label"]).copy()
    df["review_text"] = df["review_text"].astype(str).str.strip()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["label"] = df["label"].astype(str).str.strip().str.upper()

    df = df.dropna(subset=["rating"])
    df = df[df["review_text"] != ""]
    df = df[df["rating"].between(1, 5)]
    df = df[df["label"].isin(["CG", "OR"])]

    return df

train_df = clean_data(train_df)
test_df = clean_data(test_df)

# CG = 1 (fake), OR = 0 (genuine)
mapping = {"CG": 1, "OR": 0}

X_train = train_df[["review_text", "rating"]]
y_train = train_df["label"].map(mapping).astype(int)

X_test = test_df[["review_text", "rating"]]
y_test = test_df["label"].map(mapping).astype(int)

if y_train.nunique() != 2 or y_test.nunique() != 2:
    raise ValueError("Both datasets must contain CG and OR reviews.")

preprocessor = ColumnTransformer([
    ("text", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=50000,
        sublinear_tf=True
    ), "review_text"),
    ("rating", StandardScaler(), ["rating"])
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ))
])

# Train only on the training CSV
model.fit(X_train, y_train)

# Evaluate on the untouched testing CSV
predictions = model.predict(X_test)

print("Accuracy:", round(
    accuracy_score(y_test, predictions), 4
))

print(classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["OR (Genuine)", "CG (Fake)"],
    zero_division=0
))

print("Confusion matrix:")
print(confusion_matrix(
    y_test, predictions, labels=[0, 1]
))

joblib.dump(model, "fake_review_model.joblib")
print("Model saved successfully.")
