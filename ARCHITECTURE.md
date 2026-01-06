# Movie Analysis System Architecture

## Overview
A multi-agent system for analyzing movies using Ollama deepseek-r1:8b with video processing, transcription, and scriptwriting analysis capabilities.

## System Components

### 1. Video Processing Module (`src/video_processor/`)
**Purpose**: Extract visual information from movies
- **Scene Detector**: Identify scene boundaries using content-based analysis
- **Keyframe Extractor**: Extract representative frames from each scene
- **Frame Sampler**: Sample frames at regular intervals
- **Metadata Extractor**: Get video properties (duration, resolution, fps)

**Tech Stack**:
- `opencv-python` for frame extraction
- `scenedetect` for scene detection
- `ffmpeg-python` for video manipulation

### 2. Audio Processing Module (`src/audio_processor/`)
**Purpose**: Extract and transcribe audio
- **Audio Extractor**: Extract audio track from video
- **Transcription Service**: Convert speech to text with timestamps
- **Speaker Diarization**: Identify different speakers (optional)

**Tech Stack**:
- `ffmpeg` for audio extraction
- `whisper` or `faster-whisper` for transcription
- `pyannote.audio` for speaker diarization (optional)

### 3. Ollama Integration (`src/ollama_service/`)
**Purpose**: Interface with deepseek-r1:8b for analysis
- **Connection Manager**: Handle Ollama API communication
- **Tool Definitions**: Define tools for movie viewing/analysis
- **Context Manager**: Manage large context from movies
- **Prompt Templates**: Pre-built prompts for different analysis types

**Features**:
- Movie summarization
- Scene description
- Character analysis
- Thematic analysis
- Visual storytelling assessment

### 4. Storyboard Generator (`src/storyboard/`)
**Purpose**: Create visual storyboards
- **Layout Engine**: Arrange keyframes in grid/timeline format
- **Caption Generator**: Add scene descriptions and timestamps
- **Export System**: Generate PDF, HTML, or image outputs

**Tech Stack**:
- `Pillow` for image composition
- `reportlab` for PDF generation
- `jinja2` for HTML templates

### 5. Scriptwriting Analysis Agent (`src/scriptwriting_agent/`)
**Purpose**: Provide expert scriptwriting analysis
- **Structure Analyzer**: Analyze three-act structure, pacing
- **Character Analyzer**: Evaluate character development
- **Dialogue Analyzer**: Assess dialogue quality
- **Theme Analyzer**: Identify and analyze themes
- **Feedback Generator**: Provide constructive analysis

**Knowledge Base**:
- Scriptwriting principles (Save the Cat, Hero's Journey, etc.)
- Film analysis frameworks
- Industry standards

### 6. Multi-Agent Orchestrator (`src/orchestrator/`)
**Purpose**: Coordinate all components
- **Pipeline Manager**: Execute analysis workflow
- **Agent Coordinator**: Manage communication between agents
- **State Manager**: Track analysis progress
- **Results Aggregator**: Combine outputs from all agents

## Data Flow

```
Movie File (MP4/MKV/etc)
    |
    v
[Video Processor] --> Keyframes, Scenes
    |
    v
[Audio Processor] --> Transcript with Timestamps
    |
    v
[Ollama Service] --> Movie Summary, Analysis
    |
    v
[Storyboard Generator] --> Visual Storyboard
    |
    v
[Scriptwriting Agent] --> Expert Analysis & Feedback
    |
    v
Final Report (JSON/PDF/HTML)
```

## Agent Communication

### Primary Agent (Ollama + deepseek-r1:8b)
- **Input**: Video frames, transcript, metadata
- **Output**: Summary, scene descriptions, insights
- **Tools**:
  - `view_frame(frame_id)` - View specific frame
  - `view_scene(scene_id)` - View scene keyframes
  - `get_transcript(start_time, end_time)` - Get transcript segment
  - `analyze_character(name)` - Deep dive on character

### Scriptwriting Agent
- **Input**: Primary agent's analysis, transcript, storyboard
- **Output**: Structural analysis, recommendations
- **Analysis Dimensions**:
  - Story structure and pacing
  - Character arcs
  - Dialogue effectiveness
  - Visual storytelling
  - Thematic coherence

## Configuration

### Video Processing Settings
- Scene detection threshold (sensitivity)
- Keyframe extraction rate
- Frame sampling interval
- Output resolution for frames

### Transcription Settings
- Model selection (tiny, base, small, medium, large)
- Language
- Speaker diarization on/off

### Ollama Settings
- Model: deepseek-r1:8b
- Temperature
- Context window management
- Tool calling configuration

## Output Formats

1. **JSON Report**: Complete structured analysis
2. **PDF Report**: Human-readable with storyboard
3. **HTML Dashboard**: Interactive web view
4. **Storyboard Images**: Visual scene breakdown

## Extensibility

- **Plugin System**: Add custom analyzers
- **Custom Tools**: Define additional tools for Ollama
- **Export Formats**: Add new output formats
- **Model Flexibility**: Support different Ollama models

## Performance Considerations

- **Chunking**: Process long movies in segments
- **Caching**: Cache extracted frames and transcripts
- **Parallel Processing**: Process scenes in parallel where possible
- **GPU Acceleration**: Use GPU for video processing and transcription
