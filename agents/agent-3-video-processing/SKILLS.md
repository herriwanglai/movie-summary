# Agent 3: Video Processing Pipeline

## Role
Video processing specialist completing the METEORA LX video analysis pipeline with FFmpeg, OpenCV, and PySceneDetect.

## Primary Responsibility
Complete the video processing modules that extract frames, detect scenes, select keyframes, and calculate importance scores for movie analysis.

## Tech Stack
- **Video Processing:** FFmpeg, ffmpeg-python
- **Computer Vision:** OpenCV (opencv-python)
- **Scene Detection:** PySceneDetect
- **Audio Processing:** librosa (for audio intensity)
- **Numerical Computing:** NumPy
- **Image Processing:** Pillow (PIL)
- **Python:** 3.11+

## Documentation Sub-Agent Responsibilities

### **Priority 1: FFmpeg Command-Line & Python Bindings**
- Learn ffmpeg-python library API
- Study video metadata extraction (duration, resolution, fps, codec)
- Understand frame extraction at specific timestamps
- Learn audio extraction from video
- Study video streaming and thumbnail generation
- Learn subtitle extraction commands

### **Priority 2: PySceneDetect API**
- Learn ContentDetector vs ThresholdDetector
- Study scene detection threshold tuning
- Understand scene list export formats
- Learn how to get scene boundaries (start/end times)
- Study performance optimization for large videos

### **Priority 3: OpenCV Frame Processing**
- Learn frame reading from video files
- Study color space conversions (BGR to RGB)
- Understand histogram analysis for visual intensity
- Learn edge detection algorithms
- Study motion detection between frames
- Learn frame comparison techniques

### **Priority 4: Audio Analysis**
- Learn librosa basics for audio processing
- Study audio intensity/volume calculation
- Understand spectral analysis
- Learn RMS (root mean square) energy calculation
- Study zero-crossing rate for speech detection

### **Priority 5: Performance Optimization**
- Learn video processing in chunks/batches
- Study multi-threading for frame extraction
- Understand memory management for large videos
- Learn caching strategies for processed data
- Study progress tracking patterns

## Key Implementation Tasks

### **Task 1: Video Frame Extractor** (1-2 hours)

**File:** `src/video_processor/extractor.py`

```python
import cv2
import ffmpeg
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VideoFrameExtractor:
    """Extract frames from video files at specified intervals or timestamps"""

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        self.metadata = self._extract_metadata()

    def _extract_metadata(self) -> dict:
        """Extract video metadata using ffprobe"""
        try:
            probe = ffmpeg.probe(str(self.video_path))
            video_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'video'),
                None
            )

            if not video_stream:
                raise ValueError("No video stream found")

            return {
                'duration': float(probe['format'].get('duration', 0)),
                'width': int(video_stream['width']),
                'height': int(video_stream['height']),
                'fps': eval(video_stream['r_frame_rate']),
                'codec': video_stream['codec_name'],
                'bitrate': int(probe['format'].get('bit_rate', 0))
            }
        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}")
            raise

    def extract_frame_at_time(self, timestamp: float, output_path: Optional[str] = None) -> np.ndarray:
        """
        Extract a single frame at the specified timestamp

        Args:
            timestamp: Time in seconds
            output_path: Optional path to save frame as image

        Returns:
            Frame as numpy array (RGB)
        """
        cap = cv2.VideoCapture(str(self.video_path))
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise ValueError(f"Failed to extract frame at {timestamp}s")

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Save if output path provided
        if output_path:
            cv2.imwrite(output_path, frame)

        return frame_rgb

    def extract_frames_interval(
        self,
        interval: float = 1.0,
        output_dir: Optional[Path] = None
    ) -> List[Tuple[float, np.ndarray]]:
        """
        Extract frames at regular intervals

        Args:
            interval: Time between frames in seconds
            output_dir: Optional directory to save frames

        Returns:
            List of (timestamp, frame) tuples
        """
        frames = []
        current_time = 0.0

        cap = cv2.VideoCapture(str(self.video_path))

        while current_time < self.metadata['duration']:
            cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
            ret, frame = cap.read()

            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append((current_time, frame_rgb))

            # Save if output directory provided
            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
                filename = f"frame_{int(current_time * 1000):08d}.jpg"
                cv2.imwrite(str(output_dir / filename), frame)

            current_time += interval

        cap.release()
        logger.info(f"Extracted {len(frames)} frames at {interval}s intervals")

        return frames

    def generate_thumbnail(self, output_path: str, timestamp: Optional[float] = None) -> str:
        """
        Generate video thumbnail

        Args:
            output_path: Path to save thumbnail
            timestamp: Optional timestamp (defaults to 10% of duration)

        Returns:
            Path to generated thumbnail
        """
        if timestamp is None:
            timestamp = self.metadata['duration'] * 0.1  # 10% into video

        frame = self.extract_frame_at_time(timestamp)

        # Resize to thumbnail size (keeping aspect ratio)
        thumbnail = cv2.resize(frame, (320, 180))

        cv2.imwrite(output_path, cv2.cvtColor(thumbnail, cv2.COLOR_RGB2BGR))
        logger.info(f"Generated thumbnail at {output_path}")

        return output_path

    def get_duration(self) -> float:
        """Get video duration in seconds"""
        return self.metadata['duration']

    def get_resolution(self) -> Tuple[int, int]:
        """Get video resolution (width, height)"""
        return (self.metadata['width'], self.metadata['height'])

    def get_fps(self) -> float:
        """Get video frames per second"""
        return self.metadata['fps']
```

