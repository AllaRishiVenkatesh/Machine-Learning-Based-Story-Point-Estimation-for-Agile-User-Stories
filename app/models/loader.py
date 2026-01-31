import os
import joblib
import logging
from typing import Any
from threading import Lock

logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    _lock = Lock()
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self._is_loaded = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def load_model(self, model_path: str, vectorizer_path: str):
        """
        Loads the model and vectorizer from disk.
        """
        if self._is_loaded:
            logger.info("Model already loaded.")
            return

        logger.info(f"Loading model from {model_path} and vectorizer from {vectorizer_path}...")
        
        try:
            if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
                raise FileNotFoundError(f"Artifacts not found at {model_path} or {vectorizer_path}")

            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self._is_loaded = True
            logger.info("Model and vectorizer loaded successfully.")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise e

    def predict(self, text: str) -> float:
        """
        Raw prediction from the model.
        """
        if not self._is_loaded:
            raise RuntimeError("Model is not loaded. Call load_model first.")
        
        # Transform input
        vectors = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.model.predict(vectors)
        return float(prediction[0])
    
    @property
    def algorithm_name(self) -> str:
        if self.model:
            return type(self.model).__name__
        return "Unknown"
