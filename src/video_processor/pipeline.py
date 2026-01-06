"""Complete video processing pipeline orchestrating all components"""

from pathlib import Path
import logging
from typing import Dict, List, Optional
import cv2

from .extractor import VideoFrameExtractor, Frame
from .scene_detector import SceneDetector, Scene
from .keyframe_selector import KeyframeSelector, Keyframe

logger = logging.getLogger(__name__)


class VideoProcessingPipeline:
    """Orchestrate complete video processing workflow"""

    def __init__(self, video_path: str):
        """
        Initialize video processing pipeline

        Args:
            video_path: Path to video file
        """
        self.video_path = Path(video_path)

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        logger.info(f"Initializing video processing pipeline for: {self.video_path.name}")

        # Initialize components
        self.extractor = VideoFrameExtractor(str(video_path))
        self.scene_detector = SceneDetector(str(video_path))
        self.keyframe_selector = KeyframeSelector(self.extractor)

    def process(
        self,
        output_dir: Optional[Path] = None,
        keyframes_per_scene: int = 3,
        keyframe_method: str = "middle",
        save_keyframes: bool = True
    ) -> Dict:
        """
        Run complete processing pipeline

        Args:
            output_dir: Directory to save outputs (optional)
            keyframes_per_scene: Number of keyframes to extract per scene
            keyframe_method: Method for keyframe selection
            save_keyframes: Whether to save keyframe images

        Returns:
            Dict with scenes, keyframes, and metadata
        """
        logger.info(f"Starting video processing: {self.video_path.name}")

        # 1. Extract metadata
        logger.info("Extracting video metadata...")
        metadata = self._extract_metadata()
        logger.info(f"Video: {metadata['duration']:.2f}s, "
                   f"{metadata['width']}x{metadata['height']}, "
                   f"{metadata['fps']:.2f}fps")

        # 2. Detect scenes
        logger.info("Detecting scenes...")
        scenes = self.scene_detector.detect_scenes()
        logger.info(f"Detected {len(scenes)} scenes")

        # Get scene statistics
        scene_stats = self.scene_detector.get_scene_stats(scenes)
        logger.info(f"Scene stats: avg duration={scene_stats['average_scene_duration']:.2f}s, "
                   f"shortest={scene_stats['shortest_scene']:.2f}s, "
                   f"longest={scene_stats['longest_scene']:.2f}s")

        # 3. Select keyframes from scenes
        logger.info(f"Selecting keyframes ({keyframe_method} method, {keyframes_per_scene} per scene)...")
        keyframes = self.keyframe_selector.select_from_scenes(
            scenes,
            keyframes_per_scene=keyframes_per_scene,
            method=keyframe_method
        )
        logger.info(f"Selected {len(keyframes)} total keyframes")

        # 4. Save keyframe images if output directory provided
        saved_paths = []
        if output_dir and save_keyframes:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"Saving keyframes to {output_dir}...")
            saved_paths = self._save_keyframes(keyframes, output_dir)
            logger.info(f"Saved {len(saved_paths)} keyframe images")

        # 5. Build results
        logger.info("Building results...")
        results = {
            'metadata': metadata,
            'scenes': self._serialize_scenes(scenes),
            'scene_stats': scene_stats,
            'keyframes': self._serialize_keyframes(keyframes, saved_paths),
            'total_keyframes': len(keyframes),
            'processing_summary': {
                'video_file': str(self.video_path),
                'total_scenes': len(scenes),
                'total_keyframes': len(keyframes),
                'keyframes_per_scene': keyframes_per_scene,
                'keyframe_method': keyframe_method
            }
        }

        logger.info("Video processing complete!")

        return results

    def _extract_metadata(self) -> Dict:
        """Extract video metadata"""
        metadata = self.extractor.metadata
        return {
            'duration': metadata.duration,
            'fps': metadata.fps,
            'frame_count': metadata.frame_count,
            'width': metadata.width,
            'height': metadata.height,
            'codec': str(metadata.codec),
            'filename': self.video_path.name
        }

    def _serialize_scenes(self, scenes: List[Scene]) -> List[Dict]:
        """Convert Scene objects to dictionaries"""
        return [
            {
                'scene_number': scene.scene_number,
                'start_time': scene.start_time,
                'end_time': scene.end_time,
                'duration': scene.duration,
                'start_frame': scene.start_frame,
                'end_frame': scene.end_frame
            }
            for scene in scenes
        ]

    def _serialize_keyframes(
        self,
        keyframes: List[Keyframe],
        saved_paths: List[str]
    ) -> List[Dict]:
        """Convert Keyframe objects to dictionaries"""
        result = []
        for i, keyframe in enumerate(keyframes):
            kf_dict = {
                'scene_number': keyframe.scene_number,
                'timestamp': keyframe.frame.timestamp,
                'frame_number': keyframe.frame.frame_number,
                'keyframe_type': keyframe.keyframe_type,
                'importance_score': keyframe.importance_score
            }
            if i < len(saved_paths):
                kf_dict['image_path'] = saved_paths[i]
            result.append(kf_dict)
        return result

    def _save_keyframes(
        self,
        keyframes: List[Keyframe],
        output_dir: Path
    ) -> List[str]:
        """Save keyframes to directory"""
        saved_paths = []

        for keyframe in keyframes:
            filename = (f"scene{keyframe.scene_number:03d}_"
                       f"{keyframe.keyframe_type}_"
                       f"frame{keyframe.frame.frame_number:06d}.jpg")
            filepath = output_dir / filename

            # Save frame
            keyframe.frame.save(str(filepath))
            saved_paths.append(str(filepath))

        return saved_paths

    def generate_thumbnail(
        self,
        output_path: str,
        timestamp: Optional[float] = None
    ) -> str:
        """
        Generate video thumbnail

        Args:
            output_path: Path to save thumbnail
            timestamp: Optional timestamp (defaults to 10% of duration)

        Returns:
            Path to generated thumbnail
        """
        if timestamp is None:
            timestamp = self.extractor.metadata.duration * 0.1

        frame = self.extractor.extract_at_timestamp(timestamp)

        if not frame:
            raise ValueError(f"Failed to extract frame at {timestamp}s")

        # Resize to thumbnail size (320x180)
        thumbnail = cv2.resize(frame.image, (320, 180))

        # Save thumbnail
        cv2.imwrite(output_path, thumbnail)
        logger.info(f"Generated thumbnail at {output_path}")

        return output_path

    def extract_scene_clips(
        self,
        output_dir: Path,
        max_scenes: Optional[int] = None
    ) -> List[str]:
        """
        Extract individual scene clips as separate video files

        Args:
            output_dir: Directory to save scene clips
            max_scenes: Maximum number of scenes to extract (None for all)

        Returns:
            List of output file paths
        """
        logger.info("Extracting scene clips...")

        scenes = self.scene_detector.detect_scenes()
        if max_scenes:
            scenes = scenes[:max_scenes]

        output_dir = Path(output_dir)
        output_files = self.scene_detector.split_video_by_scenes(
            str(output_dir),
            scenes=scenes
        )

        logger.info(f"Extracted {len(output_files)} scene clips")
        return output_files
