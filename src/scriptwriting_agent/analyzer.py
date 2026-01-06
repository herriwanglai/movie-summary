"""Scriptwriting analyzer with expert analysis capabilities"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json

from .framework import AnalysisFramework
from ..video_processor.scene_detector import Scene
from ..audio_processor.transcriber import Transcript
from ..ollama_service.client import OllamaClient


@dataclass
class ScriptAnalysis:
    """Complete script analysis results"""
    structure_analysis: Dict[str, Any]
    character_analysis: Dict[str, Any]
    dialogue_analysis: Dict[str, Any]
    theme_analysis: Dict[str, Any]
    pacing_analysis: Dict[str, Any]
    overall_score: float
    recommendations: List[str]
    strengths: List[str]
    weaknesses: List[str]

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "structure_analysis": self.structure_analysis,
            "character_analysis": self.character_analysis,
            "dialogue_analysis": self.dialogue_analysis,
            "theme_analysis": self.theme_analysis,
            "pacing_analysis": self.pacing_analysis,
            "overall_score": self.overall_score,
            "recommendations": self.recommendations,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses
        }

    def save_json(self, output_path: str):
        """Save analysis to JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def save_markdown(self, output_path: str):
        """Save analysis as markdown report"""
        report = f"""# Scriptwriting Analysis Report

## Overall Score: {self.overall_score:.1f}/10

## Structure Analysis

{self._format_dict(self.structure_analysis)}

## Character Analysis

{self._format_dict(self.character_analysis)}

## Dialogue Analysis

{self._format_dict(self.dialogue_analysis)}

## Theme Analysis

{self._format_dict(self.theme_analysis)}

## Pacing Analysis

{self._format_dict(self.pacing_analysis)}

## Strengths

{self._format_list(self.strengths)}

## Weaknesses

{self._format_list(self.weaknesses)}

## Recommendations

{self._format_list(self.recommendations)}
"""
        with open(output_path, 'w') as f:
            f.write(report)

    def _format_dict(self, d: dict, indent: int = 0) -> str:
        """Format dictionary for markdown"""
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{'  ' * indent}**{key}:**")
                lines.append(self._format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{'  ' * indent}**{key}:**")
                lines.extend([f"{'  ' * (indent + 1)}- {item}" for item in value])
            else:
                lines.append(f"{'  ' * indent}**{key}:** {value}")
        return '\n'.join(lines)

    def _format_list(self, items: list) -> str:
        """Format list for markdown"""
        return '\n'.join([f"- {item}" for item in items])


class ScriptwritingAnalyzer:
    """Expert scriptwriting analysis using AI and frameworks"""

    def __init__(
        self,
        ollama_client: Optional[OllamaClient] = None,
        framework_type: str = "three_act"
    ):
        """
        Initialize scriptwriting analyzer

        Args:
            ollama_client: Optional OllamaClient for AI-powered analysis
            framework_type: Structural framework to use
        """
        self.ollama_client = ollama_client
        self.framework_type = framework_type
        self.framework = AnalysisFramework()

    def analyze(
        self,
        scenes: List[Scene],
        transcript: Transcript,
        summary: str,
        genre: Optional[str] = None
    ) -> ScriptAnalysis:
        """
        Perform comprehensive scriptwriting analysis

        Args:
            scenes: List of Scene objects
            transcript: Transcript object
            summary: Movie summary
            genre: Movie genre (optional)

        Returns:
            ScriptAnalysis object
        """
        # Analyze structure
        structure_analysis = self._analyze_structure(scenes, summary)

        # Analyze dialogue
        dialogue_analysis = self._analyze_dialogue(transcript)

        # Analyze pacing
        pacing_analysis = self._analyze_pacing(scenes, genre)

        # Analyze themes (using AI if available)
        theme_analysis = self._analyze_themes(transcript, summary)

        # Analyze characters (using AI if available)
        character_analysis = self._analyze_characters(transcript, summary)

        # Generate recommendations
        recommendations, strengths, weaknesses = self._generate_recommendations(
            structure_analysis,
            dialogue_analysis,
            pacing_analysis
        )

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            structure_analysis,
            dialogue_analysis,
            pacing_analysis
        )

        return ScriptAnalysis(
            structure_analysis=structure_analysis,
            character_analysis=character_analysis,
            dialogue_analysis=dialogue_analysis,
            theme_analysis=theme_analysis,
            pacing_analysis=pacing_analysis,
            overall_score=overall_score,
            recommendations=recommendations,
            strengths=strengths,
            weaknesses=weaknesses
        )

    def _analyze_structure(self, scenes: List[Scene], summary: str) -> Dict[str, Any]:
        """Analyze story structure"""
        scene_count = len(scenes)
        total_duration = scenes[-1].end_time if scenes else 0

        # Get structural framework
        framework = self.framework.get_structure_framework(self.framework_type)

        # Calculate act boundaries
        act_boundaries = {
            "act_1_end": total_duration * 0.25,
            "act_2_end": total_duration * 0.75,
            "midpoint": total_duration * 0.50
        }

        # Find which scenes correspond to act boundaries
        act_scenes = {}
        for act_name, timestamp in act_boundaries.items():
            for scene in scenes:
                if scene.start_time <= timestamp <= scene.end_time:
                    act_scenes[act_name] = scene.scene_number
                    break

        return {
            "framework": self.framework_type,
            "total_scenes": scene_count,
            "total_duration": total_duration,
            "act_boundaries": act_boundaries,
            "act_scenes": act_scenes,
            "structural_points": [
                {
                    "name": sp.name,
                    "expected_time": total_duration * sp.expected_position,
                    "description": sp.description
                }
                for sp in framework
            ]
        }

    def _analyze_dialogue(self, transcript: Transcript) -> Dict[str, Any]:
        """Analyze dialogue quality"""
        segments = transcript.segments
        total_words = len(transcript.full_text.split())
        avg_segment_length = total_words / len(segments) if segments else 0

        # Calculate dialogue density
        dialogue_time = sum(seg.end - seg.start for seg in segments)
        silence_ratio = 1 - (dialogue_time / transcript.duration) if transcript.duration > 0 else 0

        # Analyze word variety (simple measure)
        unique_words = len(set(transcript.full_text.lower().split()))
        vocabulary_richness = unique_words / total_words if total_words > 0 else 0

        return {
            "total_words": total_words,
            "total_segments": len(segments),
            "average_segment_length": avg_segment_length,
            "vocabulary_richness": vocabulary_richness,
            "silence_ratio": silence_ratio,
            "dialogue_time": dialogue_time,
            "words_per_minute": (total_words / transcript.duration * 60) if transcript.duration > 0 else 0
        }

    def _analyze_pacing(self, scenes: List[Scene], genre: Optional[str]) -> Dict[str, Any]:
        """Analyze pacing"""
        scene_durations = [scene.duration for scene in scenes]
        return self.framework.evaluate_pacing(scene_durations, genre or "drama")

    def _analyze_themes(self, transcript: Transcript, summary: str) -> Dict[str, Any]:
        """Analyze themes (uses AI if available)"""
        if self.ollama_client:
            return self._ai_analyze_themes(transcript, summary)
        else:
            return {
                "method": "keyword_based",
                "common_themes": self.framework.COMMON_THEMES[:5],
                "note": "AI analysis not available. Using common themes."
            }

    def _ai_analyze_themes(self, transcript: Transcript, summary: str) -> Dict[str, Any]:
        """AI-powered theme analysis"""
        prompt = f"""Analyze the themes in this movie.

Summary: {summary}

Transcript excerpt: {transcript.full_text[:1000]}...

Identify 3-5 major themes and explain how they are developed.
Respond in JSON format with an array of theme objects containing 'name' and 'analysis' fields."""

        try:
            response = self.ollama_client.generate(
                prompt=prompt,
                temperature=0.7
            )

            # Try to parse JSON
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                themes = json.loads(json_str)
            else:
                themes = json.loads(response)

            return {
                "method": "ai_analysis",
                "themes": themes
            }
        except:
            return {
                "method": "ai_analysis_failed",
                "raw_response": response if 'response' in locals() else "Failed to generate"
            }

    def _analyze_characters(self, transcript: Transcript, summary: str) -> Dict[str, Any]:
        """Analyze character development (uses AI if available)"""
        if self.ollama_client:
            return self._ai_analyze_characters(transcript, summary)
        else:
            return {
                "method": "basic",
                "note": "AI analysis not available",
                "arc_types": list(self.framework.CHARACTER_ARC_TYPES.keys())
            }

    def _ai_analyze_characters(self, transcript: Transcript, summary: str) -> Dict[str, Any]:
        """AI-powered character analysis"""
        prompt = f"""Analyze the main characters in this movie.

Summary: {summary}

Identify 2-3 main characters and analyze their:
- Character arc type (positive change, negative change, flat arc, etc.)
- Development throughout the story
- Key relationships
- Motivations

Respond in JSON format."""

        try:
            response = self.ollama_client.generate(prompt=prompt, temperature=0.7)
            return {"method": "ai_analysis", "analysis": response}
        except:
            return {"method": "ai_analysis_failed"}

    def _generate_recommendations(
        self,
        structure: dict,
        dialogue: dict,
        pacing: dict
    ) -> tuple:
        """Generate recommendations, strengths, and weaknesses"""
        recommendations = []
        strengths = []
        weaknesses = []

        # Structure recommendations
        total_scenes = structure.get('total_scenes', 0)
        if total_scenes < 30:
            recommendations.append("Consider adding more scenes to develop the story")
        elif total_scenes > 100:
            recommendations.append("Consider consolidating scenes for better pacing")

        # Dialogue recommendations
        words_per_min = dialogue.get('words_per_minute', 0)
        if words_per_min < 100:
            weaknesses.append("Low dialogue density - may feel slow")
            recommendations.append("Increase dialogue or add more character interaction")
        elif words_per_min > 180:
            weaknesses.append("High dialogue density - may feel rushed")
            recommendations.append("Allow more breathing room and visual storytelling")
        else:
            strengths.append("Good dialogue pacing")

        vocab_richness = dialogue.get('vocabulary_richness', 0)
        if vocab_richness > 0.3:
            strengths.append("Rich and varied vocabulary")
        elif vocab_richness < 0.15:
            weaknesses.append("Limited vocabulary variety")
            recommendations.append("Diversify word choice and dialogue styles")

        # Pacing recommendations
        pacing_consistency = pacing.get('pacing_consistency', '')
        if pacing_consistency == 'high':
            strengths.append("Consistent scene pacing")
        else:
            recommendations.append("Review scene length variations for intentional pacing")

        return recommendations, strengths, weaknesses

    def _calculate_overall_score(
        self,
        structure: dict,
        dialogue: dict,
        pacing: dict
    ) -> float:
        """Calculate overall screenplay score (0-10)"""
        score = 5.0  # Base score

        # Adjust for scene count (optimal: 40-80 scenes)
        scene_count = structure.get('total_scenes', 0)
        if 40 <= scene_count <= 80:
            score += 1.0
        elif 30 <= scene_count <= 100:
            score += 0.5

        # Adjust for dialogue pacing
        wpm = dialogue.get('words_per_minute', 0)
        if 120 <= wpm <= 160:
            score += 1.0
        elif 100 <= wpm <= 180:
            score += 0.5

        # Adjust for vocabulary
        vocab = dialogue.get('vocabulary_richness', 0)
        if vocab > 0.25:
            score += 1.0
        elif vocab > 0.18:
            score += 0.5

        # Adjust for pacing consistency
        if pacing.get('pacing_consistency') == 'high':
            score += 0.5

        # Ensure score is between 0 and 10
        return min(10.0, max(0.0, score))
