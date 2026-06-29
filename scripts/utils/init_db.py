import sqlite3
import os
import csv
import sys

# Increase CSV field limit size safely for large descriptions
max_limit = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_limit)
        break
    except OverflowError:
        max_limit = int(max_limit / 2)

def init_db():
    # Define database path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, "data", "processed", "agile_data.db")
    csv_path = os.path.join(base_dir, "data", "processed", "merged_real_data.csv")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    print(f"Initializing database at {db_path}...")
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop table if it exists to ensure a clean state when re-seeding/initializing
    cursor.execute("DROP TABLE IF EXISTS historical_stories")
    
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_text TEXT NOT NULL,
        actual_points INTEGER NOT NULL
    )
    """)
    
    # Check if real dataset exists
    if os.path.exists(csv_path):
        print(f"Loading real dataset from {csv_path}...")
        try:
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                db_data = []
                for row in reader:
                    story = row.get('story', '')
                    points_raw = row.get('points', '')
                    if story and points_raw:
                        try:
                            points = int(float(points_raw))
                            db_data.append((story, points))
                        except ValueError:
                            continue
                
                if db_data:
                    print(f"Inserting {len(db_data)} stories into the database...")
                    cursor.executemany("INSERT INTO historical_stories (story_text, actual_points) VALUES (?, ?)", db_data)
                    conn.commit()
                    print(f"Successfully loaded database with {len(db_data)} real records.")
                else:
                    print("No valid records found in CSV file.")
        except Exception as e:
            print(f"Error loading CSV into database: {e}")
            conn.rollback()
    else:
        # Initial seed data fallback
        print("Merged real data CSV not found. Populating database with fallback seed data...")
        seed_data = [
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
        cursor.executemany("INSERT INTO historical_stories (story_text, actual_points) VALUES (?, ?)", seed_data)
        conn.commit()
        print(f"Successfully populated database with {len(seed_data)} fallback seed records.")
        
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()