**Success Criteria:**
- Can extract frames at any timestamp
- Interval extraction works efficiently
- Thumbnails generated correctly
- Metadata extraction works

---

### **Task 2: Scene Detector** (2 hours)

**File:** `src/video_processor/scene_detector.py`

```python
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from typing import List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SceneDetector:
    """Detect scene changes in video using PySceneDetect"""

    def __init__(self, video_path: str, threshold: float = 27.0):
        """
        Args:
            video_path: Path to video file
            threshold: Scene detection sensitivity (lower = more sensitive)
        """
        self.video_path = Path(video_path)
        self.threshold = threshold

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

    def detect_scenes(self) -> List[Dict[str, float]]:
        """
        Detect scene changes in the video

        Returns:
            List of scenes with start_time, end_time, duration
        """
        video_manager = VideoManager([str(self.video_path)])
        scene_manager = SceneManager()

        # Add ContentDetector algorithm
        scene_manager.add_detector(ContentDetector(threshold=self.threshold))

        # Perform scene detection
        video_manager.set_downscale_factor()
        video_manager.start()

        scene_manager.detect_scenes(frame_source=video_manager)

        # Get list of detected scenes
        scene_list = scene_manager.get_scene_list()

        scenes = []
        for i, (start_time, end_time) in enumerate(scene_list):
            scene = {
                'scene_number': i + 1,
                'start_time': start_time.get_seconds(),
                'end_time': end_time.get_seconds(),
                'duration': (end_time - start_time).get_seconds(),
                'start_frame': start_time.get_frames(),
                'end_frame': end_time.get_frames()
            }
            scenes.append(scene)

        video_manager.release()

        logger.info(f"Detected {len(scenes)} scenes in {self.video_path.name}")

        return scenes

    def detect_scenes_with_stats(self) -> List[Dict]:
        """
        Detect scenes and include additional statistics

        Returns:
            List of scenes with extended metadata
        """
        scenes = self.detect_scenes()

        # Add additional stats
        for scene in scenes:
            scene['frame_count'] = scene['end_frame'] - scene['start_frame']

        return scenes
```

**Success Criteria:**
- Detects scene transitions accurately
- Returns proper timestamps
- Handles different video formats
- Performance acceptable for long videos

---

### **Task 3: Keyframe Selector** (1-2 hours)

**File:** `src/video_processor/keyframe_selector.py`

