import os

class Settings:
    PROJECT_NAME: str = "Story Point Estimator"
    VERSION: str = "1.0.0"
    
    # Paths to artifacts
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODEL_PATH: str = os.path.join(BASE_DIR, "ml_artifacts", "model.joblib")
    VECTORIZER_PATH: str = os.path.join(BASE_DIR, "ml_artifacts", "vectorizer.joblib")
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
