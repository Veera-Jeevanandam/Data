from pydantic import BaseModel
from typing import List, Optional

class UserBiomarkers(BaseModel):
    age: int
    gender: str
    bmi: float
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    cholesterol_total: int
    hba1c: float
    glucose_fasting: int
    triglycerides: int
    cholesterol_hdl: int
    cholesterol_ldl: int
    weight: float
    activity_level: str  # Sedentary, Light, Moderate, Active
    sleep_hours: float

class RecommendationResponse(BaseModel):
    risk_level: str  # Low, Moderate, High
    risk_score: int
    risk_summary: str
    fitness_recommendations: str
    diet_recommendations: str
    lifestyle_recommendations: str
    biomarker_analysis: List[dict] = []
    disclaimer: str = "This is AI-generated advice. Please consult a doctor."

class UserFeedback(BaseModel):
    rating: int  # 1-5
    is_helpful: bool
    comments: Optional[str] = None
    timestamp: Optional[str] = None
