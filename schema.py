from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime


# ==========================================
# 1. USER SCHEMAS
# ==========================================

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str


class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 2. SPRINT MISSION SCHEMAS
# ==========================================

class CreateSprintMission(BaseModel):
    session_id: int
    title: str
    instruction: str


class UpdateSprintMission(BaseModel):
    title: Optional[str] = None
    instruction: Optional[str] = None
    is_completed: Optional[bool] = None


class SprintMissionResponse(BaseModel):
    id: int
    title: str
    instruction: str
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 3. SPRINT SESSION SCHEMAS
# ==========================================

class CreateSprintSession(BaseModel):
    observation_id: int
    duration_minutes: int = Field(default=5, ge=1, le=60)
    expires_at: datetime


class UpdateSprintSession(BaseModel):
    duration_minutes: Optional[int] = None
    expires_at: Optional[datetime] = None
    status: Optional[Literal["active", "completed", "expired"]] = None


class StartSprintRequest(BaseModel):
    observation_id: int
    duration_minutes: int = Field(default=5, ge=1, le=60)


class SprintSessionResponse(BaseModel):
    id: int
    observation_id: int
    duration_minutes: int
    start_time: datetime
    expires_at: datetime
    status: Literal["active", "completed", "expired"]
    instructions: Optional[str] = None
    missions: List[SprintMissionResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 4. OBSERVATION / DISCOVERY SCHEMAS
# ==========================================

class CreateObservation(BaseModel):
    observation_name: str
    description: str
    interesting_fact: str
    confidence: Literal["high", "moderate", "low"] = "low"
    suggested_activity: Optional[str] = None
    safety_note: Optional[str] = None
    user_id: Optional[int] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)


class UpdateObservation(BaseModel):
    observation_name: Optional[str] = None
    description: Optional[str] = None
    interesting_fact: Optional[str] = None
    confidence: Optional[Literal["high", "moderate", "low"]] = None
    suggested_activity: Optional[str] = None
    safety_note: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ObservationResponse(BaseModel):
    id: int
    observation_name: str
    description: str
    interesting_fact: str
    confidence: Literal["high", "moderate", "low"]
    suggested_activity: Optional[str] = None
    safety_note: Optional[str] = None
    user_id: Optional[int] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    sprint_session: Optional[SprintSessionResponse] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 5. GEMMA AI SERVICE SCHEMA
# ==========================================

class GemmaVisionOutput(BaseModel):
    observation: str
    confidence: Literal["high", "moderate", "low"]
    description: str
    interesting_fact: str
    suggested_activity: str
    safety_note: str