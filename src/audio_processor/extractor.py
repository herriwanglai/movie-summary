"""Extract audio from video files"""

import ffmpeg
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class AudioMetadata:
    """Audio metadata"""
    duration: float
    sample_rate: int
    channels: int
    codec: str
    bitrate: Optional[int] = None


class AudioExtractor:
    """Extract audio from video files using FFmpeg"""

    def __init__(self, video_path: str):
        """
        Initialize audio extractor

        Args:
            video_path: Path to video file
        """
        self.video_path = Path(video_path)
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

    def extract_audio(
        self,
        output_path: Optional[str] = None,
        format: str = 'wav',
        sample_rate: int = 16000,
        channels: int = 1
    ) -> str:
        """
        Extract audio from video

        Args:
            output_path: Output file path (auto-generated if None)
            format: Output format ('wav', 'mp3', 'flac')
            sample_rate: Sample rate in Hz (16000 recommended for Whisper)
            channels: Number of channels (1=mono, 2=stereo)

        Returns:
            Path to extracted audio file
        """
        if output_path is None:
            output_path = self.video_path.with_suffix(f'.{format}')
        else:
            output_path = Path(output_path)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Extract audio using ffmpeg
        try:
            stream = ffmpeg.input(str(self.video_path))
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec='pcm_s16le' if format == 'wav' else None,
                ac=channels,
                ar=sample_rate,
                loglevel='error'
            )
            ffmpeg.run(stream, overwrite_output=True)
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")

        return str(output_path)

    def extract_audio_segment(
        self,
        start_time: float,
        end_time: float,
        output_path: Optional[str] = None,
        format: str = 'wav',
        sample_rate: int = 16000
    ) -> str:
        """
        Extract audio segment from video

        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output file path
            format: Output format
            sample_rate: Sample rate in Hz

        Returns:
            Path to extracted audio file
        """
        if output_path is None:
            output_path = self.video_path.parent / f"segment_{start_time}_{end_time}.{format}"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        duration = end_time - start_time

        try:
            stream = ffmpeg.input(str(self.video_path), ss=start_time, t=duration)
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec='pcm_s16le' if format == 'wav' else None,
                ar=sample_rate,
                loglevel='error'
            )
            ffmpeg.run(stream, overwrite_output=True)
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to extract audio segment: {e.stderr.decode()}")

        return str(output_path)

    def get_audio_metadata(self) -> AudioMetadata:
        """
        Get audio metadata from video

        Returns:
            AudioMetadata object
        """
        try:
            probe = ffmpeg.probe(str(self.video_path))
            audio_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'audio'),
                None
            )

            if not audio_stream:
                raise ValueError("No audio stream found in video")

            return AudioMetadata(
                duration=float(probe['format'].get('duration', 0)),
                sample_rate=int(audio_stream.get('sample_rate', 0)),
                channels=int(audio_stream.get('channels', 0)),
                codec=audio_stream.get('codec_name', 'unknown'),
                bitrate=int(audio_stream.get('bit_rate', 0)) if 'bit_rate' in audio_stream else None
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to get audio metadata: {e.stderr.decode()}")
