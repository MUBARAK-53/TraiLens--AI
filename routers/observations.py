from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from dependency import get_db
from schema import (
    CreateObservation, 
    UpdateObservation, 
    ObservationResponse, 
    CreateSprintSession, 
    CreateSprintMission
)
from services.gemma import analyze_image
from services.observations import (
    create_observation,
    get_observations,
    get_observation_by_id,
    update_observation,
    delete_observation,
)
from services.sprint_session import create_sprint_session
from services.sprint_mission import create_sprint_mission

router = APIRouter(prefix="/observations", tags=["Observations"])


@router.post("/", response_model=ObservationResponse, status_code=status.HTTP_201_CREATED)
async def post_observation(
    user_id: Optional[int] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # 1. Read image bytes and determine mime type
    image_bytes = await image.read()
    mime_type = image.content_type or "image/jpeg"

    # 2. Call Gemma AI Vision + Weather Integration
    ai_result = await analyze_image(
        image_bytes=image_bytes, 
        mime_type=mime_type, 
        latitude=latitude, 
        longitude=longitude
    )

    mock_image_url = f"https://storage.traillens.app/images/{image.filename}"

    # 3. Extract AI Response Fields
    obs_name = ai_result.get("observation", "Outdoor Discovery")
    description = ai_result.get("description", "A fascinating element of nature.")
    interesting_fact = ai_result.get("interesting_fact", "Observe closely.")
    
    mission_info = ai_result.get("mission", {})
    mission_title = mission_info.get("title", "Nature Focus")
    mission_instruction = mission_info.get("instruction", "Spend 5 minutes looking around mindfully.")
    duration = mission_info.get("duration_minutes", 5)

    # 4. Save Observation Record
    obs_data = CreateObservation(
        observation_name=obs_name,
        description=description,
        interesting_fact=interesting_fact,
        confidence="high",
        suggested_activity=mission_instruction,
        safety_note="Stay on marked paths.",
        user_id=user_id,
        latitude=latitude,
        longitude=longitude,
    )
    new_observation = await create_observation(db=db, observation=obs_data, image_url=mock_image_url)

    # 5. Automatically Create the 5-Minute Sprint Session with Soundscape
    expires_at = datetime.utcnow() + timedelta(minutes=duration)
    session_payload = CreateSprintSession(
        observation_id=new_observation.id,
        duration_minutes=duration,
        expires_at=expires_at,
        soundscape="Forest Breeze"
    )
    new_session = await create_sprint_session(db=db, sprint=session_payload)

    # 6. Automatically Create the Thrilling Sprint Mission
    mission_payload = CreateSprintMission(
        session_id=new_session.id,
        title=mission_title,
        instruction=mission_instruction
    )
    await create_sprint_mission(db=db, mission=mission_payload)

    # Refresh observation to load relations if configured
    return await get_observation_by_id(db=db, observation_id=new_observation.id)


@router.get("/", response_model=List[ObservationResponse])
async def fetch_all_observations(db: AsyncSession = Depends(get_db)):
    return await get_observations(db=db)


@router.get("/{observation_id}", response_model=ObservationResponse)
async def fetch_observation_by_id(observation_id: int, db: AsyncSession = Depends(get_db)):
    return await get_observation_by_id(db=db, observation_id=observation_id)


@router.put("/{observation_id}", response_model=ObservationResponse)
async def edit_observation(
    observation_id: int, 
    observation: UpdateObservation, 
    db: AsyncSession = Depends(get_db)
):
    return await update_observation(db=db, observation_id=observation_id, observation=observation)


@router.delete("/{observation_id}")
async def remove_observation(observation_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_observation(db=db, observation_id=observation_id)