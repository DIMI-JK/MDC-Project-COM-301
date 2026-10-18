import joblib
import pandas as pd
from pathlib import Path

# Load the trained model
model = joblib.load("fake_review_model.joblib")

# Input and output CSV files
INPUT_FILE = "flipkart_reviews.csv"
OUTPUT_FILE = "review_predictions.csv"

# Load the reviews
df = pd.read_csv(INPUT_FILE)

# Check required columns
required_columns = ["text", "rating"]
missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Prepare data in the format used during training
input_data = pd.DataFrame({
    "review_text": df["text"].fillna("").astype(str),
    "rating": pd.to_numeric(df["rating"], errors="coerce")
})

# Handle missing or invalid values
valid = (
    input_data["review_text"].str.strip().ne("")
    & input_data["rating"].between(1, 5)
)

# Initialize result columns
df["prediction"] = "Not evaluated"
df["confidence_OG"] = None
df["confidence_CG"] = None

if valid.any():
    valid_data = input_data.loc[valid]

    # Predict review labels
    predictions = model.predict(valid_data)

    # Get probabilities for each class
    probabilities = model.predict_proba(valid_data)
    classes = list(model.classes_)

    # Find probability columns by class label
    og_index = classes.index(0)
    cg_index = classes.index(1)

    # Add decisions to the original CSV
    df.loc[valid, "prediction"] = [
        "CG (Fake)" if p == 1 else "OG (Genuine)"
        for p in predictions
    ]

    df.loc[valid, "confidence_OG"] = (
        probabilities[:, og_index] * 100
    ).round(2)

    df.loc[valid, "confidence_CG"] = (
        probabilities[:, cg_index] * 100
    ).round(2)

# Save all original columns plus the predictions
df.to_csv(OUTPUT_FILE, index=False)

# Print summary
print("\nReview detection completed!")
print(f"Total reviews: {len(df)}")
print(f"Evaluated reviews: {valid.sum()}")
print(f"Skipped reviews: {(~valid).sum()}")
print("\nPrediction summary:")
print(df["prediction"].value_counts().to_string())
print(f"\nResults saved to: {Path(OUTPUT_FILE).resolve()}")
