# backend/backend_app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChromaStudentMetadata(BaseModel):
    user_id: str  # UUID from Supabase
    full_name: Optional[str]
    university: Optional[str]
    major: Optional[str]
    current_location: Optional[str]
    country: Optional[str]
    company_stage: Optional[str]
    skills: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    most_impressive_fact: Optional[str]      
    is_verified: Optional[bool] = False
    call_type: Optional[str] = "onboarding"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserProfile(BaseModel):
    user_id: str
    full_name: Optional[str]
    university: Optional[str]
    major: Optional[str]
    location: Optional[str]
    stage: Optional[str]
    bio: Optional[str]
    most_impressive_fact: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    website: Optional[str]
    twitter: Optional[str]
    devpost: Optional[str]
    skills: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    is_verified: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserPreference(BaseModel):
    user_id: str
    intro_call: Optional[bool] = False
    is_verified: Optional[bool] = False
    phone: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserTrial(BaseModel):
    user_id: str
    trial_start_time: Optional[datetime]
    trial_end_time: datetime
    is_trial_used: Optional[bool] = False

class Subscription(BaseModel):
    user_id: str
    stripe_customer_id: Optional[str]
    stripe_subscription_id: Optional[str]
    status: Optional[str]
    price_id: Optional[str]
    cancel_at_period_end: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    current_period_end: Optional[datetime] = None