"""
Enhanced Analysis Workflow - How Importance Detection Works

This demonstrates the TWO-PHASE approach:
Phase 1: BEFORE deepseek watches - identify important moments
Phase 2: DURING deepseek watching - AI analyzes with context
"""

from src.video_processor import VideoFrameExtractor, SceneDetector, KeyframeSelector
from src.video_processor.importance_detector import ImportanceDetector
from src.audio_processor import AudioExtractor, Transcriber
from src.ollama_service import OllamaClient, MovieAnalyzer
from src.ollama_service.enhanced_tools import EnhancedMovieTools


def enhanced_movie_analysis(video_path: str):
    """
    Complete workflow showing BEFORE and AFTER stages
    """

    print("="*70)
    print("PHASE 1: PREPROCESSING (Before AI watches)")
    print("="*70)

    # Step 1: Extract basic structure
    print("\n1. Extracting video structure...")
    extractor = VideoFrameExtractor(video_path)
    scene_detector = SceneDetector(video_path)
    scenes = scene_detector.detect_scenes()
    print(f"   ✓ Found {len(scenes)} scenes")

    # Step 2: Get transcript
    print("\n2. Transcribing audio...")
    audio_extractor = AudioExtractor(video_path)
    audio_path = audio_extractor.extract_audio("temp_audio.wav")
    transcriber = Transcriber(model_name='base')
    transcript = transcriber.transcribe(audio_path)
    print(f"   ✓ Transcribed {len(transcript.segments)} dialogue segments")

    # Step 3: IMPORTANCE DETECTION - This is the key enhancement!
    print("\n3. 🎯 ANALYZING IMPORTANCE (New Feature!)")
    print("   This identifies exciting/important scenes BEFORE the AI watches:")

    importance_detector = ImportanceDetector(
        video_extractor=extractor,
        scenes=scenes,
        transcript=transcript
    )

    # Analyze all scenes for importance
    importance_analyses = importance_detector.analyze_all_scenes()

    print(f"   ✓ Analyzed {len(importance_analyses)} scenes for importance")
    print("\n   Top 5 Most Important Scenes (BEFORE AI analysis):")
    for i, imp in enumerate(importance_analyses[:5], 1):
        scene = scenes[imp.scene_number - 1]
        print(f"\n   {i}. Scene {imp.scene_number} ({scene.start_time:.1f}s - {scene.end_time:.1f}s)")
        print(f"      Score: {imp.importance_score:.2f}")
        print(f"      Categories: {', '.join(imp.categories)}")
        print(f"      Visual: {imp.visual_intensity:.2f} | Audio: {imp.audio_intensity:.2f}")
        for reason in imp.reasons:
            print(f"      - {reason}")

    # Step 4: Extract keyframes (prioritizing important scenes)
    print("\n4. Extracting keyframes (prioritizing important scenes)...")
    keyframe_selector = KeyframeSelector(extractor)

    # Extract MORE keyframes from important scenes
    keyframes = []
    for scene in scenes:
        imp = importance_analyses[scene.scene_number - 1]

        # Important scenes get 3 keyframes, normal scenes get 1
        if imp.importance_score > 0.7:
            kf = keyframe_selector.select_from_scene(scene, method='distributed', num_keyframes=3)
        elif imp.importance_score > 0.5:
            kf = keyframe_selector.select_from_scene(scene, method='distributed', num_keyframes=2)
        else:
            kf = keyframe_selector.select_from_scene(scene, method='middle', num_keyframes=1)

        keyframes.extend(kf)

    print(f"   ✓ Extracted {len(keyframes)} keyframes (more from important scenes)")

    print("\n" + "="*70)
    print("PHASE 2: AI ANALYSIS (Deepseek watches with context)")
    print("="*70)

    # Step 5: Create enhanced tools with pre-computed importance
    print("\n5. Initializing AI with enhanced tools...")
    enhanced_tools = EnhancedMovieTools(
        keyframes=keyframes,
        scenes=scenes,
        transcript=transcript,
        frames_dir="./frames",
        importance_analyses=importance_analyses  # Pre-computed importance!
    )

    # Initialize Ollama client
    ollama_client = OllamaClient(model='deepseek-r1:8b')
    analyzer = MovieAnalyzer(
        client=ollama_client,
        tools=enhanced_tools,
        temperature=0.7
    )

    print("\n6. 🤖 Deepseek now has access to these ENHANCED tools:")
    print("   - get_important_scenes() - See pre-analyzed important moments")
    print("   - get_climax_scenes() - Find the climax automatically")
    print("   - get_plot_structure() - Understand three-act structure")
    print("   - get_emotional_arc() - See intensity throughout movie")
    print("   - get_character_relationships() - Analyze character dynamics")
    print("   - find_character_motivation() - Understand character goals")
    print("   - view_scene() - Now includes importance metadata")

    # Step 7: AI analyzes with full context
    print("\n7. AI generating summary with importance context...")

    # The AI can now:
    # - Call get_important_scenes() to know what to focus on
    # - View those scenes with view_scene()
    # - Get character motivations and relationships
    # - Understand the plot structure

    summary = analyzer.generate_summary()

    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)

    print("\n📊 Importance Report:")
    report = importance_detector.generate_importance_report()
    print(f"   Total scenes: {report['total_scenes']}")
    print(f"   Action scenes: {report['scene_distribution']['action']}")
    print(f"   Exciting scenes: {report['scene_distribution']['exciting']}")
    print(f"   Dialogue-heavy scenes: {report['scene_distribution']['dialogue_heavy']}")

    print(f"\n📝 AI-Generated Summary:")
    print(summary)

    print("\n✅ Analysis Complete!")
    print("\nKey Difference:")
    print("- OLD: AI randomly explores scenes to find important moments")
    print("- NEW: AI knows which scenes are important BEFORE watching")
    print("       This makes analysis faster and more focused on key plot points")


# Example: How the AI uses these tools
def example_ai_workflow():
    """
    Example of how deepseek-r1:8b uses the enhanced tools
    """

    print("\n" + "="*70)
    print("EXAMPLE: How Deepseek Uses Enhanced Tools")
    print("="*70)

    print("""
When asked to summarize the movie, deepseek-r1:8b does this:

1. First, call get_important_scenes(top_n=10)
   → Gets pre-analyzed list of exciting/important scenes
   → Sees: "Scene 45 (score: 0.89) - High visual intensity, at climax position"

2. Then, call get_plot_structure()
   → Understands three-act structure
   → Knows: "Scene 15 is likely Act 1 ending, Scene 45 is climax"

3. Then, view_scene(15) and view_scene(45)
   → Views keyframes from these key moments
   → Gets importance metadata automatically

4. Call get_character_relationships("John")
   → Sees John mentioned with "Sarah" (20 times), emotional context: conflict
   → Understands relationship dynamic

5. Call find_character_motivation("John")
   → Finds dialogue: "I have to save her" → Goal identified
   → Finds: "I'm afraid of losing everything" → Fear identified

6. Generate summary with full context
   → Focuses on important scenes
   → Understands character motivations and relationships
   → Identifies plot structure and climax
   → Produces comprehensive, focused summary

OLD APPROACH:
- AI views scenes randomly
- Discovers importance through trial and error
- May miss key moments
- Takes longer

NEW APPROACH:
- AI knows what's important BEFORE viewing
- Focuses on exciting/climactic scenes
- Understands character motivations from dialogue analysis
- More efficient and comprehensive
    """)


if __name__ == "__main__":
    # Run the enhanced workflow
    # enhanced_movie_analysis("path/to/movie.mp4")

    # Show example workflow
    example_ai_workflow()
