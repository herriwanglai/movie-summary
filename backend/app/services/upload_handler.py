from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.video import Video
from app.config import settings
import logging
import os

logger = logging.getLogger(__name__)

def handle_upload_complete(file_path: str, metadata: dict):
    """
    Triggered when TUS upload completes

    Args:
        file_path: Full path to uploaded video file
        metadata: Dict containing filename, filetype, etc.
    """
    logger.info(f"Upload complete: {file_path}")
    logger.info(f"Metadata: {metadata}")

    # Get filename and file info
    filename = metadata.get('filename', os.path.basename(file_path))
    file_size = os.path.getsize(file_path)
    mime_type = metadata.get('filetype', 'video/mp4')

    # Create database record
    db = SessionLocal()
    try:
        video = Video(
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            status="uploaded"
        )
        db.add(video)
        db.commit()
        db.refresh(video)

        logger.info(f"Created video record with ID: {video.id}")

        # Trigger video processing asynchronously
        try:
            from app.services.video_processor import process_video_async
            process_video_async(video.id)
            logger.info(f"Triggered video processing for video {video.id}")
        except Exception as e:
            logger.error(f"Failed to trigger video processing: {e}")
            # Don't fail the upload if processing trigger fails

        return video.id

    except Exception as e:
        logger.error(f"Failed to create video record: {e}")
        db.rollback()
        raise
    finally:
        db.close()
