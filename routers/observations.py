from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from dependency import get_db
from schema import CreateObservation, UpdateObservation, ObservationResponse
from services.observations import (
    create_observation,
    get_observations,
    get_observation_by_id,
    update_observation,
    delete_observation,
)

router = APIRouter(prefix="/observations", tags=["Observations"])


@router.post("/", response_model=ObservationResponse, status_code=status.HTTP_201_CREATED)
async def post_observation(
    observation_name: str = Form(...),
    description: str = Form(...),
    interesting_fact: str = Form(...),
    confidence: str = Form("low"),
    suggested_activity: Optional[str] = Form(None),
    safety_note: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # Place file storage or cloud upload logic here to get the actual URL
    mock_image_url = f"https://storage.traillens.app/images/{image.filename}"

    obs_data = CreateObservation(
        observation_name=observation_name,
        description=description,
        interesting_fact=interesting_fact,
        confidence=confidence,
        suggested_activity=suggested_activity,
        safety_note=safety_note,
        user_id=user_id,
        latitude=latitude,
        longitude=longitude,
    )

    return await create_observation(db=db, observation=obs_data, image_url=mock_image_url)


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