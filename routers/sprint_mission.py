from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependency import get_db
from schema import CreateSprintMission, UpdateSprintMission, SprintMissionResponse
from services.sprint_mission import (
    create_sprint_mission,
    get_missions_by_session_id,
    update_mission_status,
    delete_sprint_mission,
)

router = APIRouter(prefix="/sprint-missions", tags=["Sprint Missions"])


@router.post("/", response_model=SprintMissionResponse, status_code=status.HTTP_201_CREATED)
async def add_mission(mission: CreateSprintMission, db: AsyncSession = Depends(get_db)):
    return await create_sprint_mission(db=db, mission=mission)


@router.get("/session/{session_id}", response_model=List[SprintMissionResponse])
async def fetch_missions_for_session(session_id: int, db: AsyncSession = Depends(get_db)):
    return await get_missions_by_session_id(db=db, session_id=session_id)


@router.put("/{mission_id}", response_model=SprintMissionResponse)
async def edit_mission_status(
    mission_id: int, 
    mission: UpdateSprintMission, 
    db: AsyncSession = Depends(get_db)
):
    return await update_mission_status(db=db, mission_id=mission_id, mission=mission)


@router.delete("/{mission_id}")
async def remove_mission(mission_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_sprint_mission(db=db, mission_id=mission_id)