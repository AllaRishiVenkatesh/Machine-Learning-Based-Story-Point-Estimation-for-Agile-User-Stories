import sqlite3
import os

def init_db():
    # Define database path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "agile_data.db")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    print(f"Initializing database at {db_path}...")
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_text TEXT NOT NULL,
        actual_points INTEGER NOT NULL
    )
    """)
    
    # Initial seed data (The same data we used before)
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
    
    # Check if empty to avoid duplicates
    cursor.execute("SELECT count(*) FROM historical_stories")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Populating database with seed data...")
        cursor.executemany("INSERT INTO historical_stories (story_text, actual_points) VALUES (?, ?)", seed_data)
        conn.commit()
    else:
        print("Database already contains data, skipping seed.")
        
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
