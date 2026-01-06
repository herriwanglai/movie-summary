"""Basic usage example for movie analysis"""

from src.orchestrator.pipeline import MovieAnalysisPipeline, PipelineConfig

# Configure the pipeline
config = PipelineConfig(
    scene_threshold=27.0,
    keyframes_per_scene=1,
    whisper_model='base',
    ollama_host='http://localhost:11434',
    ollama_model='deepseek-r1:8b',
    storyboard_format='pdf',
    output_dir='./output'
)

# Create and run pipeline
pipeline = MovieAnalysisPipeline(
    video_path='path/to/your/movie.mp4',
    config=config
)

results = pipeline.run(verbose=True)

# Access results
print(f"Summary: {results.summary}")
print(f"Total scenes: {len(results.scenes)}")
print(f"Storyboard: {results.storyboard_path}")

# Script analysis
if results.script_analysis:
    print(f"Overall score: {results.script_analysis.overall_score}/10")
    print(f"Strengths: {results.script_analysis.strengths}")
    print(f"Recommendations: {results.script_analysis.recommendations}")
