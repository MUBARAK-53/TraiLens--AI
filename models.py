import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    observations = relationship("Observation", back_populates="user", cascade="all, delete-orphan")


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    image_url = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    observation_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    interesting_fact = Column(Text, nullable=False)
    confidence = Column(String(50), nullable=False, default="moderate")
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="observations")
    sprint_session = relationship(
        "SprintSession", 
        back_populates="observation", 
        uselist=False, 
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_observations_created_at", created_at.desc()),
    )


class SprintSession(Base):
    __tablename__ = "sprint_sessions"

    id = Column(Integer, primary_key=True, index=True)
    observation_id = Column(
        Integer, 
        ForeignKey("observations.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    duration_minutes = Column(Integer, default=5, nullable=False)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False, index=True)
    status = Column(String(50), default="active", nullable=False) # "active", "completed", "expired"

    # Relationships
    observation = relationship("Observation", back_populates="sprint_session")
    missions = relationship("SprintMission", back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_sprint_sessions_expiry_status", expires_at, status),
    )


class SprintMission(Base):
    __tablename__ = "sprint_missions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer, 
        ForeignKey("sprint_sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    title = Column(String(150), nullable=False)
    instruction = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)

    # Relationships
    session = relationship("SprintSession", back_populates="missions")