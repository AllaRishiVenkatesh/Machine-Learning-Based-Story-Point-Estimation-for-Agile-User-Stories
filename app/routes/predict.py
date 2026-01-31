from fastapi import APIRouter, HTTPException, Depends
from app.schemas.api_models import StoryRequest, PredictionResponse
from app.services.estimation import EstimationService
import logging
from app.core.store import DataStore
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency for service
def get_estimation_service():
    return EstimationService()

@router.post("/predict", response_model=PredictionResponse)
async def predict_story_points(
    request: StoryRequest, 
    service: EstimationService = Depends(get_estimation_service)
):
    """
    Predicts the story points for a given agile user story.
    Returns a Fibonacci scale value (1, 2, 3, 5, 8, 13).
    """
    # logger.info(f"Received prediction request: {request.user_story[:50]}...")
    
    try:
        result = service.estimate_story_points(request.user_story)
        
        # Log to Store
        store = DataStore.get_instance()
        pred_id = store.log_prediction(
            user_story=request.user_story,
            prediction=result["predicted_story_points"],
            confidence=result["confidence"],
            model=result["model_used"]
        )
        
        response = PredictionResponse(
            id=pred_id,
            predicted_story_points=result["predicted_story_points"],
            model_used=result["model_used"],
            confidence=result["confidence"],
            created_at=datetime.now()
        )
        
        logger.info(f"Prediction success ({pred_id}): {response.predicted_story_points} points")
        return response
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")
