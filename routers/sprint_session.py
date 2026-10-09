from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependency import get_db
from schema import CreateSprintSession, UpdateSprintSession, SprintSessionResponse
from services.sprint_session import (
    create_sprint_session,
    get_sprint_session_by_id,
    update_sprint_session,
    delete_sprint_session,
)

router = APIRouter(prefix="/sprint-sessions", tags=["Sprint Sessions"])


@router.post("/", response_model=SprintSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(sprint: CreateSprintSession, db: AsyncSession = Depends(get_db)):
    return await create_sprint_session(db=db, sprint=sprint)


@router.get("/{session_id}", response_model=SprintSessionResponse)
async def fetch_session_by_id(session_id: int, db: AsyncSession = Depends(get_db)):
    return await get_sprint_session_by_id(db=db, session_id=session_id)


@router.put("/{session_id}", response_model=SprintSessionResponse)
async def edit_session(
    session_id: int, 
    sprint: UpdateSprintSession, 
    db: AsyncSession = Depends(get_db)
):
    return await update_sprint_session(db=db, session_id=session_id, sprint=sprint)


@router.delete("/{session_id}")
async def remove_session(session_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_sprint_session(db=db, session_id=session_id)