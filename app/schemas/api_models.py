from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StoryRequest(BaseModel):
    user_story: str = Field(..., description="The user story text", min_length=5, example="As a user, I want to reset my password")

class PredictionResponse(BaseModel):
    id: str = Field(..., description="Unique ID for this inference request")
    predicted_story_points: int = Field(..., description="The estimated story points")
    model_used: str = Field(..., description="The name of the ML model used")
    confidence: str = Field(..., description="Confidence level")
    created_at: datetime = Field(..., description="Timestamp of prediction")

class FeedbackRequest(BaseModel):
    prediction_id: str = Field(..., description="The ID of the prediction being corrected")
    user_story: str = Field(..., description="Original story text")
    actual_points: int = Field(..., description="The correct story points value")
    
class HistoryItem(BaseModel):
    id: str
    user_story: str
    predicted_points: int
    confidence: str
    timestamp: str
