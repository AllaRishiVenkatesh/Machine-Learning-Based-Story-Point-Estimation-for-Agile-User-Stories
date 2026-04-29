import joblib
import os
import pandas as pd
from app.utils.preprocessing import preprocess_story

def test_model_inference():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "ml_artifacts", "model.joblib")
    vectorizer_path = os.path.join(base_dir, "ml_artifacts", "vectorizer.joblib")
    
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    test_cases = [
        "Migrate the entire collaborative editing service to a new WebSocket architecture to support 10k concurrent users.",
        "Fix typo in header",
        "As a user, I want to filter search results by price range so that I can find affordable items."
    ]
    
    print("\n--- Inference Test ---")
    for text in test_cases:
        clean = preprocess_story(text)
        vec = vectorizer.transform([clean])
        pred = model.predict(vec)[0]
        print(f"Input: {text[:50]}...")
        print(f"Raw Prediction: {pred:.4f}")
        print("-" * 30)

if __name__ == "__main__":
    test_model_inference()
