from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# Base schemas
class SceneBase(BaseModel):
    start_time: float
    end_time: float
    duration: float
    importance_score: float = 0.0
    visual_intensity: float = 0.0
    audio_intensity: float = 0.0
    dialogue_density: float = 0.0
    description: Optional[str] = None


class KeyframeBase(BaseModel):
    timestamp: float
    image_path: str


class ScreenshotBase(BaseModel):
    timestamp: float
    image_path: str
    description: Optional[str] = None


class ClipBase(BaseModel):
    start_time: float
    end_time: float
    duration: float
    title: Optional[str] = None
    description: Optional[str] = None
    output_path: Optional[str] = None


class VideoBase(BaseModel):
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    codec: Optional[str] = None


# Response schemas
class KeyframeResponse(KeyframeBase):
    id: int
    scene_id: int

    model_config = ConfigDict(from_attributes=True)


class SceneResponse(SceneBase):
    id: int
    video_id: int
    keyframes: List[KeyframeResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ScreenshotResponse(ScreenshotBase):
    id: int
    video_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClipResponse(ClipBase):
    id: int
    video_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VideoResponse(VideoBase):
    id: int
    status: str
    processing_progress: float
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    scenes: List[SceneResponse] = []
    screenshots: List[ScreenshotResponse] = []
    clips: List[ClipResponse] = []

    model_config = ConfigDict(from_attributes=True)


class VideoListResponse(BaseModel):
    id: int
    filename: str
    file_size: int
    duration: Optional[float] = None
    status: str
    processing_progress: float
    uploaded_at: datetime
    width: Optional[int] = None
    height: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
