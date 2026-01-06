"""Tool definitions for movie analysis"""

from typing import List, Dict, Any, Optional
import base64
from pathlib import Path
from ..video_processor.keyframe_selector import Keyframe
from ..video_processor.scene_detector import Scene
from ..audio_processor.transcriber import Transcript


class MovieAnalysisTools:
    """Tools for movie analysis that can be used by Ollama"""

    def __init__(
        self,
        keyframes: List[Keyframe],
        scenes: List[Scene],
        transcript: Transcript,
        frames_dir: str
    ):
        """
        Initialize movie analysis tools

        Args:
            keyframes: List of extracted keyframes
            scenes: List of detected scenes
            transcript: Movie transcript
            frames_dir: Directory containing frame images
        """
        self.keyframes = keyframes
        self.scenes = scenes
        self.transcript = transcript
        self.frames_dir = Path(frames_dir)

        # Create lookup dicts for fast access
        self.keyframes_by_scene = {}
        for kf in keyframes:
            if kf.scene_number not in self.keyframes_by_scene:
                self.keyframes_by_scene[kf.scene_number] = []
            self.keyframes_by_scene[kf.scene_number].append(kf)

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions for Ollama

        Returns:
            List of tool definition dicts
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "view_scene",
                    "description": "View keyframes and information about a specific scene",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "scene_number": {
                                "type": "integer",
                                "description": "The scene number to view"
                            }
                        },
                        "required": ["scene_number"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_transcript",
                    "description": "Get transcript text for a time range",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "start_time": {
                                "type": "number",
                                "description": "Start time in seconds"
                            },
                            "end_time": {
                                "type": "number",
                                "description": "End time in seconds"
                            }
                        },
                        "required": ["start_time", "end_time"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_dialogue",
                    "description": "Search for specific dialogue in the transcript",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Text to search for"
                            },
                            "case_sensitive": {
                                "type": "boolean",
                                "description": "Whether search should be case sensitive",
                                "default": False
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_scene_info",
                    "description": "Get detailed information about a scene",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "scene_number": {
                                "type": "integer",
                                "description": "The scene number"
                            }
                        },
                        "required": ["scene_number"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_scenes",
                    "description": "List all scenes with their time ranges",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_scene_transcript",
                    "description": "Get transcript for a specific scene",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "scene_number": {
                                "type": "integer",
                                "description": "The scene number"
                            }
                        },
                        "required": ["scene_number"]
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if tool_name == "view_scene":
            return self.view_scene(arguments['scene_number'])
        elif tool_name == "get_transcript":
            return self.get_transcript(arguments['start_time'], arguments['end_time'])
        elif tool_name == "search_dialogue":
            return self.search_dialogue(
                arguments['query'],
                arguments.get('case_sensitive', False)
            )
        elif tool_name == "get_scene_info":
            return self.get_scene_info(arguments['scene_number'])
        elif tool_name == "list_scenes":
            return self.list_scenes()
        elif tool_name == "get_scene_transcript":
            return self.get_scene_transcript(arguments['scene_number'])
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def view_scene(self, scene_number: int) -> Dict[str, Any]:
        """View keyframes from a scene"""
        if scene_number < 1 or scene_number > len(self.scenes):
            return {"error": f"Scene {scene_number} not found"}

        scene = self.scenes[scene_number - 1]
        keyframes = self.keyframes_by_scene.get(scene_number, [])

        return {
            "scene_number": scene_number,
            "start_time": scene.start_time,
            "end_time": scene.end_time,
            "duration": scene.duration,
            "keyframe_count": len(keyframes),
            "keyframe_info": [
                {
                    "type": kf.keyframe_type,
                    "timestamp": kf.frame.timestamp,
                    "importance": kf.importance_score
                }
                for kf in keyframes
            ]
        }

    def get_transcript(self, start_time: float, end_time: float) -> Dict[str, Any]:
        """Get transcript for time range"""
        text = self.transcript.get_text_in_range(start_time, end_time)
        segments = [
            seg for seg in self.transcript.segments
            if seg.start <= end_time and seg.end >= start_time
        ]

        return {
            "start_time": start_time,
            "end_time": end_time,
            "text": text,
            "segment_count": len(segments),
            "segments": [
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text
                }
                for seg in segments
            ]
        }

    def search_dialogue(self, query: str, case_sensitive: bool = False) -> Dict[str, Any]:
        """Search for dialogue"""
        results = self.transcript.search(query, case_sensitive)

        return {
            "query": query,
            "match_count": len(results),
            "matches": [
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text
                }
                for seg in results[:10]  # Limit to 10 results
            ]
        }

    def get_scene_info(self, scene_number: int) -> Dict[str, Any]:
        """Get detailed scene information"""
        if scene_number < 1 or scene_number > len(self.scenes):
            return {"error": f"Scene {scene_number} not found"}

        scene = self.scenes[scene_number - 1]

        return {
            "scene_number": scene_number,
            "start_time": scene.start_time,
            "end_time": scene.end_time,
            "duration": scene.duration,
            "start_frame": scene.start_frame,
            "end_frame": scene.end_frame
        }

    def list_scenes(self) -> Dict[str, Any]:
        """List all scenes"""
        return {
            "total_scenes": len(self.scenes),
            "scenes": [
                {
                    "scene_number": scene.scene_number,
                    "start_time": scene.start_time,
                    "end_time": scene.end_time,
                    "duration": scene.duration
                }
                for scene in self.scenes
            ]
        }

    def get_scene_transcript(self, scene_number: int) -> Dict[str, Any]:
        """Get transcript for a scene"""
        if scene_number < 1 or scene_number > len(self.scenes):
            return {"error": f"Scene {scene_number} not found"}

        scene = self.scenes[scene_number - 1]
        return self.get_transcript(scene.start_time, scene.end_time)
