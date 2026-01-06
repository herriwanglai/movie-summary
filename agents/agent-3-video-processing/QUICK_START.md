# Video Processing Pipeline - Quick Start Guide

## Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install FFmpeg (system dependency)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

## Verification

```bash
# Run verification to check everything is set up
python src/video_processor/verify_pipeline.py
```

Expected output:
```
✓ All dependencies installed!
✓ All video processor modules can be imported!
✓ FFmpeg installed
✓ Basic functionality test passed!
✓ ALL CHECKS PASSED!
```

## Basic Usage

### 1. Simple Video Processing

```python
from src.video_processor import VideoProcessingPipeline

# Process a video
pipeline = VideoProcessingPipeline("movie.mp4")
results = pipeline.process(
    output_dir="output",
    keyframes_per_scene=3,
    keyframe_method="distributed"
)

# Results contain:
# - metadata: video info (duration, fps, resolution)
# - scenes: list of detected scenes
# - keyframes: list of extracted keyframes
# - scene_stats: statistics about scenes
```

### 2. Extract Frames

```python
from src.video_processor import VideoFrameExtractor

extractor = VideoFrameExtractor("movie.mp4")

# Get video metadata
print(f"Duration: {extractor.metadata.duration}s")
print(f"Resolution: {extractor.metadata.width}x{extractor.metadata.height}")

# Extract frame at 5 seconds
frame = extractor.extract_at_timestamp(5.0)
frame.save("frame_5s.jpg")

# Extract frames every 10 seconds
frames = extractor.extract_frames_interval(interval_seconds=10.0)
print(f"Extracted {len(frames)} frames")
```

### 3. Detect Scenes

```python
from src.video_processor import SceneDetector

detector = SceneDetector("movie.mp4", threshold=27.0)
scenes = detector.detect_scenes()

for scene in scenes:
    print(f"Scene {scene.scene_number}: {scene.start_time:.2f}s - {scene.end_time:.2f}s")

# Get statistics
stats = detector.get_scene_stats(scenes)
print(f"Average scene duration: {stats['average_scene_duration']:.2f}s")
```

### 4. Select Keyframes

```python
from src.video_processor import VideoFrameExtractor, SceneDetector, KeyframeSelector

extractor = VideoFrameExtractor("movie.mp4")
detector = SceneDetector("movie.mp4")
selector = KeyframeSelector(extractor)

scenes = detector.detect_scenes()

# Select keyframes using different methods
keyframes = selector.select_from_scenes(
    scenes,
    keyframes_per_scene=3,
    method="distributed"  # Options: middle, first, last, distributed, variance
)

# Save keyframes
saved_paths = selector.save_keyframes(keyframes, "output/keyframes")
```

### 5. Analyze Scene Importance

```python
from src.video_processor import VideoFrameExtractor, SceneDetector, ImportanceDetector
from src.audio_processor import AudioExtractor, Transcriber

# Setup
extractor = VideoFrameExtractor("movie.mp4")
detector = SceneDetector("movie.mp4")
scenes = detector.detect_scenes()

# Get transcript
audio_ext = AudioExtractor("movie.mp4")
audio_ext.extract_audio("audio.wav")
transcriber = Transcriber()
transcript = transcriber.transcribe("audio.wav")

# Analyze importance
importance = ImportanceDetector(extractor, scenes, transcript)
top_scenes = importance.get_top_scenes(n=10)

for scene_imp in top_scenes:
    print(f"Scene {scene_imp.scene_number}:")
    print(f"  Score: {scene_imp.importance_score:.2f}")
    print(f"  Categories: {', '.join(scene_imp.categories)}")
    print(f"  Visual: {scene_imp.visual_intensity:.2f}")
    print(f"  Audio: {scene_imp.audio_intensity:.2f}")
```

## Run Demo

```bash
# Run comprehensive demo with synthetic test video
python src/video_processor/demo_pipeline.py
```

This will:
1. Create test videos
2. Demonstrate frame extraction
3. Demonstrate scene detection
4. Demonstrate keyframe selection
5. Run complete pipeline
6. Save outputs to `/tmp/pipeline_output/`

## API Quick Reference

### VideoFrameExtractor
```python
extractor = VideoFrameExtractor(video_path, max_resolution=1920)
frame = extractor.extract_at_timestamp(timestamp)
frames = extractor.extract_frames_interval(interval_seconds=2.0)
metadata = extractor.metadata  # .duration, .fps, .width, .height
```

### SceneDetector
```python
detector = SceneDetector(video_path, threshold=27.0, min_scene_length=1.0)
scenes = detector.detect_scenes()  # List[Scene]
stats = detector.get_scene_stats(scenes)
```

### KeyframeSelector
```python
selector = KeyframeSelector(video_extractor)
keyframes = selector.select_from_scenes(scenes, keyframes_per_scene=3, method="distributed")
# Methods: "middle", "first", "last", "distributed", "variance"
```

### VideoProcessingPipeline
```python
pipeline = VideoProcessingPipeline(video_path)
results = pipeline.process(
    output_dir="output",
    keyframes_per_scene=3,
    keyframe_method="distributed",
    save_keyframes=True
)
```

## Configuration Options

### Scene Detection Threshold
- **Lower** (15-25): More sensitive, detects subtle changes, more scenes
- **Default** (27): Balanced
- **Higher** (30-40): Less sensitive, only major changes, fewer scenes

### Keyframe Selection Methods
- **middle**: Single frame from middle of scene (fast, reliable)
- **first**: First frame of scene
- **last**: Last frame of scene
- **distributed**: Evenly spaced frames (good coverage)
- **variance**: Frames with highest visual variance (most interesting)

## Troubleshooting

### "Video file not found"
- Check file path is correct
- Use absolute paths or ensure working directory is correct

### "Cannot open video file"
- FFmpeg may not support the codec
- Try converting with: `ffmpeg -i input.mp4 -c:v libx264 output.mp4`

### "No module named cv2"
- Install OpenCV: `pip install opencv-python`

### "FFmpeg not found"
- Install FFmpeg system-wide
- Add FFmpeg to PATH

### Scene detection not working well
- Adjust threshold (try 20-30 range)
- Increase min_scene_length for longer scenes
- Check video quality (low quality = harder detection)

## Performance Tips

1. **Use max_resolution** for faster processing:
   ```python
   extractor = VideoFrameExtractor("movie.mp4", max_resolution=1280)
   ```

2. **Adjust scene detection threshold** for faster/slower detection

3. **Use 'middle' keyframe method** for fastest processing

4. **Process in chunks** for very long videos (>3 hours)

## Next Steps

- See `SKILLS.md` for detailed technical documentation
- See `COMPLETION_REPORT.md` for full implementation details
- Check `src/orchestrator/pipeline.py` for full movie analysis pipeline
- Integrate with backend via `MovieAnalysisPipeline`
