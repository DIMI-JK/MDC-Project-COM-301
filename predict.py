import joblib
import pandas as pd

# Load the trained model
model = joblib.load("fake_review_model.joblib")

# Enter review details
review_text = input("Enter review text: ").strip()

try:
    rating = float(input("Enter rating (1-5): "))
except ValueError:
    raise ValueError("Rating must be a number between 1 and 5.")

if not review_text:
    raise ValueError("Review text cannot be empty.")

if not 1 <= rating <= 5:
    raise ValueError("Rating must be between 1 and 5.")

# Prepare input in the same format used during training
input_data = pd.DataFrame({
    "review_text": [review_text],
    "rating": [rating]
})

# Predict
prediction = model.predict(input_data)[0]
probabilities = model.predict_proba(input_data)[0]

# Labels: CG = Fake, OG = Genuine
label = "CG (Fake)" if prediction == 1 else "OG (Genuine)"

print("\nPrediction:", label)
print(f"Confidence for OG (Genuine): {probabilities[0] * 100:.2f}%")
print(f"Confidence for CG (Fake): {probabilities[1] * 100:.2f}%")