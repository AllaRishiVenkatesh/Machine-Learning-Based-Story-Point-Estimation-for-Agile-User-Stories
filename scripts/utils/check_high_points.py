import pandas as pd
import os

def check_high_points():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "processed", "merged_real_data.csv")
    
    df = pd.read_csv(csv_path)
    
    # Filter for high points (>= 13)
    high_points = df[df['points'] >= 13]
    
    print(f"Total stories with >= 13 points: {len(high_points)}")
    print("\n--- Example High Point Stories ---")
    
    sample = high_points.head(10)
    for index, row in sample.iterrows():
        print(f"Points: {int(row['points'])}")
        print(f"Story: {row['story'][:150]}...") # truncate for display
        print("-" * 50)

if __name__ == "__main__":
    check_high_points()
