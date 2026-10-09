from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import SprintMission
from schema import CreateSprintMission, UpdateSprintMission


async def create_sprint_mission(db: AsyncSession, mission: CreateSprintMission):
    new_mission = SprintMission(
        session_id=mission.session_id,
        title=mission.title,
        instruction=mission.instruction,
        is_completed=False,
    )

    db.add(new_mission)
    await db.commit()
    await db.refresh(new_mission)

    return new_mission


async def get_missions_by_session_id(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(SprintMission).where(SprintMission.session_id == session_id)
    )
    existing_missions = result.scalars().all()

    if not existing_missions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Sprint Missions Found for this Session!",
        )

    return existing_missions


async def update_mission_status(
    db: AsyncSession, 
    mission_id: int, 
    mission: UpdateSprintMission
):
    result = await db.execute(
        select(SprintMission).where(SprintMission.id == mission_id)
    )
    existing_mission = result.scalar_one_or_none()

    if existing_mission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint Mission Not Found!",
        )

    update_data = mission.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_mission, key, value)

    await db.commit()
    await db.refresh(existing_mission)

    return existing_mission


async def delete_sprint_mission(db: AsyncSession, mission_id: int):
    result = await db.execute(
        select(SprintMission).where(SprintMission.id == mission_id)
    )
    existing_mission = result.scalar_one_or_none()

    if existing_mission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint Mission Not Found!",
        )

    await db.delete(existing_mission)
    await db.commit()

    return {"message": "Sprint Mission deleted successfully"}