import os
import sys
import logging
from pathlib import Path

# Add src to Python path to import video_processor
src_path = Path(__file__).resolve().parent.parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from video_processor.pipeline import VideoProcessingPipeline
from app.database import SessionLocal
from app.models.video import Video, Scene, Keyframe
import json

logger = logging.getLogger(__name__)

def process_video(video_id: int):
    """
    Process a video: detect scenes, extract keyframes, analyze importance

    Args:
        video_id: ID of video record in database
    """
    db = SessionLocal()
    try:
        # Get video record
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            logger.error(f"Video {video_id} not found")
            return

        logger.info(f"Processing video: {video.filename}")

        # Update status
        video.status = "processing"
        db.commit()

        # Initialize pipeline
        pipeline = VideoProcessingPipeline(
            video_path=video.file_path,
            scene_threshold=30.0,
            keyframes_per_scene=3
        )

        # Process video
        result = pipeline.process()

        if not result:
            logger.error(f"Processing failed for video {video_id}")
            video.status = "failed"
            video.error_message = "Processing pipeline failed"
            db.commit()
            return

        # Extract metadata
        metadata = result.get('metadata', {})
        video.duration = metadata.get('duration')
        video.width = metadata.get('width')
        video.height = metadata.get('height')
        video.fps = metadata.get('fps')
        video.codec = metadata.get('codec')

        # Save scenes
        scenes_data = result.get('scenes', [])
        for scene_data in scenes_data:
            scene = Scene(
                video_id=video.id,
                start_frame=scene_data['start_frame'],
                end_frame=scene_data['end_frame'],
                start_time=scene_data['start_time'],
                end_time=scene_data['end_time'],
                duration=scene_data['duration']
            )
            db.add(scene)
            db.flush()  # Get scene.id

            # Save keyframes for this scene
            keyframes_data = scene_data.get('keyframes', [])
            for kf_data in keyframes_data:
                keyframe = Keyframe(
                    video_id=video.id,
                    scene_id=scene.id,
                    frame_number=kf_data['frame_number'],
                    timestamp=kf_data['timestamp'],
                    importance_score=kf_data.get('importance_score', 0.0),
                    frame_path=kf_data.get('frame_path')
                )
                db.add(keyframe)

        # Update status
        video.status = "completed"
        video.processing_completed_at = result.get('processing_time')

        db.commit()

        logger.info(f"Processing completed for video {video_id}")
        logger.info(f"Detected {len(scenes_data)} scenes")

        return result

    except Exception as e:
        logger.error(f"Error processing video {video_id}: {e}", exc_info=True)
        video.status = "failed"
        video.error_message = str(e)
        db.commit()
        raise
    finally:
        db.close()


def process_video_async(video_id: int):
    """
    Process video asynchronously (for background tasks)
    """
    import threading
    thread = threading.Thread(target=process_video, args=(video_id,))
    thread.daemon = True
    thread.start()
    logger.info(f"Started background processing for video {video_id}")
