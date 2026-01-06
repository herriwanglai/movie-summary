"""Main CLI entry point for movie analysis"""

import click
from pathlib import Path
import sys

from .orchestrator.pipeline import MovieAnalysisPipeline, PipelineConfig


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Movie Summary & Analysis System

    Analyze movies using AI-powered tools with Ollama deepseek-r1:8b.
    Extract scenes, generate transcripts, create storyboards, and perform
    expert scriptwriting analysis.
    """
    pass


@cli.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--scene-threshold', default=27.0, help='Scene detection threshold')
@click.option('--keyframes', default=1, help='Keyframes per scene')
@click.option('--whisper-model', default='base', type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']),
              help='Whisper model size')
@click.option('--ollama-host', default='http://localhost:11434', help='Ollama server host')
@click.option('--ollama-model', default='deepseek-r1:8b', help='Ollama model name')
@click.option('--storyboard-format', default='pdf', type=click.Choice(['pdf', 'html', 'image']),
              help='Storyboard output format')
@click.option('--no-summary', is_flag=True, help='Skip summary generation')
@click.option('--no-script-analysis', is_flag=True, help='Skip scriptwriting analysis')
def analyze(video_path, output, scene_threshold, keyframes, whisper_model,
            ollama_host, ollama_model, storyboard_format, no_summary, no_script_analysis):
    """Analyze a movie comprehensively"""

    config = PipelineConfig(
        scene_threshold=scene_threshold,
        keyframes_per_scene=keyframes,
        whisper_model=whisper_model,
        ollama_host=ollama_host,
        ollama_model=ollama_model,
        storyboard_format=storyboard_format,
        output_dir=output,
        generate_summary=not no_summary,
        scriptwriting_analysis=not no_script_analysis
    )

    try:
        pipeline = MovieAnalysisPipeline(video_path, config)
        results = pipeline.run(verbose=True)

        click.echo(f"\n✅ Analysis complete!")
        click.echo(f"📁 Results: {results.output_dir}")

        if results.storyboard_path:
            click.echo(f"🎨 Storyboard: {results.storyboard_path}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--threshold', default=27.0, help='Scene detection threshold')
def scenes(video_path, output, threshold):
    """Detect and list scenes in a movie"""

    from .video_processor import SceneDetector

    click.echo(f"Detecting scenes in: {video_path}")

    try:
        detector = SceneDetector(video_path, threshold=threshold)
        scene_list = detector.detect_scenes()

        click.echo(f"\nFound {len(scene_list)} scenes:\n")

        for scene in scene_list:
            click.echo(f"  {scene}")

        # Save to output
        output_dir = Path(output) / Path(video_path).stem
        output_dir.mkdir(parents=True, exist_ok=True)

        import json
        scenes_data = [
            {
                "scene_number": s.scene_number,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "duration": s.duration
            }
            for s in scene_list
        ]

        output_file = output_dir / "scenes.json"
        with open(output_file, 'w') as f:
            json.dump(scenes_data, f, indent=2)

        click.echo(f"\n✅ Scenes saved to: {output_file}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--model', default='base', type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']),
              help='Whisper model size')
@click.option('--language', default=None, help='Language code (auto-detect if not specified)')
def transcribe(video_path, output, model, language):
    """Transcribe audio from a movie"""

    from .audio_processor import AudioExtractor, Transcriber

    click.echo(f"Transcribing: {video_path}")

    try:
        # Extract audio
        click.echo("Extracting audio...")
        audio_extractor = AudioExtractor(video_path)

        output_dir = Path(output) / Path(video_path).stem
        output_dir.mkdir(parents=True, exist_ok=True)

        audio_path = output_dir / "audio.wav"
        audio_extractor.extract_audio(str(audio_path))

        # Transcribe
        click.echo(f"Transcribing with Whisper ({model} model)...")
        transcriber = Transcriber(model_name=model, language=language)
        transcript = transcriber.transcribe(str(audio_path), verbose=True)

        # Save
        json_path = output_dir / "transcript.json"
        srt_path = output_dir / "transcript.srt"

        transcript.save_json(str(json_path))
        transcript.save_srt(str(srt_path))

        click.echo(f"\n✅ Transcription complete!")
        click.echo(f"📄 JSON: {json_path}")
        click.echo(f"📄 SRT: {srt_path}")
        click.echo(f"🗣️  Language: {transcript.language}")
        click.echo(f"⏱️  Duration: {transcript.duration:.1f}s")
        click.echo(f"📝 Segments: {len(transcript.segments)}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--format', default='pdf', type=click.Choice(['pdf', 'html', 'image']),
              help='Output format')
@click.option('--columns', default=3, help='Number of columns in storyboard')
def storyboard(video_path, output, format, columns):
    """Generate storyboard from a movie"""

    from .video_processor import VideoFrameExtractor, SceneDetector, KeyframeSelector
    from .storyboard import StoryboardGenerator, GridLayout, TimelineLayout

    click.echo(f"Generating storyboard for: {video_path}")

    try:
        # Detect scenes
        click.echo("Detecting scenes...")
        scene_detector = SceneDetector(video_path)
        scenes = scene_detector.detect_scenes()

        # Extract keyframes
        click.echo("Extracting keyframes...")
        video_extractor = VideoFrameExtractor(video_path)
        keyframe_selector = KeyframeSelector(video_extractor)
        keyframes = keyframe_selector.select_from_scenes(scenes, method='middle')

        # Generate storyboard
        click.echo(f"Creating {format} storyboard...")

        if columns == 1:
            layout = TimelineLayout()
        else:
            layout = GridLayout(columns=columns)

        generator = StoryboardGenerator(layout=layout, title=Path(video_path).stem)

        output_dir = Path(output) / Path(video_path).stem
        output_dir.mkdir(parents=True, exist_ok=True)

        if format == 'pdf':
            output_file = output_dir / "storyboard.pdf"
            generator.generate_pdf(keyframes, output_path=str(output_file))
        elif format == 'html':
            output_file = output_dir / "storyboard.html"
            generator.generate_html(keyframes, output_path=str(output_file))
        else:
            output_file = output_dir / "storyboard.png"
            generator.generate_image(keyframes, output_path=str(output_file))

        click.echo(f"\n✅ Storyboard created!")
        click.echo(f"🎨 {output_file}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def check():
    """Check system dependencies"""

    click.echo("Checking system dependencies...\n")

    # Check Ollama
    try:
        from .ollama_service import OllamaClient
        client = OllamaClient()
        if client.check_connection():
            click.echo("✅ Ollama: Connected")
            models = client.list_models()
            if 'deepseek-r1:8b' in models:
                click.echo("✅ deepseek-r1:8b: Available")
            else:
                click.echo("⚠️  deepseek-r1:8b: Not installed")
                click.echo("   Run: ollama pull deepseek-r1:8b")
        else:
            click.echo("❌ Ollama: Not running")
            click.echo("   Start Ollama server first")
    except Exception as e:
        click.echo(f"❌ Ollama: Error - {e}")

    # Check FFmpeg
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            click.echo("✅ FFmpeg: Installed")
        else:
            click.echo("❌ FFmpeg: Not working")
    except FileNotFoundError:
        click.echo("❌ FFmpeg: Not installed")
    except Exception as e:
        click.echo(f"❌ FFmpeg: Error - {e}")

    # Check Whisper
    try:
        import whisper
        click.echo("✅ Whisper: Installed")
    except ImportError:
        click.echo("❌ Whisper: Not installed")

    click.echo("\nSystem check complete.")


if __name__ == '__main__':
    cli()
