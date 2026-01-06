"""Scene detection using content-based analysis"""

from scenedetect import open_video, SceneManager, split_video_ffmpeg
from scenedetect.detectors import ContentDetector, ThresholdDetector
from scenedetect.video_splitter import split_video_ffmpeg
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Scene:
    """Represents a detected scene"""
    scene_number: int
    start_frame: int
    end_frame: int
    start_time: float
    end_time: float
    duration: float

    def __repr__(self):
        return (f"Scene {self.scene_number}: "
                f"{self.start_time:.2f}s - {self.end_time:.2f}s "
                f"({self.duration:.2f}s)")


class SceneDetector:
    """Detect scenes in video using content-based analysis"""

    def __init__(
        self,
        video_path: str,
        threshold: float = 27.0,
        min_scene_length: float = 1.0
    ):
        """
        Initialize scene detector

        Args:
            video_path: Path to video file
            threshold: Detection threshold (lower = more sensitive)
            min_scene_length: Minimum scene length in seconds
        """
        self.video_path = Path(video_path)
        self.threshold = threshold
        self.min_scene_length = min_scene_length

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

    def detect_scenes(self) -> List[Scene]:
        """
        Detect scenes in the video

        Returns:
            List of Scene objects
        """
        video = open_video(str(self.video_path))
        scene_manager = SceneManager()

        # Use ContentDetector for scene change detection
        scene_manager.add_detector(
            ContentDetector(threshold=self.threshold, min_scene_len=int(self.min_scene_length * video.frame_rate))
        )

        # Detect scenes
        scene_manager.detect_scenes(video)
        scene_list = scene_manager.get_scene_list()

        # Convert to Scene objects
        scenes = []
        for idx, (start_time, end_time) in enumerate(scene_list, start=1):
            start_frame = start_time.get_frames()
            end_frame = end_time.get_frames()
            start_seconds = start_time.get_seconds()
            end_seconds = end_time.get_seconds()

            scene = Scene(
                scene_number=idx,
                start_frame=start_frame,
                end_frame=end_frame,
                start_time=start_seconds,
                end_time=end_seconds,
                duration=end_seconds - start_seconds
            )
            scenes.append(scene)

        return scenes

    def split_video_by_scenes(
        self,
        output_dir: str,
        scenes: Optional[List[Scene]] = None
    ) -> List[str]:
        """
        Split video into separate files by scenes

        Args:
            output_dir: Output directory for scene videos
            scenes: List of scenes (if None, will detect scenes first)

        Returns:
            List of output file paths
        """
        if scenes is None:
            scenes = self.detect_scenes()

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Create scene list format for scenedetect
        video = open_video(str(self.video_path))
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=self.threshold))
        scene_manager.detect_scenes(video)

        # Split video
        output_files = split_video_ffmpeg(
            str(self.video_path),
            scene_manager.get_scene_list(),
            output_dir=str(output_path),
            show_progress=True
        )

        return output_files

    def get_scene_stats(self, scenes: List[Scene]) -> dict:
        """
        Get statistics about detected scenes

        Args:
            scenes: List of Scene objects

        Returns:
            Dictionary with scene statistics
        """
        if not scenes:
            return {"total_scenes": 0}

        durations = [scene.duration for scene in scenes]

        return {
            "total_scenes": len(scenes),
            "average_scene_duration": sum(durations) / len(durations),
            "shortest_scene": min(durations),
            "longest_scene": max(durations),
            "total_duration": scenes[-1].end_time if scenes else 0
        }