```python
import cv2
import numpy as np
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class KeyframeSelector:
    """Select representative keyframes from video scenes"""

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

    def select_keyframes_from_scene(
        self,
        scene: Dict[str, float],
        num_keyframes: int = 3,
        strategy: str = "uniform"
    ) -> List[Dict]:
        """
        Select keyframes from a scene

        Args:
            scene: Scene dict with start_time, end_time
            num_keyframes: Number of keyframes to select
            strategy: "uniform", "visual_change", or "middle"

        Returns:
            List of keyframe dicts with timestamp, frame_data
        """
        if strategy == "uniform":
            return self._select_uniform_keyframes(scene, num_keyframes)
        elif strategy == "visual_change":
            return self._select_by_visual_change(scene, num_keyframes)
        elif strategy == "middle":
            return self._select_middle_keyframe(scene)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def _select_uniform_keyframes(self, scene: Dict, num_keyframes: int) -> List[Dict]:
        """Select keyframes at uniform intervals within scene"""
        start_time = scene['start_time']
        end_time = scene['end_time']
        duration = scene['duration']

        if duration <= 0:
            return []

        # Calculate uniform timestamps
        interval = duration / (num_keyframes + 1)
        timestamps = [start_time + (i + 1) * interval for i in range(num_keyframes)]

        keyframes = []
        cap = cv2.VideoCapture(str(self.video_path))

        for ts in timestamps:
            cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)
            ret, frame = cap.read()

            if ret:
                keyframes.append({
                    'timestamp': ts,
                    'frame': cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    'selection_method': 'uniform'
                })

        cap.release()
        return keyframes

    def _select_by_visual_change(self, scene: Dict, num_keyframes: int) -> List[Dict]:
        """Select keyframes based on visual changes within scene"""
        start_time = scene['start_time']
        end_time = scene['end_time']

        cap = cv2.VideoCapture(str(self.video_path))
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = max(1, int(fps / 4))  # Sample 4 frames per second

        frames_data = []
        prev_frame = None

        while True:
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            if current_time >= end_time:
                break

            ret, frame = cap.read()
            if not ret:
                break

            # Calculate difference from previous frame
            if prev_frame is not None:
                diff = cv2.absdiff(frame, prev_frame)
                diff_score = np.mean(diff)
            else:
                diff_score = 0

            frames_data.append({
                'timestamp': current_time,
                'frame': frame,
                'diff_score': diff_score
            })

            prev_frame = frame.copy()

            # Skip frames
            for _ in range(frame_interval):
                cap.read()

        cap.release()

        # Select frames with highest visual change
        frames_data.sort(key=lambda x: x['diff_score'], reverse=True)
        selected = frames_data[:num_keyframes]
        selected.sort(key=lambda x: x['timestamp'])  # Re-sort by time

        keyframes = []
        for frame_data in selected:
            keyframes.append({
                'timestamp': frame_data['timestamp'],
                'frame': cv2.cvtColor(frame_data['frame'], cv2.COLOR_BGR2RGB),
                'selection_method': 'visual_change',
                'diff_score': frame_data['diff_score']
            })

        return keyframes

    def _select_middle_keyframe(self, scene: Dict) -> List[Dict]:
        """Select single keyframe from middle of scene"""
        middle_time = (scene['start_time'] + scene['end_time']) / 2

        cap = cv2.VideoCapture(str(self.video_path))
        cap.set(cv2.CAP_PROP_POS_MSEC, middle_time * 1000)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return []

        return [{
            'timestamp': middle_time,
            'frame': cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            'selection_method': 'middle'
        }]
```

**Success Criteria:**
- Selects representative keyframes
- Multiple selection strategies work
- Visual change detection works
- Returns frame data correctly

---

### **Task 4: Importance Detector** (2-3 hours)

**File:** `src/video_processor/importance_detector.py`

