#!/usr/bin/env python3
"""
Verification script for video processing pipeline

Tests all components and their dependencies
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required dependencies are installed"""
    logger.info("Checking dependencies...")

    dependencies = {
        'cv2': 'opencv-python',
        'scenedetect': 'scenedetect',
        'ffmpeg': 'ffmpeg-python',
        'numpy': 'numpy',
        'PIL': 'Pillow'
    }

    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            logger.info(f"✓ {package} ({module}) - OK")
        except ImportError:
            logger.error(f"✗ {package} ({module}) - MISSING")
            missing.append(package)

    if missing:
        logger.error(f"\nMissing dependencies: {', '.join(missing)}")
        logger.error("Install with: pip install " + " ".join(missing))
        return False

    logger.info("\n✓ All dependencies installed!")
    return True


def check_imports():
    """Check if all video processor modules can be imported"""
    logger.info("\nChecking video processor imports...")

    modules = [
        ('VideoFrameExtractor', 'Frame extraction'),
        ('SceneDetector', 'Scene detection'),
        ('KeyframeSelector', 'Keyframe selection'),
        ('ImportanceDetector', 'Importance detection'),
        ('VideoProcessingPipeline', 'Pipeline orchestration')
    ]

    all_ok = True
    for module_name, description in modules:
        try:
            exec(f"from src.video_processor import {module_name}")
            logger.info(f"✓ {module_name} - {description} - OK")
        except ImportError as e:
            logger.error(f"✗ {module_name} - {description} - FAILED: {e}")
            all_ok = False

    if all_ok:
        logger.info("\n✓ All video processor modules can be imported!")
    else:
        logger.error("\n✗ Some modules failed to import")

    return all_ok


def check_ffmpeg():
    """Check if FFmpeg is installed on the system"""
    logger.info("\nChecking FFmpeg installation...")

    import subprocess

    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            logger.info(f"✓ FFmpeg installed: {version_line}")
            return True
        else:
            logger.error("✗ FFmpeg command failed")
            return False
    except FileNotFoundError:
        logger.error("✗ FFmpeg not found in PATH")
        logger.error("Install FFmpeg: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        logger.error(f"✗ Error checking FFmpeg: {e}")
        return False


def run_basic_test():
    """Run a basic functionality test"""
    logger.info("\nRunning basic functionality test...")

    try:
        import numpy as np
        import cv2
        from scenedetect import open_video

        # Create a simple test video in memory
        logger.info("Testing OpenCV video creation...")
        test_video_path = Path('/tmp/test_video_verification.mp4')

        # Create a simple 5-second test video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            str(test_video_path),
            fourcc,
            30.0,
            (640, 480)
        )

        # Generate 150 frames (5 seconds at 30fps)
        for i in range(150):
            # Create a frame with changing colors
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame[:, :] = (i % 255, (i * 2) % 255, (i * 3) % 255)

            # Add frame number text
            cv2.putText(
                frame,
                f"Frame {i}",
                (50, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                3
            )

            out.write(frame)

        out.release()
        logger.info(f"✓ Created test video: {test_video_path}")

        # Test video can be opened
        cap = cv2.VideoCapture(str(test_video_path))
        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            logger.info(f"✓ Test video readable: {frame_count} frames at {fps}fps")
        else:
            logger.error("✗ Failed to open test video")
            return False

        # Clean up
        if test_video_path.exists():
            test_video_path.unlink()
            logger.info("✓ Cleaned up test video")

        logger.info("\n✓ Basic functionality test passed!")
        return True

    except Exception as e:
        logger.error(f"\n✗ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification checks"""
    logger.info("="*60)
    logger.info("VIDEO PROCESSING PIPELINE VERIFICATION")
    logger.info("="*60)

    results = {
        'dependencies': check_dependencies(),
        'imports': check_imports(),
        'ffmpeg': check_ffmpeg(),
        'basic_test': run_basic_test()
    }

    logger.info("\n" + "="*60)
    logger.info("VERIFICATION SUMMARY")
    logger.info("="*60)

    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{check.upper()}: {status}")
        if not passed:
            all_passed = False

    logger.info("="*60)

    if all_passed:
        logger.info("\n✓ ALL CHECKS PASSED! Video processing pipeline is ready.")
        return 0
    else:
        logger.error("\n✗ SOME CHECKS FAILED. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
