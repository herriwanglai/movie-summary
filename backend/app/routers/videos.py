from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.video import Video
from app.schemas.video import VideoResponse, VideoListResponse

router = APIRouter(prefix="/videos", tags=["videos"])

@router.get("/", response_model=List[VideoListResponse])
def list_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all uploaded videos"""
    videos = db.query(Video).offset(skip).limit(limit).all()
    return videos

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video by ID"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
