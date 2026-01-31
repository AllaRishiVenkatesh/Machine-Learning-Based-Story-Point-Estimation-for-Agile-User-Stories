from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.api_models import FeedbackRequest, HistoryItem
from app.core.store import DataStore
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Accepts user corrections for model retraining.
    """
    try:
        store = DataStore.get_instance()
        store.log_feedback(
            prediction_id=request.prediction_id,
            user_story=request.user_story,
            actual_points=request.actual_points
        )
        logger.info(f"Feedback received for {request.prediction_id}")
        return {"status": "success", "message": "Feedback recorded."}
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to save feedback")

@router.get("/history", response_model=List[HistoryItem])
async def get_history():
    """
    Get recent prediction history.
    """
    try:
        store = DataStore.get_instance()
        data = store.get_recent_history(limit=10)
        return data
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return []

@router.delete("/history")
async def clear_history():
    """
    Clears the prediction history.
    """
    try:
        store = DataStore.get_instance()
        store.clear_history()
        return {"status": "success", "message": "History cleared."}
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear history")
