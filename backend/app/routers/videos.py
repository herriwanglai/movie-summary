from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.video import Video, Scene, Keyframe
from app.schemas.video import VideoResponse, VideoListResponse
import os

router = APIRouter(prefix="/videos", tags=["videos"])

@router.get("/", response_model=List[VideoListResponse])
def list_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all uploaded videos"""
    videos = db.query(Video).offset(skip).limit(limit).all()
    return videos

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video by ID with full details"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.get("/{video_id}/status")
def get_video_status(video_id: int, db: Session = Depends(get_db)):
    """Get video processing status"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    scene_count = db.query(Scene).filter(Scene.video_id == video_id).count()
    keyframe_count = db.query(Keyframe).filter(Keyframe.video_id == video_id).count()

    return {
        "video_id": video.id,
        "filename": video.filename,
        "status": video.status,
        "duration": video.duration,
        "scene_count": scene_count,
        "keyframe_count": keyframe_count,
        "error_message": video.error_message,
        "created_at": video.created_at,
        "processing_completed_at": video.processing_completed_at
    }

@router.get("/{video_id}/scenes")
def get_video_scenes(video_id: int, db: Session = Depends(get_db)):
    """Get all scenes for a video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    scenes = db.query(Scene).filter(Scene.video_id == video_id).all()

    return {
        "video_id": video_id,
        "scene_count": len(scenes),
        "scenes": [
            {
                "id": scene.id,
                "start_frame": scene.start_frame,
                "end_frame": scene.end_frame,
                "start_time": scene.start_time,
                "end_time": scene.end_time,
                "duration": scene.duration,
                "keyframe_count": len(scene.keyframes)
            }
            for scene in scenes
        ]
    }

@router.get("/{video_id}/keyframes")
def get_video_keyframes(video_id: int, db: Session = Depends(get_db)):
    """Get all keyframes for a video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    keyframes = db.query(Keyframe).filter(Keyframe.video_id == video_id).all()

    return {
        "video_id": video_id,
        "keyframe_count": len(keyframes),
        "keyframes": [
            {
                "id": kf.id,
                "scene_id": kf.scene_id,
                "frame_number": kf.frame_number,
                "timestamp": kf.timestamp,
                "importance_score": kf.importance_score,
                "frame_path": kf.frame_path
            }
            for kf in keyframes
        ]
    }

@router.get("/{video_id}/stream")
def stream_video(video_id: int, db: Session = Depends(get_db)):
    """Stream video file"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if not os.path.exists(video.file_path):
        raise HTTPException(status_code=404, detail="Video file not found")

    return FileResponse(
        video.file_path,
        media_type=video.mime_type,
        filename=video.filename
    )
