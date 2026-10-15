import joblib

model = joblib.load("fake_review_model.joblib")

def predict_review(review_text):
    if not review_text or not review_text.strip():
        raise ValueError("Review text cannot be empty")

    prediction = int(model.predict([review_text])[0])
    probabilities = model.predict_proba([review_text])[0]
    class_index = list(model.classes_).index(prediction)
    confidence = float(probabilities[class_index]) * 100

    label = "Likely fake" if prediction == 1 else "Likely genuine"

    print("Review:", review_text)
    print("Prediction:", label)
    print(f"Model confidence: {confidence:.2f}%")

if __name__ == "__main__":
    review = input("Enter a product review: ")
    predict_review(review)