import os
import sqlite3
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

# Use absolute imports or run as module, but for a script, simple relative path handling is needed
# if running from root.
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.preprocessing import clean_text

# 1. Load Data
# Using the merged real-world dataset from CSV folder
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "data", "merged_real_data.csv")

if os.path.exists(csv_path):
    print(f"Loading training data from: {csv_path}")
    df = pd.read_csv(csv_path)
    # Ensure columns match expectations
    if "story" not in df.columns or "points" not in df.columns:
        # Fallback mapping if headers are weird (though import_csv_folder ensures them)
        print("Warning: Columns 'story' or 'points' missing. Checking headers...")
        print(df.columns)
else:
    raise FileNotFoundError(f"Training data not found at {csv_path}. Run scripts/import_csv_folder.py first.")

print("Training data:")
print(df.head())

# 2. Preprocessing
print("Preprocessing...")
df['clean_text'] = df['story'].apply(clean_text)

# 3. Vectorization
print("Vectorizing...")
# Using TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['clean_text'])
y = df['points']

# 4. Model Training
print("Training RandomForest...")
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)

# 5. Saving Artifacts
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml_artifacts")
os.makedirs(output_dir, exist_ok=True)

model_path = os.path.join(output_dir, "model.joblib")
vectorizer_path = os.path.join(output_dir, "vectorizer.joblib")

print(f"Saving artifacts to {output_dir}...")
joblib.dump(rf, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("Done. Model is ready.")
