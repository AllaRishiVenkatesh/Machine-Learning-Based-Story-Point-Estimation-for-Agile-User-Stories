import pandas as pd
import os

def check_distribution():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "merged_real_data.csv")
    
    df = pd.read_csv(csv_path)
    
    print("--- Story Point Distribution ---")
    counts = df['points'].value_counts()
    percentages = df['points'].value_counts(normalize=True) * 100
    
    result = pd.concat([counts, percentages], axis=1, keys=['Count', 'Percent'])
    print(result.sort_index())

if __name__ == "__main__":
    check_distribution()
