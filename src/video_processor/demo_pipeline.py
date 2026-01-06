#!/usr/bin/env python3
"""
Demo script for video processing pipeline

Creates a test video and processes it through the complete pipeline
"""

import sys
import logging
from pathlib import Path
import json
import cv2
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.video_processor import VideoProcessingPipeline

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_test_video(output_path: Path, duration: int = 30) -> Path:
    """
    Create a test video with scene changes

    Args:
        output_path: Path to save video
        duration: Duration in seconds

    Returns:
        Path to created video
    """
    logger.info(f"Creating test video: {output_path}")

    # Video settings
    fps = 30
    width, height = 1280, 720
    total_frames = duration * fps

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    # Generate frames with distinct scenes
    scene_duration = 5  # seconds per scene
    frames_per_scene = scene_duration * fps

    for i in range(total_frames):
        # Determine which scene we're in
        scene_num = i // frames_per_scene
        frame_in_scene = i % frames_per_scene

        # Create frame with different colors per scene
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        if scene_num == 0:
            # Scene 1: Blue gradient
            frame[:, :, 0] = 255  # Blue channel
            frame[:, :, 1] = int((frame_in_scene / frames_per_scene) * 255)
        elif scene_num == 1:
            # Scene 2: Green gradient
            frame[:, :, 1] = 255  # Green channel
            frame[:, :, 2] = int((frame_in_scene / frames_per_scene) * 255)
        elif scene_num == 2:
            # Scene 3: Red gradient
            frame[:, :, 2] = 255  # Red channel
            frame[:, :, 0] = int((frame_in_scene / frames_per_scene) * 255)
        elif scene_num == 3:
            # Scene 4: Yellow gradient
            frame[:, :, 1] = 255  # Green
            frame[:, :, 2] = 255  # Red
            frame[:, :, 0] = int((frame_in_scene / frames_per_scene) * 255)
        elif scene_num == 4:
            # Scene 5: Cyan gradient
            frame[:, :, 0] = 255  # Blue
            frame[:, :, 1] = 255  # Green
            frame[:, :, 2] = int((frame_in_scene / frames_per_scene) * 255)
        else:
            # Scene 6: Magenta gradient
            frame[:, :, 0] = 255  # Blue
            frame[:, :, 2] = 255  # Red
            frame[:, :, 1] = int((frame_in_scene / frames_per_scene) * 255)

        # Add text overlay
        timestamp = i / fps
        text = f"Scene {scene_num + 1} | Time: {timestamp:.2f}s | Frame: {i}"
        cv2.putText(
            frame, text,
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            3
        )

        # Add scene number in center
        cv2.putText(
            frame,
            f"SCENE {scene_num + 1}",
            (width // 2 - 200, height // 2),
            cv2.FONT_HERSHEY_BOLD,
            3,
            (255, 255, 255),
            5
        )

        out.write(frame)

    out.release()
    logger.info(f"✓ Created test video: {output_path} ({duration}s, {total_frames} frames)")

    return output_path


def demo_basic_extraction():
    """Demo: Basic frame extraction"""
    logger.info("\n" + "="*60)
    logger.info("DEMO 1: Basic Frame Extraction")
    logger.info("="*60)

    # Create test video
    test_video = Path("/tmp/test_video_demo.mp4")
    create_test_video(test_video, duration=10)

    try:
        from src.video_processor import VideoFrameExtractor

        # Initialize extractor
        extractor = VideoFrameExtractor(str(test_video))

        # Extract metadata
        logger.info(f"\nVideo Metadata:")
        logger.info(f"  Duration: {extractor.metadata.duration:.2f}s")
        logger.info(f"  FPS: {extractor.metadata.fps:.2f}")
        logger.info(f"  Resolution: {extractor.metadata.width}x{extractor.metadata.height}")
        logger.info(f"  Frames: {extractor.metadata.frame_count}")

        # Extract frame at 5 seconds
        logger.info(f"\nExtracting frame at 5.0s...")
        frame = extractor.extract_at_timestamp(5.0)
        if frame:
            logger.info(f"✓ Extracted frame #{frame.frame_number} at {frame.timestamp:.2f}s")

        # Extract frames at 2-second intervals
        logger.info(f"\nExtracting frames at 2s intervals...")
        frames = extractor.extract_frames_interval(interval_seconds=2.0)
        logger.info(f"✓ Extracted {len(frames)} frames")

        logger.info("\n✓ Demo 1 complete!")

    finally:
        if test_video.exists():
            test_video.unlink()


def demo_scene_detection():
    """Demo: Scene detection"""
    logger.info("\n" + "="*60)
    logger.info("DEMO 2: Scene Detection")
    logger.info("="*60)

    # Create test video with clear scene changes
    test_video = Path("/tmp/test_video_scenes.mp4")
    create_test_video(test_video, duration=30)

    try:
        from src.video_processor import SceneDetector

        # Initialize detector
        detector = SceneDetector(str(test_video), threshold=20.0)

        # Detect scenes
        logger.info("\nDetecting scenes...")
        scenes = detector.detect_scenes()

        logger.info(f"\n✓ Detected {len(scenes)} scenes:")
        for scene in scenes:
            logger.info(f"  {scene}")

        # Get statistics
        stats = detector.get_scene_stats(scenes)
        logger.info(f"\nScene Statistics:")
        logger.info(f"  Total scenes: {stats['total_scenes']}")
        logger.info(f"  Average duration: {stats['average_scene_duration']:.2f}s")
        logger.info(f"  Shortest scene: {stats['shortest_scene']:.2f}s")
        logger.info(f"  Longest scene: {stats['longest_scene']:.2f}s")

        logger.info("\n✓ Demo 2 complete!")

    finally:
        if test_video.exists():
            test_video.unlink()


def demo_keyframe_selection():
    """Demo: Keyframe selection"""
    logger.info("\n" + "="*60)
    logger.info("DEMO 3: Keyframe Selection")
    logger.info("="*60)

    # Create test video
    test_video = Path("/tmp/test_video_keyframes.mp4")
    create_test_video(test_video, duration=20)

    try:
        from src.video_processor import VideoFrameExtractor, SceneDetector, KeyframeSelector

        # Setup
        extractor = VideoFrameExtractor(str(test_video))
        detector = SceneDetector(str(test_video), threshold=20.0)
        selector = KeyframeSelector(extractor)

        # Detect scenes
        scenes = detector.detect_scenes()
        logger.info(f"\nDetected {len(scenes)} scenes")

        # Select keyframes using different methods
        methods = ['middle', 'first', 'last', 'distributed']

        for method in methods:
            keyframes = selector.select_from_scenes(
                scenes,
                keyframes_per_scene=1 if method != 'distributed' else 3,
                method=method
            )
            logger.info(f"\n{method.upper()} method: {len(keyframes)} keyframes")
            for kf in keyframes[:3]:  # Show first 3
                logger.info(f"  Scene {kf.scene_number}: "
                          f"frame #{kf.frame.frame_number} "
                          f"at {kf.frame.timestamp:.2f}s "
                          f"({kf.keyframe_type})")

        logger.info("\n✓ Demo 3 complete!")

    finally:
        if test_video.exists():
            test_video.unlink()


def demo_full_pipeline():
    """Demo: Complete video processing pipeline"""
    logger.info("\n" + "="*60)
    logger.info("DEMO 4: Complete Video Processing Pipeline")
    logger.info("="*60)

    # Create test video
    test_video = Path("/tmp/test_video_pipeline.mp4")
    create_test_video(test_video, duration=30)

    output_dir = Path("/tmp/pipeline_output")
    output_dir.mkdir(exist_ok=True)

    try:
        # Initialize pipeline
        logger.info("\nInitializing pipeline...")
        pipeline = VideoProcessingPipeline(str(test_video))

        # Process video
        logger.info("\nProcessing video...")
        results = pipeline.process(
            output_dir=output_dir,
            keyframes_per_scene=3,
            keyframe_method="distributed",
            save_keyframes=True
        )

        # Display results
        logger.info("\n" + "="*60)
        logger.info("PROCESSING RESULTS")
        logger.info("="*60)

        logger.info("\nMetadata:")
        for key, value in results['metadata'].items():
            logger.info(f"  {key}: {value}")

        logger.info(f"\nScenes: {len(results['scenes'])}")
        logger.info(f"Keyframes: {results['total_keyframes']}")

        logger.info("\nScene Details:")
        for scene in results['scenes'][:3]:  # Show first 3
            logger.info(f"  Scene {scene['scene_number']}: "
                       f"{scene['start_time']:.2f}s - {scene['end_time']:.2f}s "
                       f"({scene['duration']:.2f}s)")

        logger.info("\nKeyframe Details:")
        for kf in results['keyframes'][:5]:  # Show first 5
            logger.info(f"  Scene {kf['scene_number']}: "
                       f"frame #{kf['frame_number']} "
                       f"at {kf['timestamp']:.2f}s "
                       f"({kf['keyframe_type']})")

        # Save results to JSON
        results_file = output_dir / "results.json"
        # Remove numpy arrays before saving
        serializable_results = {
            'metadata': results['metadata'],
            'scenes': results['scenes'],
            'scene_stats': results['scene_stats'],
            'keyframes': results['keyframes'],
            'total_keyframes': results['total_keyframes'],
            'processing_summary': results['processing_summary']
        }

        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)

        logger.info(f"\n✓ Results saved to: {results_file}")

        # Generate thumbnail
        logger.info("\nGenerating thumbnail...")
        thumbnail_path = output_dir / "thumbnail.jpg"
        pipeline.generate_thumbnail(str(thumbnail_path))
        logger.info(f"✓ Thumbnail saved to: {thumbnail_path}")

        logger.info("\n" + "="*60)
        logger.info("✓ DEMO 4 COMPLETE!")
        logger.info(f"✓ Output directory: {output_dir}")
        logger.info("="*60)

    finally:
        if test_video.exists():
            test_video.unlink()
        # Keep output_dir for inspection


def main():
    """Run all demos"""
    logger.info("\n" + "="*70)
    logger.info("VIDEO PROCESSING PIPELINE DEMONSTRATION")
    logger.info("="*70)

    try:
        demo_basic_extraction()
        demo_scene_detection()
        demo_keyframe_selection()
        demo_full_pipeline()

        logger.info("\n" + "="*70)
        logger.info("✓ ALL DEMOS COMPLETED SUCCESSFULLY!")
        logger.info("="*70)
        logger.info("\nCheck /tmp/pipeline_output/ for sample outputs")

        return 0

    except Exception as e:
        logger.error(f"\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
