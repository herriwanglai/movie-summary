"""Scriptwriting analysis frameworks and knowledge base"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class StructuralPoint:
    """Key structural point in screenplay"""
    name: str
    expected_position: float  # Percentage through the movie (0.0 - 1.0)
    description: str


class AnalysisFramework:
    """Framework for screenplay analysis"""

    # Three-Act Structure
    THREE_ACT_STRUCTURE = [
        StructuralPoint("Opening Image", 0.00, "First impression of the story world"),
        StructuralPoint("Setup", 0.00, "Introduce protagonist, world, and status quo"),
        StructuralPoint("Inciting Incident", 0.10, "Event that sets story in motion"),
        StructuralPoint("Plot Point 1", 0.25, "End of Act 1 - protagonist commits to journey"),
        StructuralPoint("Midpoint", 0.50, "Major shift or revelation"),
        StructuralPoint("Plot Point 2", 0.75, "End of Act 2 - all hope is lost"),
        StructuralPoint("Climax", 0.90, "Final confrontation"),
        StructuralPoint("Resolution", 0.95, "New status quo established"),
    ]

    # Save the Cat Beat Sheet
    SAVE_THE_CAT_BEATS = [
        StructuralPoint("Opening Image", 0.00, "Snapshot of protagonist's world"),
        StructuralPoint("Theme Stated", 0.05, "What the story is really about"),
        StructuralPoint("Setup", 0.01, "Introduce characters and world"),
        StructuralPoint("Catalyst", 0.10, "Life-changing event"),
        StructuralPoint("Debate", 0.12, "Should the hero take the journey?"),
        StructuralPoint("Break into Two", 0.20, "Hero commits to the journey"),
        StructuralPoint("B Story", 0.22, "Secondary plot begins"),
        StructuralPoint("Fun and Games", 0.25, "Promise of the premise"),
        StructuralPoint("Midpoint", 0.50, "False victory or false defeat"),
        StructuralPoint("Bad Guys Close In", 0.55, "Things get worse"),
        StructuralPoint("All Is Lost", 0.75, "Lowest point"),
        StructuralPoint("Dark Night of the Soul", 0.77, "Moment of reflection"),
        StructuralPoint("Break into Three", 0.80, "Solution discovered"),
        StructuralPoint("Finale", 0.85, "Climax and resolution"),
        StructuralPoint("Final Image", 0.99, "Opposite of opening image"),
    ]

    # Character Arc Types
    CHARACTER_ARC_TYPES = {
        "positive_change": {
            "description": "Character grows and improves",
            "examples": "Luke Skywalker, Andy Dufresne"
        },
        "negative_change": {
            "description": "Character deteriorates or falls",
            "examples": "Michael Corleone, Walter White"
        },
        "flat_arc": {
            "description": "Character stays the same but changes the world",
            "examples": "James Bond, Sherlock Holmes"
        },
        "corruption_arc": {
            "description": "Good character becomes bad",
            "examples": "Anakin Skywalker, Harvey Dent"
        },
        "redemption_arc": {
            "description": "Bad character becomes good",
            "examples": "Ebenezer Scrooge, Zuko"
        }
    }

    # Story Themes Categories
    COMMON_THEMES = [
        "Love and Relationships",
        "Good vs Evil",
        "Coming of Age",
        "Identity and Self-Discovery",
        "Power and Corruption",
        "Survival",
        "Revenge",
        "Redemption",
        "Sacrifice",
        "Family",
        "Justice",
        "Freedom",
        "Death and Mortality",
        "Truth vs Deception",
        "Nature vs Technology"
    ]

    # Dialogue Quality Criteria
    DIALOGUE_CRITERIA = {
        "subtext": "Does dialogue have layers beneath the surface?",
        "character_voice": "Does each character have a distinct voice?",
        "conflict": "Does dialogue create or reveal conflict?",
        "advancement": "Does dialogue move the story forward?",
        "naturalism": "Does dialogue sound realistic yet purposeful?",
        "economy": "Is every line necessary?",
        "rhythm": "Does dialogue have good pacing and rhythm?"
    }

    # Pacing Guidelines
    PACING_GUIDELINES = {
        "action": "Fast cuts, short scenes, high energy",
        "drama": "Longer scenes, character focus, emotional beats",
        "thriller": "Escalating tension, time pressure, suspense",
        "comedy": "Rhythm and timing, setup and payoff",
        "horror": "Build and release, quiet and loud moments"
    }

    @classmethod
    def get_structure_framework(cls, framework_type: str = "three_act") -> List[StructuralPoint]:
        """Get structural framework"""
        if framework_type == "three_act":
            return cls.THREE_ACT_STRUCTURE
        elif framework_type == "save_the_cat":
            return cls.SAVE_THE_CAT_BEATS
        else:
            return cls.THREE_ACT_STRUCTURE

    @classmethod
    def analyze_structure_alignment(
        cls,
        scene_count: int,
        key_moments: List[Dict[str, Any]],
        framework_type: str = "three_act"
    ) -> Dict[str, Any]:
        """
        Analyze how well the movie aligns with structural framework

        Args:
            scene_count: Total number of scenes
            key_moments: List of identified key moments with scene numbers
            framework_type: Type of framework to use

        Returns:
            Analysis results
        """
        framework = cls.get_structure_framework(framework_type)
        alignment_score = 0
        deviations = []

        for moment in key_moments:
            scene_num = moment.get('scene_number', 0)
            position = scene_num / scene_count if scene_count > 0 else 0

            # Find closest structural point
            closest_point = min(
                framework,
                key=lambda sp: abs(sp.expected_position - position)
            )

            deviation = abs(closest_point.expected_position - position)
            if deviation < 0.1:  # Within 10%
                alignment_score += 1
            else:
                deviations.append({
                    "moment": moment.get('name', 'Unknown'),
                    "expected": closest_point.expected_position,
                    "actual": position,
                    "deviation": deviation
                })

        return {
            "framework": framework_type,
            "alignment_score": alignment_score / len(framework) if framework else 0,
            "deviations": deviations,
            "total_points": len(framework)
        }

    @classmethod
    def get_character_arc_guidance(cls, arc_type: str) -> Dict[str, Any]:
        """Get guidance for character arc type"""
        return cls.CHARACTER_ARC_TYPES.get(arc_type, {})

    @classmethod
    def evaluate_pacing(
        cls,
        scene_durations: List[float],
        genre: str = "drama"
    ) -> Dict[str, Any]:
        """
        Evaluate pacing based on scene durations

        Args:
            scene_durations: List of scene durations in seconds
            genre: Movie genre

        Returns:
            Pacing analysis
        """
        if not scene_durations:
            return {"error": "No scenes provided"}

        avg_duration = sum(scene_durations) / len(scene_durations)
        variance = sum((d - avg_duration) ** 2 for d in scene_durations) / len(scene_durations)

        # Identify pacing issues
        long_scenes = [i for i, d in enumerate(scene_durations) if d > avg_duration * 2]
        short_scenes = [i for i, d in enumerate(scene_durations) if d < avg_duration * 0.5]

        return {
            "average_scene_duration": avg_duration,
            "variance": variance,
            "pacing_consistency": "high" if variance < avg_duration else "varied",
            "long_scenes": long_scenes,
            "short_scenes": short_scenes,
            "genre_guidance": cls.PACING_GUIDELINES.get(genre.lower(), "Varies by genre"),
            "total_scenes": len(scene_durations)
        }
