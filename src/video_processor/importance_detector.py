"""Enhanced scene analysis to identify important moments"""

import numpy as np
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

from ..video_processor.extractor import VideoFrameExtractor, Frame
from ..video_processor.scene_detector import Scene
from ..audio_processor.transcriber import Transcript


@dataclass
class SceneImportance:
    """Scene importance analysis"""
    scene_number: int
    importance_score: float
    reasons: List[str]
    categories: List[str]  # 'action', 'dialogue_heavy', 'emotional', 'climax'
    audio_intensity: float
    visual_intensity: float
    dialogue_density: float


class ImportanceDetector:
    """Detect important/exciting scenes before AI analysis"""

    def __init__(
        self,
        video_extractor: VideoFrameExtractor,
        scenes: List[Scene],
        transcript: Transcript
    ):
        """
        Initialize importance detector

        Args:
            video_extractor: VideoFrameExtractor instance
            scenes: List of detected scenes
            transcript: Movie transcript
        """
        self.extractor = video_extractor
        self.scenes = scenes
        self.transcript = transcript

    def analyze_all_scenes(self) -> List[SceneImportance]:
        """
        Analyze all scenes for importance

        Returns:
            List of SceneImportance objects sorted by importance
        """
        scene_analyses = []

        for scene in self.scenes:
            analysis = self.analyze_scene(scene)
            scene_analyses.append(analysis)

        # Sort by importance score
        scene_analyses.sort(key=lambda x: x.importance_score, reverse=True)

        return scene_analyses

    def analyze_scene(self, scene: Scene) -> SceneImportance:
        """Analyze a single scene for importance"""

        # 1. Visual intensity (motion, brightness changes)
        visual_intensity = self._calculate_visual_intensity(scene)

        # 2. Audio intensity (from transcript timing)
        audio_intensity = self._calculate_audio_intensity(scene)

        # 3. Dialogue density
        dialogue_density = self._calculate_dialogue_density(scene)

        # 4. Dialogue content analysis
        dialogue_importance = self._analyze_dialogue_content(scene)

        # 5. Position in movie (climax typically at 75-90%)
        position_score = self._calculate_position_score(scene)

        # Combine scores
        importance_score = (
            visual_intensity * 0.25 +
            audio_intensity * 0.20 +
            dialogue_density * 0.15 +
            dialogue_importance * 0.25 +
            position_score * 0.15
        )

        # Categorize scene
        categories = self._categorize_scene(
            visual_intensity,
            audio_intensity,
            dialogue_density
        )

        # Generate reasons
        reasons = self._generate_reasons(
            visual_intensity,
            audio_intensity,
            dialogue_density,
            dialogue_importance,
            position_score
        )

        return SceneImportance(
            scene_number=scene.scene_number,
            importance_score=importance_score,
            reasons=reasons,
            categories=categories,
            audio_intensity=audio_intensity,
            visual_intensity=visual_intensity,
            dialogue_density=dialogue_density
        )

    def _calculate_visual_intensity(self, scene: Scene) -> float:
        """
        Calculate visual intensity (motion, brightness changes)

        High intensity suggests action scenes
        """
        # Sample frames from the scene
        num_samples = min(10, int(scene.duration * self.extractor.metadata.fps / 10))
        if num_samples < 2:
            return 0.5

        frame_step = (scene.end_frame - scene.start_frame) // num_samples
        frames = []

        for i in range(num_samples):
            frame_num = scene.start_frame + i * frame_step
            frame = self.extractor.extract_frame(frame_num)
            if frame:
                frames.append(frame.image)

        if len(frames) < 2:
            return 0.5

        # Calculate frame differences (motion)
        diffs = []
        for i in range(len(frames) - 1):
            diff = np.mean(np.abs(frames[i].astype(float) - frames[i+1].astype(float)))
            diffs.append(diff)

        avg_diff = np.mean(diffs)

        # Normalize (typical values: 5-50 for static, 50-150 for action)
        normalized = min(1.0, avg_diff / 100.0)

        return normalized

    def _calculate_audio_intensity(self, scene: Scene) -> float:
        """
        Calculate audio intensity from dialogue timing

        Short gaps between dialogue = high intensity
        """
        # Get dialogue segments in this scene
        segments = [
            seg for seg in self.transcript.segments
            if seg.start >= scene.start_time and seg.end <= scene.end_time
        ]

        if not segments:
            return 0.3  # Low score for silent scenes

        # Calculate gaps between dialogue
        gaps = []
        for i in range(len(segments) - 1):
            gap = segments[i+1].start - segments[i].end
            gaps.append(gap)

        if gaps:
            avg_gap = np.mean(gaps)
            # Short gaps = high intensity
            # Normalize: 0.5s gap = 1.0, 3s gap = 0.0
            intensity = max(0.0, 1.0 - (avg_gap / 3.0))
        else:
            intensity = 0.5

        return intensity

    def _calculate_dialogue_density(self, scene: Scene) -> float:
        """Calculate how dialogue-heavy the scene is"""
        if scene.duration == 0:
            return 0.0

        # Get transcript text for this scene
        text = self.transcript.get_text_in_range(scene.start_time, scene.end_time)

        # Words per minute
        word_count = len(text.split())
        duration_minutes = scene.duration / 60.0

        if duration_minutes == 0:
            return 0.0

        wpm = word_count / duration_minutes

        # Normalize: 100 wpm = 0.5, 200+ wpm = 1.0
        normalized = min(1.0, wpm / 200.0)

        return normalized

    def _analyze_dialogue_content(self, scene: Scene) -> float:
        """
        Analyze dialogue content for importance signals

        Keywords that suggest important scenes
        """
        text = self.transcript.get_text_in_range(
            scene.start_time,
            scene.end_time
        ).lower()

        # Keywords indicating important moments
        importance_keywords = {
            # Emotional intensity
            'love', 'hate', 'kill', 'die', 'dead', 'sorry', 'please',
            # Conflict
            'fight', 'war', 'battle', 'attack', 'stop', 'help',
            # Revelation
            'truth', 'secret', 'know', 'remember', 'realize', 'understand',
            # Character names repeated (confrontation)
            # Exclamations
            'no!', 'yes!', 'why', 'how', 'what',
            # Climactic
            'final', 'end', 'last', 'finish', 'over',
            # Relationship
            'father', 'mother', 'son', 'daughter', 'brother', 'sister',
            'friend', 'family'
        }

        # Count keyword occurrences
        keyword_count = sum(1 for keyword in importance_keywords if keyword in text)

        # Also check for ALL CAPS (shouting in subtitles)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(1, len(text))

        # Exclamation marks and question marks
        emotion_marks = text.count('!') + text.count('?')

        # Combine signals
        keyword_score = min(1.0, keyword_count / 5.0)
        caps_score = min(1.0, caps_ratio * 10.0)
        emotion_score = min(1.0, emotion_marks / 10.0)

        importance = (keyword_score * 0.5 + caps_score * 0.25 + emotion_score * 0.25)

        return importance

    def _calculate_position_score(self, scene: Scene) -> float:
        """
        Score based on position in movie

        Key moments typically at:
        - 25% (end of Act 1)
        - 50% (midpoint)
        - 75% (end of Act 2 / all is lost)
        - 90% (climax)
        """
        total_duration = self.scenes[-1].end_time if self.scenes else 1.0
        position = scene.start_time / total_duration

        # Key structural points
        key_points = [0.10, 0.25, 0.50, 0.75, 0.90]

        # Find distance to nearest key point
        min_distance = min(abs(position - kp) for kp in key_points)

        # Closer to key point = higher score
        # Within 5% of key point gets max score
        if min_distance < 0.05:
            score = 1.0
        elif min_distance < 0.10:
            score = 0.7
        elif min_distance < 0.15:
            score = 0.4
        else:
            score = 0.2

        # Boost for climax region (75-95%)
        if 0.75 <= position <= 0.95:
            score = max(score, 0.8)

        return score

    def _categorize_scene(
        self,
        visual_intensity: float,
        audio_intensity: float,
        dialogue_density: float
    ) -> List[str]:
        """Categorize the scene type"""
        categories = []

        if visual_intensity > 0.7:
            categories.append('action')

        if audio_intensity > 0.7:
            categories.append('intense')

        if dialogue_density > 0.7:
            categories.append('dialogue_heavy')

        if visual_intensity > 0.6 and audio_intensity > 0.6:
            categories.append('exciting')

        if visual_intensity < 0.3 and audio_intensity < 0.3:
            categories.append('quiet')

        if not categories:
            categories.append('neutral')

        return categories

    def _generate_reasons(
        self,
        visual_intensity: float,
        audio_intensity: float,
        dialogue_density: float,
        dialogue_importance: float,
        position_score: float
    ) -> List[str]:
        """Generate human-readable reasons for importance"""
        reasons = []

        if visual_intensity > 0.7:
            reasons.append("High visual intensity - likely action sequence")

        if audio_intensity > 0.7:
            reasons.append("Rapid dialogue pacing - intense conversation")

        if dialogue_importance > 0.7:
            reasons.append("Important dialogue keywords detected")

        if dialogue_density > 0.7:
            reasons.append("Dialogue-heavy scene - character development")

        if position_score > 0.8:
            reasons.append("At key structural position in movie")

        if not reasons:
            reasons.append("Standard scene")

        return reasons

    def get_top_scenes(self, n: int = 10) -> List[SceneImportance]:
        """
        Get top N most important scenes

        Args:
            n: Number of scenes to return

        Returns:
            List of top N SceneImportance objects
        """
        all_analyses = self.analyze_all_scenes()
        return all_analyses[:n]

    def get_scenes_by_category(self, category: str) -> List[SceneImportance]:
        """Get all scenes of a specific category"""
        all_analyses = self.analyze_all_scenes()
        return [s for s in all_analyses if category in s.categories]

    def generate_importance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive importance report"""
        all_analyses = self.analyze_all_scenes()

        return {
            "total_scenes": len(all_analyses),
            "top_10_scenes": [
                {
                    "scene": s.scene_number,
                    "score": s.importance_score,
                    "categories": s.categories,
                    "reasons": s.reasons
                }
                for s in all_analyses[:10]
            ],
            "scene_distribution": {
                "action": len([s for s in all_analyses if 'action' in s.categories]),
                "exciting": len([s for s in all_analyses if 'exciting' in s.categories]),
                "dialogue_heavy": len([s for s in all_analyses if 'dialogue_heavy' in s.categories]),
                "quiet": len([s for s in all_analyses if 'quiet' in s.categories])
            },
            "average_scores": {
                "visual_intensity": np.mean([s.visual_intensity for s in all_analyses]),
                "audio_intensity": np.mean([s.audio_intensity for s in all_analyses]),
                "dialogue_density": np.mean([s.dialogue_density for s in all_analyses])
            }
        }
