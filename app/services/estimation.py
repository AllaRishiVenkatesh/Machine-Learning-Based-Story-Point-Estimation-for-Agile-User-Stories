import numpy as np
from app.models.loader import ModelLoader
from app.utils.preprocessing import preprocess_story

AGILE_POINTS = [1, 2, 3, 5, 8, 13]

class EstimationService:
    def __init__(self):
        self.loader = ModelLoader.get_instance()

    def _find_nearest_point(self, value: float) -> int:
        """
        Maps a continuous prediction to the nearest valid Story Point.
        """
        # Ensure value is at least the smallest valid point
        if value < AGILE_POINTS[0]:
            return AGILE_POINTS[0]
        
        # Determine nearest valid point
        idx = (np.abs(np.array(AGILE_POINTS) - value)).argmin()
        return AGILE_POINTS[idx]

    def _calculate_confidence(self, raw_pred: float, mapped_point: int) -> str:
        """
        Heuristic confidence based on distance to the valid point.
        Closer distance = High confidence.
        """
        distance = abs(raw_pred - mapped_point)
        if distance < 0.2:
            return "high"
        elif distance < 0.5:
            return "medium"
        else:
            return "low"

    def estimate_story_points(self, raw_story_text: str):
        """
        End-to-end estimation pipeline.
        """
        # 1. Preprocess
        cleaned_text = preprocess_story(raw_story_text)
        
        # 2. Get Raw Prediction
        raw_pred = self.loader.predict(cleaned_text)
        
        # 3. Map to Agile Scale
        final_points = self._find_nearest_point(raw_pred)
        
        # 4. Calculate Meta-data
        confidence = self._calculate_confidence(raw_pred, final_points)
        model_name = self.loader.algorithm_name
        
        return {
            "predicted_story_points": final_points,
            "raw_prediction": round(raw_pred, 2),
            "model_used": model_name,
            "confidence": confidence
        }
