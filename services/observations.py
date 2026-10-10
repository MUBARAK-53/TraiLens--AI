from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Observation
from schema import CreateObservation, UpdateObservation


async def create_observation(
    db: AsyncSession, 
    observation: CreateObservation, 
    image_url: str
):
    new_observation = Observation(
        user_id=observation.user_id,
        image_url=image_url,
        latitude=observation.latitude,
        longitude=observation.longitude,
        observation_name=observation.observation_name,
        description=observation.description,
        interesting_fact=observation.interesting_fact,
        confidence=observation.confidence,
        suggested_activity=observation.suggested_activity,
        safety_note=observation.safety_note,
    )

    db.add(new_observation)
    await db.commit()
    await db.refresh(new_observation)

    return new_observation


async def get_observations(db: AsyncSession):
    result = await db.execute(
        select(Observation).order_by(Observation.created_at.desc())
    )
    # Returns an empty list [] gracefully instead of breaking the Android app with a 404 error
    return result.scalars().all()


async def get_observation_by_id(db: AsyncSession, observation_id: int):
    result = await db.execute(
        select(Observation).where(Observation.id == observation_id)
    )
    existing_observation = result.scalar_one_or_none()

    if existing_observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation Not Found!",
        )

    return existing_observation


async def update_observation(
    db: AsyncSession, 
    observation_id: int, 
    observation: UpdateObservation
):
    result = await db.execute(
        select(Observation).where(Observation.id == observation_id)
    )
    existing_observation = result.scalar_one_or_none()

    if existing_observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation Not Found!",
        )

    update_data = observation.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_observation, key, value)

    await db.commit()
    await db.refresh(existing_observation)

    return existing_observation


async def delete_observation(db: AsyncSession, observation_id: int):
    result = await db.execute(
        select(Observation).where(Observation.id == observation_id)
    )
    existing_observation = result.scalar_one_or_none()

    if existing_observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation Not Found!",
        )

    await db.delete(existing_observation)
    await db.commit()

    return {"message": "Observation deleted successfully"}