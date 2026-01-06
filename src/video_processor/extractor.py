"""Video frame extraction utilities"""

import cv2
import os
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class VideoMetadata:
    """Video file metadata"""
    duration: float
    fps: float
    frame_count: int
    width: int
    height: int
    codec: str


@dataclass
class Frame:
    """Represents a video frame"""
    frame_number: int
    timestamp: float
    image: np.ndarray

    def save(self, path: str) -> None:
        """Save frame to file"""
        cv2.imwrite(path, self.image)


class VideoFrameExtractor:
    """Extract frames from video files"""

    def __init__(self, video_path: str, max_resolution: Optional[int] = None):
        """
        Initialize video frame extractor

        Args:
            video_path: Path to video file
            max_resolution: Maximum width for extracted frames (maintains aspect ratio)
        """
        self.video_path = Path(video_path)
        self.max_resolution = max_resolution

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        self.cap = cv2.VideoCapture(str(video_path))
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")

        self.metadata = self._extract_metadata()

    def _extract_metadata(self) -> VideoMetadata:
        """Extract video metadata"""
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        codec = int(self.cap.get(cv2.CAP_PROP_FOURCC))

        return VideoMetadata(
            duration=frame_count / fps if fps > 0 else 0,
            fps=fps,
            frame_count=frame_count,
            width=width,
            height=height,
            codec=codec
        )

    def _resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame if max_resolution is set"""
        if self.max_resolution and frame.shape[1] > self.max_resolution:
            aspect_ratio = frame.shape[0] / frame.shape[1]
            new_width = self.max_resolution
            new_height = int(new_width * aspect_ratio)
            return cv2.resize(frame, (new_width, new_height))
        return frame

    def extract_frame(self, frame_number: int) -> Optional[Frame]:
        """
        Extract a specific frame by frame number

        Args:
            frame_number: Frame number to extract

        Returns:
            Frame object or None if extraction fails
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = self._resize_frame(frame)
        timestamp = frame_number / self.metadata.fps

        return Frame(frame_number=frame_number, timestamp=timestamp, image=frame)

    def extract_at_timestamp(self, timestamp: float) -> Optional[Frame]:
        """
        Extract frame at specific timestamp

        Args:
            timestamp: Time in seconds

        Returns:
            Frame object or None if extraction fails
        """
        frame_number = int(timestamp * self.metadata.fps)
        return self.extract_frame(frame_number)

    def extract_frames_interval(
        self,
        interval_seconds: float = 1.0,
        start_time: float = 0.0,
        end_time: Optional[float] = None
    ) -> List[Frame]:
        """
        Extract frames at regular intervals

        Args:
            interval_seconds: Time interval between frames
            start_time: Start time in seconds
            end_time: End time in seconds (None for end of video)

        Returns:
            List of Frame objects
        """
        end_time = end_time or self.metadata.duration
        frames = []

        current_time = start_time
        while current_time <= end_time:
            frame = self.extract_at_timestamp(current_time)
            if frame:
                frames.append(frame)
            current_time += interval_seconds

        return frames

    def extract_frames_by_numbers(self, frame_numbers: List[int]) -> List[Frame]:
        """
        Extract specific frames by frame numbers

        Args:
            frame_numbers: List of frame numbers to extract

        Returns:
            List of Frame objects
        """
        frames = []
        for frame_number in frame_numbers:
            frame = self.extract_frame(frame_number)
            if frame:
                frames.append(frame)
        return frames

    def save_frames(self, frames: List[Frame], output_dir: str, prefix: str = "frame") -> List[str]:
        """
        Save frames to directory

        Args:
            frames: List of Frame objects
            output_dir: Output directory path
            prefix: Filename prefix

        Returns:
            List of saved file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_paths = []
        for frame in frames:
            filename = f"{prefix}_{frame.frame_number:06d}.jpg"
            filepath = output_path / filename
            frame.save(str(filepath))
            saved_paths.append(str(filepath))

        return saved_paths

    def __del__(self):
        """Release video capture"""
        if hasattr(self, 'cap'):
            self.cap.release()
