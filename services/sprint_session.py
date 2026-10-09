from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import SprintSession
from schema import CreateSprintSession, UpdateSprintSession


async def create_sprint_session(
    db: AsyncSession, 
    sprint: CreateSprintSession
):
    result = await db.execute(
        select(SprintSession).where(
            SprintSession.observation_id == sprint.observation_id
        )
    )
    existing_session = result.scalar_one_or_none()

    if existing_session is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sprint Session already exists for this observation!",
        )

    new_sprint = SprintSession(
        observation_id=sprint.observation_id,
        duration_minutes=sprint.duration_minutes,
        expires_at=sprint.expires_at,
        status="active",
    )

    db.add(new_sprint)
    await db.commit()
    await db.refresh(new_sprint)

    return new_sprint


async def get_sprint_session_by_id(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(SprintSession).where(SprintSession.id == session_id)
    )
    existing_session = result.scalar_one_or_none()

    if existing_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint Session Not Found!",
        )

    return existing_session


async def update_sprint_session(
    db: AsyncSession, 
    session_id: int, 
    sprint: UpdateSprintSession
):
    result = await db.execute(
        select(SprintSession).where(SprintSession.id == session_id)
    )
    existing_session = result.scalar_one_or_none()

    if existing_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint Session Not Found!",
        )

    update_data = sprint.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_session, key, value)

    await db.commit()
    await db.refresh(existing_session)

    return existing_session


async def delete_sprint_session(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(SprintSession).where(SprintSession.id == session_id)
    )
    existing_session = result.scalar_one_or_none()

    if existing_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint Session Not Found!",
        )

    await db.delete(existing_session)
    await db.commit()

    return {"message": "Sprint Session deleted successfully"}