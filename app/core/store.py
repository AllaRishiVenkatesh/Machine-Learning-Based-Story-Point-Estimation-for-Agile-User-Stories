import csv
import os
import uuid
from datetime import datetime
from threading import Lock
from typing import List, Dict, Any

class DataStore:
    _instance = None
    _lock = Lock()
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.history_file = os.path.join(self.data_dir, "history.csv")
        self.feedback_file = os.path.join(self.data_dir, "feedback.csv")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize files with headers if they don't exist
        self._init_file(self.history_file, ["id", "timestamp", "user_story", "predicted_points", "confidence", "model"])
        self._init_file(self.feedback_file, ["id", "timestamp", "prediction_id", "user_story", "actual_points"])

    def _init_file(self, filepath, headers):
        if not os.path.exists(filepath):
            with open(filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def log_prediction(self, user_story: str, prediction: int, confidence: str, model: str) -> str:
        """
        Logs a prediction to history and returns the generated ID.
        """
        pred_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        with self._lock:
            with open(self.history_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([pred_id, timestamp, user_story, prediction, confidence, model])
                
        return pred_id

    def log_feedback(self, prediction_id: str, user_story: str, actual_points: int):
        """
        Logs user feedback for model retraining.
        """
        timestamp = datetime.now().isoformat()
        idea_id = str(uuid.uuid4())
        
        with self._lock:
            with open(self.feedback_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([idea_id, timestamp, prediction_id, user_story, actual_points])

    def get_recent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns the last N history items.
        """
        history = []
        if not os.path.exists(self.history_file):
            return history
            
        try:
            with open(self.history_file, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Read all and take last N (not efficient for huge files, but fine here)
                rows = list(reader)
                history = rows[-limit:]
                history.reverse() # Newest first
        except Exception as e:
            print(f"Error reading history: {e}")
            
        return history

    def clear_history(self):
        """
        Clears all prediction history.
        """
        with self._lock:
            # Re-initialize the file (overwrites it with just headers)
            self._init_file(self.history_file, ["id", "timestamp", "user_story", "predicted_points", "confidence", "model"])
            # Force overwrite since _init_file only writes if not exists, but here we want to truncate
            with open(self.history_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "timestamp", "user_story", "predicted_points", "confidence", "model"])
