from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependency import get_db
from schema import CreateUser, UpdateUser, UserResponse
from services.user import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: CreateUser, db: AsyncSession = Depends(get_db)):
    return await create_user(db=db, user=user)


@router.get("/", response_model=List[UserResponse])
async def fetch_all_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db=db)


@router.get("/{user_id}", response_model=UserResponse)
async def fetch_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db=db, user_id=user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def edit_user(user_id: int, user: UpdateUser, db: AsyncSession = Depends(get_db)):
    return await update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}")
async def remove_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_user(db=db, user_id=user_id)