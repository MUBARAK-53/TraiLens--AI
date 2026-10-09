from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schema import CreateUser, UpdateUser


async def create_user(db: AsyncSession, user: CreateUser):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!",
        )

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    existing_users = result.scalars().all()

    if not existing_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Users Found!",
        )

    return existing_users


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!",
        )

    return existing_user


async def update_user(db: AsyncSession, user_id: int, user: UpdateUser):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!",
        )

    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_user, key, value)

    await db.commit()
    await db.refresh(existing_user)

    return existing_user


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!",
        )

    await db.delete(existing_user)
    await db.commit()

    return {"message": "User deleted successfully"}