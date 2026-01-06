"""Enhanced tools with importance detection for better movie analysis"""

from typing import List, Dict, Any
from .tools import MovieAnalysisTools
from ..video_processor.importance_detector import ImportanceDetector, SceneImportance


class EnhancedMovieTools(MovieAnalysisTools):
    """
    Enhanced tools that provide pre-analyzed importance information

    This allows deepseek-r1:8b to:
    1. Know which scenes are most important BEFORE watching
    2. Understand character relationships from dialogue analysis
    3. Identify exciting/climactic moments automatically
    4. Focus on key plot points
    """

    def __init__(
        self,
        keyframes,
        scenes,
        transcript,
        frames_dir,
        importance_analyses: List[SceneImportance] = None
    ):
        """
        Initialize enhanced tools

        Args:
            importance_analyses: Pre-computed scene importance analyses
        """
        super().__init__(keyframes, scenes, transcript, frames_dir)
        self.importance_analyses = importance_analyses or []

        # Create importance lookup
        self.importance_by_scene = {
            imp.scene_number: imp
            for imp in self.importance_analyses
        }

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get enhanced tool definitions"""
        base_tools = super().get_tool_definitions()

        # Add new enhanced tools
        enhanced_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_important_scenes",
                    "description": "Get the most important/exciting scenes in the movie (already pre-analyzed)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "top_n": {
                                "type": "integer",
                                "description": "Number of top scenes to return",
                                "default": 10
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by category: action, exciting, dialogue_heavy, quiet",
                                "default": None
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_climax_scenes",
                    "description": "Get scenes that are likely the climax of the movie",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_character_relationships",
                    "description": "Analyze character relationships from dialogue",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "character_name": {
                                "type": "string",
                                "description": "Name of character to analyze relationships for"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_plot_structure",
                    "description": "Get the movie's plot structure with key turning points",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_emotional_arc",
                    "description": "Get the emotional arc/intensity throughout the movie",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_character_motivation",
                    "description": "Find dialogue that reveals character motivations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "character_name": {
                                "type": "string",
                                "description": "Character name to analyze"
                            }
                        },
                        "required": ["character_name"]
                    }
                }
            }
        ]

        return base_tools + enhanced_tools

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool with enhanced functionality"""

        # Handle enhanced tools
        if tool_name == "get_important_scenes":
            return self.get_important_scenes(
                arguments.get('top_n', 10),
                arguments.get('category')
            )
        elif tool_name == "get_climax_scenes":
            return self.get_climax_scenes()
        elif tool_name == "get_character_relationships":
            return self.get_character_relationships(arguments['character_name'])
        elif tool_name == "get_plot_structure":
            return self.get_plot_structure()
        elif tool_name == "get_emotional_arc":
            return self.get_emotional_arc()
        elif tool_name == "find_character_motivation":
            return self.find_character_motivation(arguments['character_name'])

        # Enhance base tool responses with importance info
        elif tool_name == "view_scene":
            result = super().execute_tool(tool_name, arguments)
            scene_num = arguments['scene_number']
            if scene_num in self.importance_by_scene:
                imp = self.importance_by_scene[scene_num]
                result['importance_analysis'] = {
                    'importance_score': imp.importance_score,
                    'categories': imp.categories,
                    'reasons': imp.reasons,
                    'visual_intensity': imp.visual_intensity,
                    'audio_intensity': imp.audio_intensity
                }
            return result

        else:
            # Fall back to base tools
            return super().execute_tool(tool_name, arguments)

    def get_important_scenes(
        self,
        top_n: int = 10,
        category: str = None
    ) -> Dict[str, Any]:
        """
        Get most important scenes (pre-analyzed BEFORE AI watches)

        This gives deepseek a roadmap of key moments
        """
        if category:
            filtered = [
                imp for imp in self.importance_analyses
                if category in imp.categories
            ]
            scenes = filtered[:top_n]
        else:
            scenes = self.importance_analyses[:top_n]

        return {
            "total_analyzed": len(self.importance_analyses),
            "returned": len(scenes),
            "important_scenes": [
                {
                    "scene_number": imp.scene_number,
                    "importance_score": round(imp.importance_score, 2),
                    "categories": imp.categories,
                    "reasons": imp.reasons,
                    "time_range": f"{self.scenes[imp.scene_number - 1].start_time:.1f}s - {self.scenes[imp.scene_number - 1].end_time:.1f}s",
                    "visual_intensity": round(imp.visual_intensity, 2),
                    "audio_intensity": round(imp.audio_intensity, 2)
                }
                for imp in scenes
            ],
            "recommendation": "View these scenes first for key plot points and exciting moments"
        }

    def get_climax_scenes(self) -> Dict[str, Any]:
        """Get likely climax scenes (typically 75-90% through the movie)"""
        total_duration = self.scenes[-1].end_time if self.scenes else 0

        # Find scenes in climax region with high importance
        climax_scenes = [
            imp for imp in self.importance_analyses
            if 0.75 <= (self.scenes[imp.scene_number - 1].start_time / total_duration) <= 0.95
            and imp.importance_score > 0.6
        ]

        # Sort by importance
        climax_scenes.sort(key=lambda x: x.importance_score, reverse=True)

        return {
            "climax_region": "75-95% of movie runtime",
            "likely_climax_scenes": [
                {
                    "scene_number": imp.scene_number,
                    "importance_score": round(imp.importance_score, 2),
                    "position": f"{(self.scenes[imp.scene_number - 1].start_time / total_duration * 100):.1f}%",
                    "categories": imp.categories,
                    "reasons": imp.reasons
                }
                for imp in climax_scenes[:5]
            ]
        }

    def get_character_relationships(self, character_name: str) -> Dict[str, Any]:
        """
        Analyze character relationships from dialogue patterns

        This helps identify:
        - Who the character interacts with most
        - Nature of relationships (conflict, support, etc.)
        """
        character_lower = character_name.lower()

        # Find all dialogue mentioning this character
        mentions = self.transcript.search(character_name, case_sensitive=False)

        # Analyze dialogue around character
        relationships = {}
        emotions = []

        for segment in mentions:
            text_lower = segment.text.lower()

            # Detect emotional context
            if any(word in text_lower for word in ['love', 'care', 'friend']):
                emotions.append('positive')
            elif any(word in text_lower for word in ['hate', 'enemy', 'kill', 'fight']):
                emotions.append('conflict')

            # Look for other character names (simplified - in real impl, use NER)
            # For now, look for capitalized words
            words = segment.text.split()
            for word in words:
                if word[0].isupper() and word.lower() != character_lower:
                    if word not in relationships:
                        relationships[word] = 0
                    relationships[word] += 1

        return {
            "character": character_name,
            "total_mentions": len(mentions),
            "mentioned_with": [
                {"name": name, "co_occurrence": count}
                for name, count in sorted(relationships.items(), key=lambda x: x[1], reverse=True)[:5]
            ],
            "emotional_context": {
                "positive": emotions.count('positive'),
                "conflict": emotions.count('conflict')
            },
            "key_moments": [
                {
                    "timestamp": seg.start,
                    "dialogue": seg.text
                }
                for seg in mentions[:5]
            ]
        }

    def get_plot_structure(self) -> Dict[str, Any]:
        """
        Get plot structure with key turning points

        Based on three-act structure and importance analysis
        """
        total_duration = self.scenes[-1].end_time if self.scenes else 0

        # Identify key structural points
        act1_end = 0.25 * total_duration
        midpoint = 0.50 * total_duration
        act2_end = 0.75 * total_duration
        climax = 0.90 * total_duration

        def find_important_scene_near(target_time, window=0.05):
            """Find most important scene near target time"""
            window_duration = window * total_duration
            candidates = [
                imp for imp in self.importance_analyses
                if abs(self.scenes[imp.scene_number - 1].start_time - target_time) < window_duration
            ]
            if candidates:
                return max(candidates, key=lambda x: x.importance_score)
            return None

        structure = {
            "three_act_structure": {
                "act_1": {
                    "range": f"0% - 25% (0s - {act1_end:.1f}s)",
                    "key_moment": None
                },
                "act_2": {
                    "range": f"25% - 75% ({act1_end:.1f}s - {act2_end:.1f}s)",
                    "midpoint": None
                },
                "act_3": {
                    "range": f"75% - 100% ({act2_end:.1f}s - {total_duration:.1f}s)",
                    "climax": None
                }
            }
        }

        # Find important scenes at key points
        act1_scene = find_important_scene_near(act1_end)
        if act1_scene:
            structure["three_act_structure"]["act_1"]["key_moment"] = {
                "scene": act1_scene.scene_number,
                "note": "Likely inciting incident or plot point 1",
                "importance": round(act1_scene.importance_score, 2)
            }

        midpoint_scene = find_important_scene_near(midpoint)
        if midpoint_scene:
            structure["three_act_structure"]["act_2"]["midpoint"] = {
                "scene": midpoint_scene.scene_number,
                "note": "Midpoint - major shift or revelation",
                "importance": round(midpoint_scene.importance_score, 2)
            }

        climax_scene = find_important_scene_near(climax)
        if climax_scene:
            structure["three_act_structure"]["act_3"]["climax"] = {
                "scene": climax_scene.scene_number,
                "note": "Climax - final confrontation",
                "importance": round(climax_scene.importance_score, 2)
            }

        return structure

    def get_emotional_arc(self) -> Dict[str, Any]:
        """
        Get emotional intensity throughout the movie

        Shows the rise and fall of tension/excitement
        """
        # Sample emotional intensity at 10% intervals
        total_duration = self.scenes[-1].end_time if self.scenes else 0
        intervals = []

        for pct in range(0, 101, 10):
            target_time = (pct / 100.0) * total_duration

            # Find scene at this time
            scene = None
            for s in self.scenes:
                if s.start_time <= target_time <= s.end_time:
                    scene = s
                    break

            if scene and scene.scene_number in self.importance_by_scene:
                imp = self.importance_by_scene[scene.scene_number]
                intervals.append({
                    "position": f"{pct}%",
                    "intensity": round((imp.visual_intensity + imp.audio_intensity) / 2, 2),
                    "scene": scene.scene_number
                })

        return {
            "emotional_arc": intervals,
            "note": "Higher intensity indicates action/excitement, lower indicates quieter moments",
            "interpretation": self._interpret_arc(intervals)
        }

    def _interpret_arc(self, intervals: List[Dict]) -> str:
        """Interpret the emotional arc pattern"""
        if not intervals:
            return "Unable to analyze"

        intensities = [i['intensity'] for i in intervals]

        # Find peaks
        peaks = []
        for i in range(1, len(intensities) - 1):
            if intensities[i] > intensities[i-1] and intensities[i] > intensities[i+1]:
                peaks.append(intervals[i]['position'])

        if not peaks:
            return "Steady intensity throughout"

        return f"Peaks at {', '.join(peaks)} suggesting building tension and releases"

    def find_character_motivation(self, character_name: str) -> Dict[str, Any]:
        """
        Find dialogue that reveals character motivations

        Looks for keywords indicating goals, fears, desires
        """
        # Find all dialogue mentioning the character
        mentions = self.transcript.search(character_name, case_sensitive=False)

        # Keywords for different motivation types
        motivation_keywords = {
            'goal': ['want', 'need', 'must', 'have to', 'going to', 'will'],
            'fear': ['afraid', 'fear', 'scared', 'worry', 'anxious'],
            'desire': ['wish', 'hope', 'dream', 'love', 'care'],
            'conflict': ['but', 'however', 'can\'t', 'won\'t', 'impossible'],
            'backstory': ['was', 'used to', 'remember', 'before', 'ago']
        }

        categorized = {cat: [] for cat in motivation_keywords}

        for segment in mentions:
            text_lower = segment.text.lower()
            for category, keywords in motivation_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    categorized[category].append({
                        'timestamp': segment.start,
                        'dialogue': segment.text
                    })

        return {
            "character": character_name,
            "motivation_analysis": {
                category: moments[:3]  # Top 3 for each category
                for category, moments in categorized.items()
                if moments
            },
            "summary": f"Found {sum(len(m) for m in categorized.values())} dialogue moments revealing motivations"
        }
