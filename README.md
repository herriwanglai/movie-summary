# Movie Summary & Analysis System

An intelligent multi-agent system for comprehensive movie analysis using Ollama deepseek-r1:8b. Automatically processes videos to generate summaries, storyboards, transcripts, and expert scriptwriting analysis.

## Features

- 🎬 **Video Processing**: Automatic scene detection and keyframe extraction
- 🎤 **Transcription**: Speech-to-text with timestamps using Whisper
- 🤖 **AI Analysis**: Deep movie analysis using Ollama deepseek-r1:8b
- 📊 **Storyboard Generation**: Visual storyboards with scene breakdowns
- ✍️ **Scriptwriting Analysis**: Expert analysis of story structure, characters, and themes
- 📄 **Multiple Outputs**: JSON, PDF, and HTML reports

## System Architecture

The system consists of several specialized components:

1. **Video Processor**: Extracts frames, detects scenes, identifies keyframes
2. **Audio Processor**: Extracts and transcribes audio with timestamps
3. **Ollama Service**: Interfaces with deepseek-r1:8b for intelligent analysis
4. **Storyboard Generator**: Creates visual storyboards from keyframes
5. **Scriptwriting Agent**: Provides expert scriptwriting analysis
6. **Orchestrator**: Coordinates all components in a unified pipeline

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

## Prerequisites

- Python 3.10+
- FFmpeg (for video/audio processing)
- Ollama with deepseek-r1:8b model installed
- GPU recommended for faster processing

## Installation

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 2. Install Ollama and deepseek-r1:8b

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the deepseek-r1:8b model
ollama pull deepseek-r1:8b
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```bash
# Analyze a movie
python -m src.main analyze movie.mp4

# With custom output directory
python -m src.main analyze movie.mp4 --output ./results

# Generate only storyboard
python -m src.main storyboard movie.mp4

# Get transcript only
python -m src.main transcribe movie.mp4
```

### Python API

```python
from src.orchestrator.pipeline import MovieAnalysisPipeline

# Initialize pipeline
pipeline = MovieAnalysisPipeline(
    video_path="movie.mp4",
    output_dir="./results"
)

# Run complete analysis
results = pipeline.run()

# Access components
print(results.summary)
print(results.transcript)
results.storyboard.save_pdf("storyboard.pdf")
```

## Configuration

Create a `.env` file or `config.yaml`:

```yaml
# Ollama Configuration
ollama:
  host: http://localhost:11434
  model: deepseek-r1:8b
  temperature: 0.7

# Video Processing
video:
  scene_threshold: 27.0  # Sensitivity for scene detection
  keyframe_interval: 30  # Extract keyframe every N frames
  max_resolution: 1920   # Downscale to this width

# Transcription
audio:
  model: base            # whisper model: tiny/base/small/medium/large
  language: en           # or 'auto' for detection

# Storyboard
storyboard:
  columns: 3
  include_captions: true
  format: pdf            # pdf, html, or images
```

## Output Structure

```
output/
├── movie_name/
│   ├── frames/           # Extracted keyframes
│   ├── scenes/           # Scene metadata
│   ├── transcript.json   # Full transcript with timestamps
│   ├── analysis.json     # AI analysis results
│   ├── storyboard.pdf    # Visual storyboard
│   ├── report.html       # Interactive HTML report
│   └── script_analysis.md # Scriptwriting analysis
```

## Examples

See the `examples/` directory for:
- Basic movie analysis
- Custom tool definitions for Ollama
- Integrating with other agents
- Batch processing multiple movies

## Tools for Ollama Agent

The system provides these tools to the deepseek-r1:8b agent:

- `view_frame(frame_id)` - View a specific frame
- `view_scene(scene_id)` - View keyframes from a scene
- `get_transcript(start, end)` - Get transcript segment
- `search_dialogue(query)` - Search for specific dialogue
- `analyze_character(name)` - Deep character analysis
- `compare_scenes(scene1, scene2)` - Compare two scenes

## Advanced Usage

### Custom Scriptwriting Analysis

```python
from src.scriptwriting_agent.analyzer import ScriptwritingAnalyzer

analyzer = ScriptwritingAnalyzer()
analysis = analyzer.analyze(
    transcript=transcript,
    scenes=scenes,
    summary=ollama_summary
)

print(analysis.structure_score)
print(analysis.character_development)
print(analysis.recommendations)
```

### Multi-Agent Coordination

```python
from src.orchestrator.multi_agent import MultiAgentCoordinator

coordinator = MultiAgentCoordinator()
coordinator.add_agent("summarizer", ollama_agent)
coordinator.add_agent("scriptwriter", scriptwriting_agent)

results = coordinator.execute_workflow(video_path)
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
```

## Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama service
ollama serve
```

### GPU/CUDA Issues
```bash
# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Support for streaming services (with proper authorization)
- [ ] Real-time analysis mode
- [ ] Multi-language support
- [ ] Character face recognition
- [ ] Music and sound analysis
- [ ] Comparison mode for multiple movies
- [ ] Export to screenplay format

## Acknowledgments

- Ollama team for the amazing inference engine
- DeepSeek for the reasoning model
- OpenAI Whisper for transcription
- PySceneDetect for scene detection
