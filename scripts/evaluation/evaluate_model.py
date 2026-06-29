import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Use absolute imports or run as module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.utils.preprocessing import clean_text

def evaluate_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, "data", "processed", "agile_data.db")
    model_path = os.path.join(base_dir, "ml_artifacts", "model.joblib")
    vectorizer_path = os.path.join(base_dir, "ml_artifacts", "vectorizer.joblib")
    output_dir = os.path.join(base_dir, "docs", "images")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(db_path) or not os.path.exists(model_path):
        print(f"Database ({db_path}) or model artifact ({model_path}) not found.")
        return

    print("Loading data from database...")
    conn = sqlite3.connect(db_path)
    try:
        # Load from historical_stories and alias columns to 'story' and 'points' for consistency
        df = pd.read_sql_query("SELECT story_text AS story, actual_points AS points FROM historical_stories", conn)
    finally:
        conn.close()

    if df.empty:
        print("No records found in database.")
        return
    
    # Validation logic (same as training for evaluation representation)
    valid_points = [1, 2, 3, 5, 8, 13, 21]
    df = df[df['points'].isin(valid_points)]
    
    # Sort index to guarantee deterministic split matching the training script
    df = df.sort_index()
    
    # Extract test split before evaluation to prevent data leakage
    from sklearn.model_selection import train_test_split
    _, df_test = train_test_split(df, test_size=0.2, random_state=42)
    df = df_test
    print(f"Evaluating model on unseen test split (size = {len(df)})...")
    
    print("Preprocessing...")
    df['clean_text'] = df['story'].apply(clean_text)

    print("Loading models...")
    vectorizer = joblib.load(vectorizer_path)
    model = joblib.load(model_path)

    print("Predicting...")
    X = vectorizer.transform(df['clean_text'])
    y_true = df['points']
    y_pred = model.predict(X)

    # Metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    print(f"Metrics:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.2f}")

    # Plot 1: True vs Predicted Scatter
    plt.figure(figsize=(8, 6))
    plt.scatter(y_true, y_pred, alpha=0.3)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('True Story Points')
    plt.ylabel('Predicted Story Points')
    plt.title('True vs Predicted Story Points')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'true_vs_predicted.png'))
    plt.close()

    # Plot 2: Residual Distribution
    residuals = y_true - y_pred
    plt.figure(figsize=(8, 6))
    plt.hist(residuals, bins=50, edgecolor='k', alpha=0.7)
    plt.xlabel('Residual (True - Predicted)')
    plt.ylabel('Frequency')
    plt.title('Residual Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'residual_distribution.png'))
    plt.close()

    # Plot 3: Feature Importance (Top 20)
    importances = model.feature_importances_
    feature_names = vectorizer.get_feature_names_out()
    top_indices = np.argsort(importances)[-20:]
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(20), importances[top_indices], align='center')
    plt.yticks(range(20), [feature_names[i] for i in top_indices])
    plt.xlabel('Importance')
    plt.ylabel('Feature (Keyword)')
    plt.title('Top 20 Feature Importances')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_importance.png'))
    plt.close()

    # Create a metrics report
    report_path = os.path.join(base_dir, "metrics_report.md")
    with open(report_path, "w") as f:
        f.write("# Model Evaluation Metrics\n\n")
        f.write(f"- **Mean Absolute Error (MAE)**: {mae:.2f}\n")
        f.write(f"- **Root Mean Squared Error (RMSE)**: {rmse:.2f}\n")
        f.write(f"- **R^2 Score**: {r2:.2f}\n")
    print("Done generating evaluation graphs and metrics!")

if __name__ == "__main__":
    evaluate_model()
