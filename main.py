from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import engine, Base
from routers.user import router as user_router
from routers.observations import router as observation_router
from routers.sprint_session import router as sprint_session_router
from routers.sprint_mission import router as sprint_mission_router
from routers.ai import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creates tables asynchronously on app startup if they don't exist yet
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Application runs while sitting here
    
    # Close database connections or engine pools on shutdown
    await engine.dispose()


app = FastAPI(
    title="TrailLens API",
    version="1.0.0",
    description="Backend API powering TrailLens 5-minute gamified outdoor exploration",
    lifespan=lifespan,
)

# Register Routers
app.include_router(user_router)
app.include_router(observation_router)
app.include_router(sprint_session_router)
app.include_router(sprint_mission_router)
app.include_router(ai_router)


@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "online", "message": "TrailLens API is running smoothly!"}