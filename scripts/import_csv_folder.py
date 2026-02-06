import pandas as pd
import os
import glob

def import_csv_folder():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_folder = os.path.join(base_dir, "data", "csv_source")
    output_path = os.path.join(base_dir, "data", "merged_real_data.csv")
    
    all_files = glob.glob(os.path.join(csv_folder, "*.csv"))
    print(f"Found {len(all_files)} CSV files in {csv_folder}")
    
    li = []
    
    for filename in all_files:
        try:
            # Read CSV, handling potential encoding errors or bad lines
            df = pd.read_csv(filename, on_bad_lines='skip', encoding='utf-8')
            
            # Ensure required columns exist (case insensitive check could be better, but sticking to standard)
            # The sample showed: issuekey,created,title,description,storypoints
            if 'title' in df.columns and 'description' in df.columns and 'storypoints' in df.columns:
                
                # Filter rows where storypoints is valid (numeric and > 0)
                # Convert to numeric, errors='coerce' turns non-numeric to NaN
                df['points'] = pd.to_numeric(df['storypoints'], errors='coerce')
                df = df.dropna(subset=['points'])
                df = df[df['points'] > 0]
                
                # Combine title and description
                df['story'] = df['title'].fillna('') + ". " + df['description'].fillna('')
                
                # Keep only what we need
                valid_df = df[['story', 'points']].copy()
                li.append(valid_df)
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    if li:
        final_df = pd.concat(li, axis=0, ignore_index=True)
        print(f"Total merged records: {len(final_df)}")
        
        # Shuffle
        final_df = final_df.sample(frac=1).reset_index(drop=True)
        
        # Save
        final_df.to_csv(output_path, index=False)
        print(f"Saved merged dataset to {output_path}")
    else:
        print("No valid data found to merge.")

if __name__ == "__main__":
    import_csv_folder()
