"""Transcribe audio using Whisper"""

import whisper
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class TranscriptSegment:
    """Represents a segment of transcribed audio"""
    id: int
    start: float
    end: float
    text: str
    confidence: Optional[float] = None
    speaker: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "confidence": self.confidence,
            "speaker": self.speaker
        }


@dataclass
class Transcript:
    """Complete transcript with metadata"""
    segments: List[TranscriptSegment]
    language: str
    duration: float
    full_text: str

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "segments": [seg.to_dict() for seg in self.segments],
            "language": self.language,
            "duration": self.duration,
            "full_text": self.full_text
        }

    def save_json(self, output_path: str) -> None:
        """Save transcript as JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def save_srt(self, output_path: str) -> None:
        """Save transcript as SRT subtitle file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for seg in self.segments:
                f.write(f"{seg.id}\n")
                f.write(f"{self._format_timestamp(seg.start)} --> {self._format_timestamp(seg.end)}\n")
                f.write(f"{seg.text}\n\n")

    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp for SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def get_text_at_time(self, timestamp: float) -> Optional[str]:
        """Get transcript text at specific timestamp"""
        for seg in self.segments:
            if seg.start <= timestamp <= seg.end:
                return seg.text
        return None

    def get_text_in_range(self, start: float, end: float) -> str:
        """Get transcript text in time range"""
        texts = []
        for seg in self.segments:
            # Check if segment overlaps with range
            if seg.start <= end and seg.end >= start:
                texts.append(seg.text)
        return " ".join(texts)

    def search(self, query: str, case_sensitive: bool = False) -> List[TranscriptSegment]:
        """Search for text in transcript"""
        results = []
        search_query = query if case_sensitive else query.lower()

        for seg in self.segments:
            search_text = seg.text if case_sensitive else seg.text.lower()
            if search_query in search_text:
                results.append(seg)

        return results


class Transcriber:
    """Transcribe audio using OpenAI Whisper"""

    def __init__(
        self,
        model_name: str = "base",
        device: Optional[str] = None,
        language: Optional[str] = None
    ):
        """
        Initialize transcriber

        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
            device: Device to use ('cuda' or 'cpu', auto-detected if None)
            language: Language code (None for auto-detection)
        """
        self.model_name = model_name
        self.device = device
        self.language = language
        self.model = None

    def _load_model(self):
        """Load Whisper model (lazy loading)"""
        if self.model is None:
            self.model = whisper.load_model(self.model_name, device=self.device)

    def transcribe(
        self,
        audio_path: str,
        task: str = "transcribe",
        verbose: bool = False
    ) -> Transcript:
        """
        Transcribe audio file

        Args:
            audio_path: Path to audio file
            task: 'transcribe' or 'translate' (to English)
            verbose: Show progress

        Returns:
            Transcript object
        """
        self._load_model()

        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Transcribe
        result = self.model.transcribe(
            str(audio_path),
            task=task,
            language=self.language,
            verbose=verbose
        )

        # Convert to TranscriptSegment objects
        segments = []
        for idx, seg in enumerate(result['segments']):
            segments.append(TranscriptSegment(
                id=idx + 1,
                start=seg['start'],
                end=seg['end'],
                text=seg['text'].strip(),
                confidence=seg.get('confidence')
            ))

        # Calculate total duration
        duration = segments[-1].end if segments else 0.0

        # Create full text
        full_text = " ".join(seg.text for seg in segments)

        return Transcript(
            segments=segments,
            language=result['language'],
            duration=duration,
            full_text=full_text
        )

    def transcribe_segment(
        self,
        audio_path: str,
        start_time: float,
        end_time: float
    ) -> Transcript:
        """
        Transcribe audio segment

        Args:
            audio_path: Path to audio file
            start_time: Start time in seconds
            end_time: End time in seconds

        Returns:
            Transcript object
        """
        # Note: For segment transcription, you might want to extract the audio
        # segment first using AudioExtractor, or use faster-whisper which
        # supports seeking
        return self.transcribe(audio_path)

    @staticmethod
    def load_transcript(json_path: str) -> Transcript:
        """
        Load transcript from JSON file

        Args:
            json_path: Path to JSON file

        Returns:
            Transcript object
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        segments = [
            TranscriptSegment(**seg) for seg in data['segments']
        ]

        return Transcript(
            segments=segments,
            language=data['language'],
            duration=data['duration'],
            full_text=data['full_text']
        )
