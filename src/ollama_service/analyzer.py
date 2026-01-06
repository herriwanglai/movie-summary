"""Movie analyzer using Ollama"""

from typing import List, Dict, Any, Optional
from .client import OllamaClient
from .tools import MovieAnalysisTools
from ..video_processor.keyframe_selector import Keyframe
from ..video_processor.scene_detector import Scene
from ..audio_processor.transcriber import Transcript
import json


class MovieAnalyzer:
    """Analyze movies using Ollama with deepseek-r1"""

    def __init__(
        self,
        client: OllamaClient,
        tools: MovieAnalysisTools,
        temperature: float = 0.7
    ):
        """
        Initialize movie analyzer

        Args:
            client: OllamaClient instance
            tools: MovieAnalysisTools instance
            temperature: Sampling temperature
        """
        self.client = client
        self.tools = tools
        self.temperature = temperature

    def generate_summary(self, max_length: int = 500) -> str:
        """
        Generate movie summary

        Args:
            max_length: Maximum summary length in words

        Returns:
            Movie summary
        """
        scenes_info = self.tools.list_scenes()
        total_scenes = scenes_info['total_scenes']

        system_prompt = """You are a professional film critic and analyst.
        You have access to tools to view scenes and read the transcript of a movie.
        Provide insightful, detailed analysis of films."""

        prompt = f"""Please analyze this movie and provide a comprehensive summary.

        The movie has {total_scenes} scenes. Use the available tools to:
        1. List all scenes to understand the structure
        2. View key scenes to understand visual storytelling
        3. Read the transcript to understand dialogue and narrative

        Then provide a summary covering:
        - Plot overview
        - Main themes
        - Visual style
        - Key moments
        - Overall impression

        Keep the summary under {max_length} words."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = self.client.generate_with_tools(
            messages=messages,
            tools=self.tools.get_tool_definitions(),
            tool_executor=lambda name, args: self.tools.execute_tool(name, args),
            temperature=self.temperature
        )

        return response

    def analyze_scene(self, scene_number: int) -> Dict[str, Any]:
        """
        Analyze a specific scene in detail

        Args:
            scene_number: Scene number to analyze

        Returns:
            Scene analysis dict
        """
        system_prompt = """You are a professional film analyst specializing in scene analysis.
        Analyze scenes for visual composition, narrative purpose, and emotional impact."""

        prompt = f"""Please analyze scene {scene_number} in detail.

        Use the tools to:
        1. View the scene's keyframes
        2. Read the scene's transcript

        Provide analysis covering:
        - Visual composition and cinematography
        - Dialogue and subtext
        - Character interactions
        - Narrative purpose
        - Emotional tone
        - How it connects to the overall story

        Format your response as a structured analysis."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = self.client.generate_with_tools(
            messages=messages,
            tools=self.tools.get_tool_definitions(),
            tool_executor=lambda name, args: self.tools.execute_tool(name, args),
            temperature=self.temperature
        )

        return {
            "scene_number": scene_number,
            "analysis": response
        }

    def identify_themes(self) -> List[str]:
        """
        Identify major themes in the movie

        Returns:
            List of identified themes
        """
        system_prompt = """You are a film scholar specializing in thematic analysis.
        Identify and explain the major themes in films."""

        prompt = """Please analyze this movie and identify its major themes.

        Use the available tools to explore scenes and dialogue throughout the movie.

        List 3-5 major themes and explain how each is developed through:
        - Visual motifs
        - Dialogue
        - Character arcs
        - Plot events

        Format your response as a JSON array of theme objects with 'name' and 'description' fields."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = self.client.generate_with_tools(
            messages=messages,
            tools=self.tools.get_tool_definitions(),
            tool_executor=lambda name, args: self.tools.execute_tool(name, args),
            temperature=self.temperature
        )

        # Try to parse JSON response
        try:
            # Extract JSON from response if it's wrapped in markdown
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            else:
                return json.loads(response)
        except:
            # Fallback: return as plain text
            return [{"name": "Themes", "description": response}]

    def analyze_character(self, character_name: str) -> Dict[str, Any]:
        """
        Analyze a character's development and role

        Args:
            character_name: Name of the character

        Returns:
            Character analysis dict
        """
        system_prompt = """You are a character analysis expert.
        Provide detailed character analysis including motivations, arc, and relationships."""

        prompt = f"""Please analyze the character "{character_name}" in this movie.

        Use the tools to search for their dialogue and appearances throughout the movie.

        Analyze:
        - Character introduction and initial state
        - Motivations and goals
        - Character arc and development
        - Key relationships
        - Defining moments
        - Final state and transformation

        Provide a comprehensive character study."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = self.client.generate_with_tools(
            messages=messages,
            tools=self.tools.get_tool_definitions(),
            tool_executor=lambda name, args: self.tools.execute_tool(name, args),
            temperature=self.temperature
        )

        return {
            "character_name": character_name,
            "analysis": response
        }

    def generate_scene_descriptions(self) -> List[Dict[str, Any]]:
        """
        Generate descriptions for all scenes

        Returns:
            List of scene descriptions
        """
        scenes = self.tools.list_scenes()
        descriptions = []

        system_prompt = """You are a film annotator. Provide concise, vivid scene descriptions."""

        for scene in scenes['scenes'][:10]:  # Limit to first 10 scenes for efficiency
            scene_num = scene['scene_number']

            prompt = f"""Describe scene {scene_num} in 2-3 sentences.
            View the scene and read its transcript, then describe what happens."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            response = self.client.generate_with_tools(
                messages=messages,
                tools=self.tools.get_tool_definitions(),
                tool_executor=lambda name, args: self.tools.execute_tool(name, args),
                temperature=self.temperature,
                max_iterations=5  # Limit iterations per scene
            )

            descriptions.append({
                "scene_number": scene_num,
                "start_time": scene['start_time'],
                "end_time": scene['end_time'],
                "description": response
            })

        return descriptions

    def compare_scenes(self, scene1: int, scene2: int) -> str:
        """
        Compare two scenes

        Args:
            scene1: First scene number
            scene2: Second scene number

        Returns:
            Comparison analysis
        """
        system_prompt = """You are a film analyst specializing in comparative analysis."""

        prompt = f"""Compare scene {scene1} and scene {scene2}.

        For each scene:
        1. View the keyframes
        2. Read the transcript

        Then compare them in terms of:
        - Visual style
        - Narrative function
        - Emotional tone
        - Dialogue approach
        - How they relate to each other in the story

        Provide a detailed comparison."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = self.client.generate_with_tools(
            messages=messages,
            tools=self.tools.get_tool_definitions(),
            tool_executor=lambda name, args: self.tools.execute_tool(name, args),
            temperature=self.temperature
        )

        return response
