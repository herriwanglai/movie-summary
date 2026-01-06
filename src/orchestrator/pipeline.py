"""Main pipeline for movie analysis"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import json
from tqdm import tqdm

from ..video_processor import VideoFrameExtractor, SceneDetector, KeyframeSelector
from ..audio_processor import AudioExtractor, Transcriber
from ..ollama_service import OllamaClient, MovieAnalysisTools, MovieAnalyzer
from ..storyboard import StoryboardGenerator, GridLayout
from ..scriptwriting_agent import ScriptwritingAnalyzer


@dataclass
class PipelineConfig:
    """Configuration for analysis pipeline"""
    # Video processing
    scene_threshold: float = 27.0
    keyframes_per_scene: int = 1
    keyframe_method: str = 'middle'
    max_resolution: int = 1920

    # Audio/Transcription
    whisper_model: str = 'base'
    transcription_language: Optional[str] = None

    # Ollama
    ollama_host: str = 'http://localhost:11434'
    ollama_model: str = 'deepseek-r1:8b'
    temperature: float = 0.7

    # Storyboard
    storyboard_format: str = 'pdf'  # 'pdf', 'html', 'image'
    storyboard_columns: int = 3

    # Analysis
    generate_summary: bool = True
    analyze_scenes: bool = True
    scriptwriting_analysis: bool = True

    # Output
    output_dir: str = './output'


@dataclass
class AnalysisResults:
    """Results from movie analysis"""
    video_path: str
    output_dir: str
    scenes: list
    keyframes: list
    transcript: Any
    summary: Optional[str] = None
    scene_descriptions: Optional[List[Dict]] = None
    themes: Optional[List[Dict]] = None
    script_analysis: Optional[Any] = None
    storyboard_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MovieAnalysisPipeline:
    """Complete movie analysis pipeline"""

    def __init__(
        self,
        video_path: str,
        config: Optional[PipelineConfig] = None
    ):
        """
        Initialize pipeline

        Args:
            video_path: Path to video file
            config: Pipeline configuration
        """
        self.video_path = Path(video_path)
        self.config = config or PipelineConfig()

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        # Setup output directory
        self.output_dir = Path(self.config.output_dir) / self.video_path.stem
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize all pipeline components"""
        print("Initializing components...")

        # Video processing
        self.video_extractor = VideoFrameExtractor(
            str(self.video_path),
            max_resolution=self.config.max_resolution
        )
        self.scene_detector = SceneDetector(
            str(self.video_path),
            threshold=self.config.scene_threshold
        )
        self.keyframe_selector = KeyframeSelector(self.video_extractor)

        # Audio processing
        self.audio_extractor = AudioExtractor(str(self.video_path))
        self.transcriber = Transcriber(
            model_name=self.config.whisper_model,
            language=self.config.transcription_language
        )

        # Ollama (check connection)
        self.ollama_client = OllamaClient(
            host=self.config.ollama_host,
            model=self.config.ollama_model
        )

        if not self.ollama_client.check_connection():
            print("Warning: Ollama server not available. AI features will be limited.")
            self.ollama_client = None

        # Storyboard generator
        from ..storyboard.layout import GridLayout, TimelineLayout, CompactLayout

        if self.config.storyboard_columns == 1:
            layout = TimelineLayout()
        elif self.config.storyboard_columns >= 4:
            layout = CompactLayout()
        else:
            layout = GridLayout(columns=self.config.storyboard_columns)

        self.storyboard_generator = StoryboardGenerator(
            layout=layout,
            title=f"Storyboard: {self.video_path.stem}"
        )

        # Scriptwriting analyzer
        self.script_analyzer = ScriptwritingAnalyzer(
            ollama_client=self.ollama_client
        )

    def run(self, verbose: bool = True) -> AnalysisResults:
        """
        Run complete analysis pipeline

        Args:
            verbose: Show progress

        Returns:
            AnalysisResults object
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Analyzing: {self.video_path.name}")
            print(f"{'='*60}\n")

        # Step 1: Extract video metadata
        if verbose:
            print("📹 Extracting video metadata...")
        metadata = self._extract_metadata()

        # Step 2: Detect scenes
        if verbose:
            print("🎬 Detecting scenes...")
        scenes = self._detect_scenes()
        if verbose:
            print(f"   Found {len(scenes)} scenes")

        # Step 3: Extract keyframes
        if verbose:
            print("🖼️  Extracting keyframes...")
        keyframes = self._extract_keyframes(scenes)
        if verbose:
            print(f"   Extracted {len(keyframes)} keyframes")

        # Step 4: Extract and transcribe audio
        if verbose:
            print("🎤 Extracting and transcribing audio...")
        transcript = self._transcribe_audio()
        if verbose:
            print(f"   Transcribed {len(transcript.segments)} segments")

        # Step 5: Initialize tools for Ollama
        frames_dir = self.output_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        self.keyframe_selector.save_keyframes(keyframes, str(frames_dir))

        movie_tools = MovieAnalysisTools(
            keyframes=keyframes,
            scenes=scenes,
            transcript=transcript,
            frames_dir=str(frames_dir)
        )

        # Step 6: Generate summary (if enabled and Ollama available)
        summary = None
        if self.config.generate_summary and self.ollama_client:
            if verbose:
                print("📝 Generating movie summary...")
            summary = self._generate_summary(movie_tools)

        # Step 7: Generate scene descriptions (if enabled)
        scene_descriptions = None
        if self.config.analyze_scenes and self.ollama_client:
            if verbose:
                print("📋 Analyzing scenes...")
            scene_descriptions = self._analyze_scenes(movie_tools)

        # Step 8: Generate storyboard
        if verbose:
            print("🎨 Generating storyboard...")
        storyboard_path = self._generate_storyboard(
            keyframes,
            scene_descriptions,
            metadata
        )

        # Step 9: Scriptwriting analysis
        script_analysis = None
        if self.config.scriptwriting_analysis:
            if verbose:
                print("✍️  Performing scriptwriting analysis...")
            script_analysis = self._scriptwriting_analysis(
                scenes,
                transcript,
                summary or "No summary available"
            )

        # Step 10: Save all results
        if verbose:
            print("💾 Saving results...")
        self._save_results(
            scenes, transcript, summary,
            scene_descriptions, script_analysis, metadata
        )

        if verbose:
            print(f"\n{'='*60}")
            print(f"✅ Analysis complete!")
            print(f"📁 Results saved to: {self.output_dir}")
            print(f"{'='*60}\n")

        return AnalysisResults(
            video_path=str(self.video_path),
            output_dir=str(self.output_dir),
            scenes=scenes,
            keyframes=keyframes,
            transcript=transcript,
            summary=summary,
            scene_descriptions=scene_descriptions,
            script_analysis=script_analysis,
            storyboard_path=storyboard_path,
            metadata=metadata
        )

    def _extract_metadata(self) -> Dict[str, Any]:
        """Extract video metadata"""
        metadata = self.video_extractor.metadata
        return {
            "filename": self.video_path.name,
            "duration": metadata.duration,
            "fps": metadata.fps,
            "resolution": f"{metadata.width}x{metadata.height}",
            "frame_count": metadata.frame_count
        }

    def _detect_scenes(self) -> list:
        """Detect scenes"""
        return self.scene_detector.detect_scenes()

    def _extract_keyframes(self, scenes: list) -> list:
        """Extract keyframes from scenes"""
        return self.keyframe_selector.select_from_scenes(
            scenes,
            keyframes_per_scene=self.config.keyframes_per_scene,
            method=self.config.keyframe_method
        )

    def _transcribe_audio(self):
        """Extract and transcribe audio"""
        # Extract audio
        audio_path = self.output_dir / "audio.wav"
        self.audio_extractor.extract_audio(str(audio_path))

        # Transcribe
        transcript = self.transcriber.transcribe(str(audio_path))

        # Save transcript
        transcript.save_json(str(self.output_dir / "transcript.json"))
        transcript.save_srt(str(self.output_dir / "transcript.srt"))

        return transcript

    def _generate_summary(self, tools: MovieAnalysisTools) -> str:
        """Generate movie summary"""
        analyzer = MovieAnalyzer(
            client=self.ollama_client,
            tools=tools,
            temperature=self.config.temperature
        )
        return analyzer.generate_summary()

    def _analyze_scenes(self, tools: MovieAnalysisTools) -> List[Dict]:
        """Analyze scenes"""
        analyzer = MovieAnalyzer(
            client=self.ollama_client,
            tools=tools,
            temperature=self.config.temperature
        )
        return analyzer.generate_scene_descriptions()

    def _generate_storyboard(
        self,
        keyframes: list,
        scene_descriptions: Optional[List[Dict]],
        metadata: dict
    ) -> str:
        """Generate storyboard"""
        captions = None
        if scene_descriptions:
            captions = [desc.get('description', '') for desc in scene_descriptions]

        if self.config.storyboard_format == 'pdf':
            output_path = self.output_dir / "storyboard.pdf"
            return self.storyboard_generator.generate_pdf(
                keyframes, captions, metadata, str(output_path)
            )
        elif self.config.storyboard_format == 'html':
            output_path = self.output_dir / "storyboard.html"
            return self.storyboard_generator.generate_html(
                keyframes, captions, metadata, str(output_path)
            )
        else:  # image
            output_path = self.output_dir / "storyboard.png"
            return self.storyboard_generator.generate_image(
                keyframes, captions, str(output_path)
            )

    def _scriptwriting_analysis(self, scenes: list, transcript, summary: str):
        """Perform scriptwriting analysis"""
        analysis = self.script_analyzer.analyze(
            scenes=scenes,
            transcript=transcript,
            summary=summary
        )

        # Save analysis
        analysis.save_json(str(self.output_dir / "script_analysis.json"))
        analysis.save_markdown(str(self.output_dir / "script_analysis.md"))

        return analysis

    def _save_results(
        self,
        scenes,
        transcript,
        summary,
        scene_descriptions,
        script_analysis,
        metadata
    ):
        """Save all results"""
        # Save scenes metadata
        scenes_data = [
            {
                "scene_number": s.scene_number,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "duration": s.duration,
                "start_frame": s.start_frame,
                "end_frame": s.end_frame
            }
            for s in scenes
        ]

        with open(self.output_dir / "scenes.json", 'w') as f:
            json.dump(scenes_data, f, indent=2)

        # Save summary
        if summary:
            with open(self.output_dir / "summary.txt", 'w') as f:
                f.write(summary)

        # Save scene descriptions
        if scene_descriptions:
            with open(self.output_dir / "scene_descriptions.json", 'w') as f:
                json.dump(scene_descriptions, f, indent=2)

        # Save complete metadata
        with open(self.output_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
