from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String, unique=True)
    file_size = Column(Integer)
    duration = Column(Float, nullable=True)
    mime_type = Column(String)

    # Processing status
    status = Column(String, default="uploaded")  # uploaded, processing, completed, error
    processing_progress = Column(Float, default=0.0)

    # Metadata
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    fps = Column(Float, nullable=True)
    codec = Column(String, nullable=True)

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    # Relationships
    scenes = relationship("Scene", back_populates="video", cascade="all, delete-orphan")
    screenshots = relationship("Screenshot", back_populates="video", cascade="all, delete-orphan")
    clips = relationship("Clip", back_populates="video", cascade="all, delete-orphan")


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))

    start_time = Column(Float)
    end_time = Column(Float)
    duration = Column(Float)

    # Importance metrics
    importance_score = Column(Float, default=0.0)
    visual_intensity = Column(Float, default=0.0)
    audio_intensity = Column(Float, default=0.0)
    dialogue_density = Column(Float, default=0.0)

    # Description
    description = Column(Text, nullable=True)

    video = relationship("Video", back_populates="scenes")
    keyframes = relationship("Keyframe", back_populates="scene", cascade="all, delete-orphan")


class Keyframe(Base):
    __tablename__ = "keyframes"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"))

    timestamp = Column(Float)
    image_path = Column(String)

    scene = relationship("Scene", back_populates="keyframes")


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))

    timestamp = Column(Float)
    image_path = Column(String)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="screenshots")


class Clip(Base):
    __tablename__ = "clips"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))

    start_time = Column(Float)
    end_time = Column(Float)
    duration = Column(Float)

    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    output_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="clips")
