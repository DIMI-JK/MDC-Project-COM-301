
import pandas as pd
import joblib

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# ---------------------------------
# 1. Load saved model and test data
# ---------------------------------

model = joblib.load("fake_review_model.joblib")
df = pd.read_csv("fake_reviews_test.csv")

# Required columns
required_columns = {"review_text", "rating", "label"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "Test dataset must contain review_text, rating, and label columns."
    )

# ---------------------------------
# 2. Clean test data
# ---------------------------------

df = df.dropna(subset=["review_text", "rating", "label"]).copy()

df["review_text"] = df["review_text"].astype(str).str.strip()
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["label"] = df["label"].astype(str).str.strip().str.upper()

df = df.dropna(subset=["rating"])
df = df[df["review_text"] != ""]
df = df[df["rating"].between(1, 5)]

# CG = Fake (1), OR = Genuine (0)
label_mapping = {
    "OR": 0,
    "CG": 1
}

df = df[df["label"].isin(label_mapping)].copy()
df["label"] = df["label"].map(label_mapping).astype(int)

if df.empty or df["label"].nunique() != 2:
    raise ValueError(
        "Test data must contain both OR and CG labels after cleaning."
    )

# ---------------------------------
# 3. Prepare features and true labels
# ---------------------------------

X_test = df[["review_text", "rating"]]
y_test = df["label"]

# ---------------------------------
# 4. Make predictions
# ---------------------------------

predictions = model.predict(X_test)

# ---------------------------------
# 5. Display evaluation metrics
# ---------------------------------

print("\nTest Dataset Size:", len(df))

print(
    "\nAccuracy:",
    round(accuracy_score(y_test, predictions), 4)
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["OR (Genuine)", "CG (Fake)"],
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

# ---------------------------------
# 6. Save individual predictions
# ---------------------------------

df["actual_label"] = df["label"].map({
    0: "OR (Genuine)",
    1: "CG (Fake)"
})

df["predicted_label"] = pd.Series(
    predictions, index=df.index
).map({
    0: "OR (Genuine)",
    1: "CG (Fake)"
})

df["correct_prediction"] = (
    df["label"].to_numpy() == predictions
)

df.to_csv("test_predictions.csv", index=False)

print("\nDetailed predictions saved to test_predictions.csv")