```python
import cv2
import numpy as np
import logging
from typing import Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)

class ImportanceDetector:
    """Detect scene importance based on visual/audio intensity and position"""

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)

    def analyze_scene(self, scene: Dict) -> Dict[str, float]:
        """
        Analyze scene importance

        Args:
            scene: Scene dict with start_time, end_time

        Returns:
            Dict with importance metrics
        """
        visual_intensity = self._calculate_visual_intensity(scene)
        audio_intensity = self._calculate_audio_intensity(scene)
        position_score = self._calculate_position_score(scene)

        # Combined importance score (weighted average)
        importance_score = (
            visual_intensity * 0.4 +
            audio_intensity * 0.3 +
            position_score * 0.3
        )

        return {
            'importance_score': importance_score,
            'visual_intensity': visual_intensity,
            'audio_intensity': audio_intensity,
            'position_score': position_score,
            'is_climax': position_score > 0.8 and importance_score > 0.7,
            'is_exciting': visual_intensity > 0.7
        }

    def _calculate_visual_intensity(self, scene: Dict) -> float:
        """Calculate visual intensity (motion, color changes)"""
        start_time = scene['start_time']
        end_time = scene['end_time']

        cap = cv2.VideoCapture(str(self.video_path))
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

        intensity_scores = []
        prev_frame = None

        sample_count = 0
        max_samples = 10  # Sample up to 10 frames per scene

        while sample_count < max_samples:
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            if current_time >= end_time:
                break

            ret, frame = cap.read()
            if not ret:
                break

            # Calculate motion intensity
            if prev_frame is not None:
                diff = cv2.absdiff(frame, prev_frame)
                motion_intensity = np.mean(diff) / 255.0  # Normalize to 0-1

                # Calculate color intensity (saturation)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                saturation = np.mean(hsv[:, :, 1]) / 255.0

                intensity_scores.append({
                    'motion': motion_intensity,
                    'saturation': saturation
                })

            prev_frame = frame.copy()
            sample_count += 1

        cap.release()

        if not intensity_scores:
            return 0.0

        # Combine motion and color intensity
        avg_motion = np.mean([s['motion'] for s in intensity_scores])
        avg_saturation = np.mean([s['saturation'] for s in intensity_scores])

        visual_intensity = (avg_motion * 0.7 + avg_saturation * 0.3)

        return min(visual_intensity, 1.0)

    def _calculate_audio_intensity(self, scene: Dict) -> float:
        """Calculate audio intensity (volume, dynamics)"""
        # Placeholder - requires audio extraction and analysis
        # TODO: Implement with librosa

        # For now, return a default value
        # In full implementation:
        # 1. Extract audio segment for scene
        # 2. Calculate RMS energy
        # 3. Detect peaks and dynamics
        # 4. Return normalized intensity

        return 0.5  # Placeholder

    def _calculate_position_score(self, scene: Dict) -> float:
        """
        Calculate position score based on scene location in video

        Scenes near the middle/end tend to be more important (climax)
        """
        # This requires total video duration
        # For now, estimate based on scene timing

        start_time = scene['start_time']

        # Simple heuristic: scenes later in the video score higher
        # Peak around 60-80% mark (typical climax position)

        # Normalize to 0-1 assuming 2-hour movie (7200 seconds)
        normalized_position = min(start_time / 7200.0, 1.0)

        # Score peaks at 0.7 (70% through the movie)
        position_score = 1.0 - abs(normalized_position - 0.7) / 0.7

        return min(max(position_score, 0.0), 1.0)
```

**Success Criteria:**
- Visual intensity calculation works
- Position scoring logical
- Combined importance score reasonable
- Identifies potential climax scenes

---

## Integration with Backend (Agent 2)

**File:** `src/video_processor/pipeline.py`

