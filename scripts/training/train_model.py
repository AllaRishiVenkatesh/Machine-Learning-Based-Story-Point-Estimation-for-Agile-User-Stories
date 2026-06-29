import os
import sqlite3
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Use absolute imports or run as module, but for a script, simple relative path handling is needed
# if running from root.
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.preprocessing import clean_text

# 1. Load Data
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path = os.path.join(base_dir, "data", "processed", "agile_data.db")

if os.path.exists(db_path):
    print(f"Loading training data from database: {db_path}")
    conn = sqlite3.connect(db_path)
    try:
        # Load from historical_stories and alias columns to 'story' and 'points' for the pipeline
        df = pd.read_sql_query("SELECT story_text AS story, actual_points AS points FROM historical_stories", conn)
    finally:
        conn.close()
        
    if df.empty:
        raise ValueError("No records found in database. Run scripts/utils/init_db.py first.")
    
    # Only keep standard fibonacci points to reduce noise
    valid_points = [1, 2, 3, 5, 8, 13, 21] 
    df = df[df['points'].isin(valid_points)]
    
    # Sort index to guarantee deterministic split
    df = df.sort_index()
    
    # Split dataset before balancing to avoid data leakage
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    print(f"Dataset split: Train set size = {len(df_train)}, Test set size = {len(df_test)}")
    
    # --- BALANCING LOGIC START ---
    # The real world data is heavily skewed to 1s and 2s.
    # We must balance it so the model learns to predict 8s and 13s.
    print("Balancing dataset distribution (train split only)...")
    
    # Sample N items from each class to flatten the distribution
    # If a class has fewer than N, take them all.
    TARGET_PER_CLASS = 1500 
    
    balanced_dfs = []
    for point_val in valid_points:
        subset = df_train[df_train['points'] == point_val]
        if len(subset) > 0:
            if len(subset) > TARGET_PER_CLASS:
                # Undersample majority
                subset = subset.sample(n=TARGET_PER_CLASS, random_state=42)
            else:
                # Oversample minority (with replacement)
                subset = subset.sample(n=TARGET_PER_CLASS, replace=True, random_state=42)
            balanced_dfs.append(subset)
    
    if balanced_dfs:
        df_train_balanced = pd.concat(balanced_dfs)
        df_train_balanced = df_train_balanced.sample(frac=1, random_state=42).reset_index(drop=True)
        print("Balanced train distribution:")
        print(df_train_balanced['points'].value_counts().sort_index())
        df = df_train_balanced
    # --- BALANCING LOGIC END ---

    # Ensure columns match expectations
    if "story" not in df.columns or "points" not in df.columns:
        print("Warning: Columns 'story' or 'points' missing. Checking headers...")
        print(df.columns)
else:
    raise FileNotFoundError(f"Database file not found at {db_path}. Run scripts/utils/init_db.py first.")

print("Training data sample:")
print(df.head())

# 2. Preprocessing
print("Preprocessing...")
df['clean_text'] = df['story'].apply(clean_text)

# 3. Vectorization
print("Vectorizing with Stop Words removal...")
# Using TF-IDF with English Stop Words filtering
vectorizer = TfidfVectorizer(max_features=4000, stop_words='english')
X = vectorizer.fit_transform(df['clean_text'])
y = df['points']

# 4. Model Training
print("Training RandomForest...")
rf = RandomForestRegressor(n_estimators=20, max_depth=20, random_state=42)
rf.fit(X, y)

# 5. Saving Artifacts
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml_artifacts")
os.makedirs(output_dir, exist_ok=True)

model_path = os.path.join(output_dir, "model.joblib")
vectorizer_path = os.path.join(output_dir, "vectorizer.joblib")

print(f"Saving artifacts to {output_dir}...")
joblib.dump(rf, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("Done. Model is ready.")
