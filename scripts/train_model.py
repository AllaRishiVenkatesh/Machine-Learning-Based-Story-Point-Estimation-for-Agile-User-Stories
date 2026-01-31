import os
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

# 1. Dummy Data Generation
# In a real scenario, load from CSV
data = [
    ("As a user, I want to log in so that I can access my account", 2),
    ("As a user, I want to reset my password via email", 3),
    ("As an admin, I want to view a dashboard of all users", 5),
    ("As a user, I want to upload a profile picture", 3),
    ("As a user, I want to integrate with a third-party API for payments", 8),
    ("As an admin, I want to generate a downloadable PDF report of monthly sales", 8),
    ("As a user, I want to have a persistent shopping cart", 5),
    ("As a user, I want to change the color theme of the app", 2),
    ("As a user, I want multi-factor authentication", 5),
    ("As a developer, I want to migrate the database to a new schema without downtime", 13),
    ("As a user, I want to search for items by keyword", 3),
    ("As a user, I want to filter search results by price range", 3),
    ("As a user, I want to see a history of my orders", 5),
    ("As a user, I want to get push notifications for new messages", 5),
    ("As a user, I want to delete my account permanently", 3),
]

df = pd.DataFrame(data, columns=["story", "points"])

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
