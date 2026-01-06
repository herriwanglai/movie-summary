"""Select keyframes from scenes"""

import numpy as np
from typing import List, Optional
from dataclasses import dataclass
from .extractor import VideoFrameExtractor, Frame
from .scene_detector import Scene


@dataclass
class Keyframe:
    """Represents a keyframe with associated metadata"""
    frame: Frame
    scene_number: int
    keyframe_type: str  # 'first', 'middle', 'last', 'representative'
    importance_score: float = 1.0


class KeyframeSelector:
    """Select representative keyframes from scenes"""

    def __init__(self, video_extractor: VideoFrameExtractor):
        """
        Initialize keyframe selector

        Args:
            video_extractor: VideoFrameExtractor instance
        """
        self.extractor = video_extractor

    def select_from_scene(
        self,
        scene: Scene,
        method: str = 'middle',
        num_keyframes: int = 1
    ) -> List[Keyframe]:
        """
        Select keyframes from a scene

        Args:
            scene: Scene object
            method: Selection method ('first', 'middle', 'last', 'distributed', 'variance')
            num_keyframes: Number of keyframes to extract

        Returns:
            List of Keyframe objects
        """
        if method == 'first':
            return self._select_first(scene)
        elif method == 'middle':
            return self._select_middle(scene)
        elif method == 'last':
            return self._select_last(scene)
        elif method == 'distributed':
            return self._select_distributed(scene, num_keyframes)
        elif method == 'variance':
            return self._select_by_variance(scene, num_keyframes)
        else:
            raise ValueError(f"Unknown method: {method}")

    def _select_first(self, scene: Scene) -> List[Keyframe]:
        """Select first frame of scene"""
        frame = self.extractor.extract_frame(scene.start_frame)
        if frame:
            return [Keyframe(
                frame=frame,
                scene_number=scene.scene_number,
                keyframe_type='first'
            )]
        return []

    def _select_middle(self, scene: Scene) -> List[Keyframe]:
        """Select middle frame of scene"""
        middle_frame = (scene.start_frame + scene.end_frame) // 2
        frame = self.extractor.extract_frame(middle_frame)
        if frame:
            return [Keyframe(
                frame=frame,
                scene_number=scene.scene_number,
                keyframe_type='middle'
            )]
        return []

    def _select_last(self, scene: Scene) -> List[Keyframe]:
        """Select last frame of scene"""
        frame = self.extractor.extract_frame(scene.end_frame)
        if frame:
            return [Keyframe(
                frame=frame,
                scene_number=scene.scene_number,
                keyframe_type='last'
            )]
        return []

    def _select_distributed(self, scene: Scene, num_keyframes: int) -> List[Keyframe]:
        """Select evenly distributed keyframes across scene"""
        scene_length = scene.end_frame - scene.start_frame
        if num_keyframes <= 0:
            return []

        if num_keyframes == 1:
            return self._select_middle(scene)

        keyframes = []
        step = scene_length / (num_keyframes + 1)

        for i in range(1, num_keyframes + 1):
            frame_number = int(scene.start_frame + i * step)
            frame = self.extractor.extract_frame(frame_number)
            if frame:
                keyframes.append(Keyframe(
                    frame=frame,
                    scene_number=scene.scene_number,
                    keyframe_type='distributed',
                    importance_score=1.0
                ))

        return keyframes

    def _select_by_variance(self, scene: Scene, num_keyframes: int) -> List[Keyframe]:
        """
        Select keyframes based on image variance (higher variance = more interesting)

        Args:
            scene: Scene object
            num_keyframes: Number of keyframes to select

        Returns:
            List of Keyframe objects
        """
        # Sample frames from the scene
        sample_rate = max(1, (scene.end_frame - scene.start_frame) // 100)
        frame_numbers = range(scene.start_frame, scene.end_frame, sample_rate)

        # Calculate variance for each frame
        frame_variances = []
        for frame_num in frame_numbers:
            frame = self.extractor.extract_frame(frame_num)
            if frame:
                # Calculate variance of grayscale image
                gray = np.mean(frame.image, axis=2)
                variance = np.var(gray)
                frame_variances.append((frame_num, variance, frame))

        # Sort by variance and select top N
        frame_variances.sort(key=lambda x: x[1], reverse=True)
        selected = frame_variances[:num_keyframes]

        # Sort by frame number to maintain temporal order
        selected.sort(key=lambda x: x[0])

        keyframes = []
        for frame_num, variance, frame in selected:
            keyframes.append(Keyframe(
                frame=frame,
                scene_number=scene.scene_number,
                keyframe_type='representative',
                importance_score=float(variance)
            ))

        return keyframes

    def select_from_scenes(
        self,
        scenes: List[Scene],
        keyframes_per_scene: int = 1,
        method: str = 'middle'
    ) -> List[Keyframe]:
        """
        Select keyframes from multiple scenes

        Args:
            scenes: List of Scene objects
            keyframes_per_scene: Number of keyframes per scene
            method: Selection method

        Returns:
            List of all Keyframe objects
        """
        all_keyframes = []
        for scene in scenes:
            keyframes = self.select_from_scene(scene, method, keyframes_per_scene)
            all_keyframes.extend(keyframes)

        return all_keyframes

    def save_keyframes(
        self,
        keyframes: List[Keyframe],
        output_dir: str,
        prefix: str = "keyframe"
    ) -> List[str]:
        """
        Save keyframes to directory

        Args:
            keyframes: List of Keyframe objects
            output_dir: Output directory
            prefix: Filename prefix

        Returns:
            List of saved file paths
        """
        from pathlib import Path

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_paths = []
        for idx, keyframe in enumerate(keyframes):
            filename = (f"{prefix}_scene{keyframe.scene_number:03d}_"
                       f"{keyframe.keyframe_type}_{idx:04d}.jpg")
            filepath = output_path / filename
            keyframe.frame.save(str(filepath))
            saved_paths.append(str(filepath))

        return saved_paths