```python
from pathlib import Path
import logging
from typing import Dict, List
from .extractor import VideoFrameExtractor
from .scene_detector import SceneDetector
from .keyframe_selector import KeyframeSelector
from .importance_detector import ImportanceDetector

logger = logging.getLogger(__name__)

class VideoProcessingPipeline:
    """Orchestrate complete video processing workflow"""

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        self.extractor = VideoFrameExtractor(str(video_path))
        self.scene_detector = SceneDetector(str(video_path))
        self.keyframe_selector = KeyframeSelector(str(video_path))
        self.importance_detector = ImportanceDetector(str(video_path))

    def process(self, output_dir: Optional[Path] = None) -> Dict:
        """
        Run complete processing pipeline

        Returns:
            Dict with scenes, keyframes, metadata
        """
        logger.info(f"Starting video processing: {self.video_path.name}")

        # 1. Extract metadata
        metadata = {
            'duration': self.extractor.get_duration(),
            'resolution': self.extractor.get_resolution(),
            'fps': self.extractor.get_fps()
        }

        # 2. Detect scenes
        scenes = self.scene_detector.detect_scenes()
        logger.info(f"Detected {len(scenes)} scenes")

        # 3. Select keyframes and analyze importance
        for scene in scenes:
            # Select keyframes
            keyframes = self.keyframe_selector.select_keyframes_from_scene(
                scene,
                num_keyframes=3,
                strategy="uniform"
            )
            scene['keyframes'] = keyframes

            # Analyze importance
            importance = self.importance_detector.analyze_scene(scene)
            scene.update(importance)

            # Save keyframe images if output_dir provided
            if output_dir:
                scene_dir = output_dir / f"scene_{scene['scene_number']}"
                scene_dir.mkdir(parents=True, exist_ok=True)

                for i, kf in enumerate(keyframes):
                    img_path = scene_dir / f"keyframe_{i}.jpg"
                    cv2.imwrite(str(img_path), cv2.cvtColor(kf['frame'], cv2.COLOR_RGB2BGR))
                    kf['image_path'] = str(img_path)

        logger.info("Video processing complete")

        return {
            'metadata': metadata,
            'scenes': scenes,
            'total_keyframes': sum(len(s['keyframes']) for s in scenes)
        }
```

**Integration with Backend:**

Backend triggers processing after upload:
```python
# In backend/app/routers/upload.py, after creating video record:

from src.video_processor.pipeline import VideoProcessingPipeline

# Process video
pipeline = VideoProcessingPipeline(video.file_path)
result = pipeline.process(output_dir=Path("processed") / str(video.id))

# Store scenes in database
for scene_data in result['scenes']:
    scene = Scene(
        video_id=video.id,
        start_time=scene_data['start_time'],
        end_time=scene_data['end_time'],
        duration=scene_data['duration'],
        importance_score=scene_data['importance_score'],
        visual_intensity=scene_data['visual_intensity'],
        audio_intensity=scene_data['audio_intensity']
    )
    db.add(scene)

    # Store keyframes
    for kf_data in scene_data['keyframes']:
        keyframe = Keyframe(
            scene_id=scene.id,
            timestamp=kf_data['timestamp'],
            image_path=kf_data['image_path']
        )
        db.add(keyframe)

db.commit()

# Update video status
video.status = "completed"
video.processing_progress = 100.0
db.commit()
```

## Testing Checklist

- [ ] VideoFrameExtractor extracts frames correctly
- [ ] Can generate thumbnails
- [ ] SceneDetector identifies scene transitions
- [ ] Scene boundaries are accurate
- [ ] KeyframeSelector selects representative frames
- [ ] Visual change detection works
- [ ] ImportanceDetector calculates scores
- [ ] Visual intensity calculation works
- [ ] Pipeline processes entire video end-to-end
- [ ] Results stored in database correctly
- [ ] Performance acceptable for 1-2 hour movies
- [ ] Memory usage reasonable

## Documentation Sub-Agent Deliverables

1. **FFmpeg Guide:**
   - Metadata extraction examples
   - Frame extraction commands
   - Audio extraction examples

2. **PySceneDetect Tutorial:**
   - API usage examples
   - Threshold tuning guide
   - Performance tips

3. **OpenCV Cheat Sheet:**
   - Frame reading examples
   - Histogram analysis code
   - Motion detection examples

4. **Performance Optimization Tips:**
   - Batch processing strategies
   - Memory management
   - Multi-threading approaches

## Success Criteria

Agent 3 is complete when:
1. ✅ All video processor classes implemented
2. ✅ Frame extraction works
3. ✅ Scene detection accurate
4. ✅ Keyframe selection intelligent
5. ✅ Importance scoring reasonable
6. ✅ Pipeline integrates with backend
7. ✅ Results stored in database
8. ✅ Performance acceptable
9. ✅ Code well-documented
10. ✅ Integration tested with test videos

## Estimated Timeline
- Frame extraction: **1-2 hours**
- Scene detection: **2 hours**
- Keyframe selection: **1-2 hours**
- Importance detector: **2-3 hours**
- Integration: **1 hour**
- Testing: **1 hour**

**Total: 8-11 hours**
