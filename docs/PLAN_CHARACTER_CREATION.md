# Character Creation Feature - Implementation Plan

## Overview

The Character Creation feature is a **post-analysis enhancement** that activates after all AI analysis (plots, character analysis, and intimacy analysis) is complete. It creates comprehensive, exportable character profiles with visual references and AI-generated additional imagery.

## Prerequisites

Before Character Creation can run:
- [ ] Scene detection complete
- [ ] Keyframe extraction complete
- [ ] Audio transcription complete
- [ ] Plot analysis complete
- [ ] Character analysis complete
- [ ] Intimacy analysis complete

---

## Feature Architecture

### Phase 1: LLAVA Screenshot Capture System

**Purpose**: Capture high-quality screenshots of character faces, bodies, expressions, poses, and outfits using LLAVA vision model.

#### 1.1 Screenshot Types to Capture

| Type | Description | Use Case |
|------|-------------|----------|
| **Face Close-up** | Clear face shot, frontal or 3/4 angle | Identity reference |
| **Full Body** | Standing/sitting full body shot | Body type, posture |
| **Expression Set** | Various emotions (happy, sad, angry, etc.) | Expression range |
| **Pose Variations** | Action poses, gestures | Movement style |
| **Outfit Gallery** | Different costumes/clothing | Wardrobe reference |

#### 1.2 LLAVA Integration

```python
# src/character_creator/llava_capture.py

class LLAVACharacterCapture:
    """
    Uses LLAVA vision model to identify and capture character screenshots.
    """

    def __init__(self, ollama_host: str = "localhost:11434"):
        self.model = "llava"  # or llava:13b for higher quality
        self.capture_types = [
            "face_closeup",
            "full_body",
            "expression",
            "pose",
            "outfit"
        ]

    async def analyze_frame_for_character(
        self,
        frame_path: str,
        character_name: str
    ) -> dict:
        """
        Analyze a frame to detect character presence and quality.
        Returns: {
            "character_present": bool,
            "face_visible": bool,
            "face_quality": float,  # 0-1 score
            "body_visible": bool,
            "body_percentage": float,  # how much body is visible
            "expression": str,  # detected expression
            "pose": str,  # detected pose type
            "outfit_description": str
        }
        """
        pass

    async def capture_best_screenshots(
        self,
        video_path: str,
        character_name: str,
        character_appearances: list,  # timestamps where character appears
        target_counts: dict = {
            "face_closeup": 3,
            "full_body": 2,
            "expression": 5,
            "pose": 3,
            "outfit": 4
        }
    ) -> dict:
        """
        Capture the best screenshots for each type.
        """
        pass
```

#### 1.3 Frame Selection Algorithm

```
1. Get all keyframes from scenes where character appears
2. For each keyframe:
   a. Run LLAVA analysis to detect character
   b. Score frame quality (resolution, lighting, focus)
   c. Classify capture type (face/body/expression/pose/outfit)
   d. Store with metadata
3. Select top N frames per capture type
4. Extract high-resolution versions from original video
5. Save to character-specific folder
```

---

### Phase 2: Actor Metadata Web Search

**Purpose**: Find real-world information about the actor portraying the character.

#### 2.1 Data to Retrieve

```python
class ActorMetadata:
    # Basic Info
    real_name: str
    stage_name: str
    birth_date: str
    age: int
    nationality: str

    # Physical Attributes
    height: str  # e.g., "5'10\" (178 cm)"
    weight: str  # e.g., "165 lbs (75 kg)"
    eye_color: str
    hair_color: str
    body_type: str

    # Career Info
    imdb_id: str
    imdb_url: str
    filmography_highlights: list[str]
    awards: list[str]

    # Profile Pictures
    headshot_urls: list[str]
    full_body_urls: list[str]

    # Social Media
    instagram: str
    twitter: str
    official_website: str
```

#### 2.2 Web Search Integration

```python
# src/character_creator/actor_search.py

class ActorMetadataSearch:
    """
    Search web for actor information using multiple sources.
    """

    SEARCH_SOURCES = [
        "imdb.com",
        "wikipedia.org",
        "themoviedb.org",
        "rottentomatoes.com"
    ]

    async def search_actor(
        self,
        movie_title: str,
        character_name: str,
        hints: list[str] = []  # Additional search hints
    ) -> ActorMetadata:
        """
        Search for actor who plays the character.

        Strategy:
        1. Search "{movie_title} {character_name} actor"
        2. Search "{movie_title} cast"
        3. Parse IMDB/Wikipedia for structured data
        4. Download profile pictures
        """
        pass

    async def download_reference_photos(
        self,
        actor_name: str,
        save_dir: str,
        count: int = 5
    ) -> list[str]:
        """
        Download high-quality reference photos of the actor.
        """
        pass
```

#### 2.3 Search Strategy Flow

```
1. Extract movie title from video metadata/analysis
2. Get character name from character analysis
3. Search: "{movie} {character} played by actor"
4. If found:
   a. Search actor name on IMDB
   b. Parse profile page for metadata
   c. Download headshots and full body photos
5. If not found:
   a. Search movie cast list
   b. Match character name to actor
   c. Retry metadata fetch
6. Cache results to avoid repeated searches
```

---

### Phase 3: Super-Detailed JSON Prompt Structure

**Purpose**: Create a comprehensive, structured prompt that captures every detail of the character for AI image generation.

#### 3.1 JSON Schema

```json
{
  "$schema": "character_prompt_v1",
  "character": {
    "name": "string",
    "role": "protagonist|antagonist|supporting|background",
    "movie_title": "string",
    "actor": {
      "real_name": "string",
      "age_in_movie": "number",
      "ethnicity": "string"
    }
  },

  "physical_appearance": {
    "face": {
      "shape": "oval|round|square|heart|oblong",
      "skin_tone": "string",
      "eyes": {
        "color": "string",
        "shape": "string",
        "distinctive_features": ["string"]
      },
      "nose": {
        "shape": "string",
        "size": "small|medium|large"
      },
      "mouth": {
        "lip_shape": "string",
        "lip_fullness": "thin|medium|full"
      },
      "facial_hair": {
        "type": "none|stubble|beard|mustache|goatee",
        "style": "string",
        "color": "string"
      },
      "distinctive_marks": ["string"]
    },

    "hair": {
      "color": "string",
      "length": "bald|very_short|short|medium|long|very_long",
      "texture": "straight|wavy|curly|coily",
      "style": "string"
    },

    "body": {
      "height": "string",
      "build": "slim|athletic|average|muscular|heavyset",
      "posture": "string",
      "distinctive_features": ["string"]
    }
  },

  "expression_library": [
    {
      "emotion": "string",
      "description": "string",
      "screenshot_ref": "string"
    }
  ],

  "pose_library": [
    {
      "pose_type": "standing|sitting|walking|action",
      "description": "string",
      "screenshot_ref": "string"
    }
  ],

  "outfit_library": [
    {
      "outfit_name": "string",
      "scene_context": "string",
      "description": {
        "upper_body": "string",
        "lower_body": "string",
        "footwear": "string",
        "accessories": ["string"],
        "colors": ["string"],
        "style": "casual|formal|uniform|costume"
      },
      "screenshot_ref": "string"
    }
  ],

  "character_traits": {
    "personality": ["string"],
    "mannerisms": ["string"],
    "speaking_style": "string",
    "movement_style": "string"
  },

  "reference_images": {
    "movie_screenshots": {
      "face_closeups": ["path"],
      "full_body": ["path"],
      "expressions": ["path"],
      "poses": ["path"],
      "outfits": ["path"]
    },
    "actor_photos": {
      "headshots": ["url"],
      "full_body": ["url"],
      "other": ["url"]
    }
  },

  "generation_prompts": {
    "base_prompt": "string - detailed physical description",
    "style_modifiers": ["string"],
    "negative_prompt": "string - what to avoid"
  }
}
```

#### 3.2 Prompt Generation Service

```python
# src/character_creator/prompt_generator.py

class CharacterPromptGenerator:
    """
    Generates super-detailed JSON prompts from analysis data.
    """

    async def generate_prompt(
        self,
        character_analysis: dict,  # From AI character analysis
        screenshots: dict,  # From LLAVA capture
        actor_metadata: ActorMetadata,  # From web search
        intimacy_analysis: dict = None  # Optional
    ) -> dict:
        """
        Combine all data into comprehensive JSON prompt.
        """
        pass

    def generate_base_prompt(self, prompt_json: dict) -> str:
        """
        Generate a text prompt from JSON for image generation.

        Example output:
        "A 35-year-old Caucasian male with an athletic build,
        approximately 6'1\" tall. Short brown hair styled neatly
        to the side, light stubble beard. Blue-green eyes,
        strong jawline, slight cleft chin. Wearing a navy blue
        tailored suit with white shirt, no tie, collar open..."
        """
        pass
```

---

### Phase 4: Character Creation Dialog UI

**Purpose**: Present all collected data in an editable dialog for user review and submission.

#### 4.1 Dialog Layout Design

```
+------------------------------------------------------------------+
|  Character Creation - [Character Name]                      [X]  |
+------------------------------------------------------------------+
|                                                                   |
|  +-- Screenshots -----------------------------------------------+ |
|  |  [Face 1] [Face 2] [Face 3]  |  [Body 1] [Body 2]           | |
|  |  [Expr 1] [Expr 2] [Expr 3]  |  [Pose 1] [Pose 2] [Pose 3]  | |
|  |  [Outfit 1] [Outfit 2] [Outfit 3] [Outfit 4]                 | |
|  +--------------------------------------------------------------+ |
|                                                                   |
|  +-- Actor Reference -------------------------------------------+ |
|  |  [Photo 1] [Photo 2] [Photo 3]                               | |
|  |  Name: John Smith          Age: 35                           | |
|  |  Height: 6'1" (185cm)      Weight: 180 lbs (82kg)           | |
|  |  IMDB: imdb.com/name/nm123456                                | |
|  +--------------------------------------------------------------+ |
|                                                                   |
|  +-- Character Profile -----------------------------------------+ |
|  |  Physical Description:                                       | |
|  |  +--------------------------------------------------------+ | |
|  |  | [Editable text area with auto-generated description]   | | |
|  |  +--------------------------------------------------------+ | |
|  |                                                              | |
|  |  Outfit Descriptions:                                        | |
|  |  +--------------------------------------------------------+ | |
|  |  | [Editable outfit details]                              | | |
|  |  +--------------------------------------------------------+ | |
|  +--------------------------------------------------------------+ |
|                                                                   |
|  +-- JSON Prompt Preview ---------------------------------------+ |
|  |  {                                                           | |
|  |    "character": { ... },                                     | |
|  |    "physical_appearance": { ... },                           | |
|  |    ...                                                       | |
|  |  }                                                [Edit JSON]| |
|  +--------------------------------------------------------------+ |
|                                                                   |
|  [Cancel]                    [Save Draft]    [Generate Images]   |
+------------------------------------------------------------------+
```

#### 4.2 React Component Structure

```typescript
// frontend/src/components/character/CharacterCreationDialog.tsx

interface CharacterCreationDialogProps {
  videoId: number;
  characterId: number;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CharacterPromptData) => void;
}

// Sub-components:
// - ScreenshotGallery
// - ActorReferencePanel
// - CharacterProfileEditor
// - JsonPromptPreview
// - GenerationOptionsPanel
```

#### 4.3 Component Tree

```
CharacterCreationDialog
├── DialogHeader
│   ├── Title (Character Name)
│   └── CloseButton
├── DialogContent
│   ├── ScreenshotGallery
│   │   ├── CategoryTabs (Face/Body/Expression/Pose/Outfit)
│   │   ├── ImageGrid
│   │   │   └── ThumbnailCard (selectable, deletable)
│   │   └── AddMoreButton
│   ├── ActorReferencePanel
│   │   ├── PhotoGallery
│   │   ├── MetadataDisplay
│   │   └── EditMetadataButton
│   ├── CharacterProfileEditor
│   │   ├── PhysicalDescriptionTextarea
│   │   ├── OutfitDescriptionList
│   │   ├── TraitsEditor
│   │   └── AutoGenerateButton
│   └── JsonPromptPreview
│       ├── JsonViewer (collapsible)
│       ├── CopyButton
│       └── EditJsonButton
├── DialogFooter
│   ├── CancelButton
│   ├── SaveDraftButton
│   └── GenerateImagesButton
└── GenerationProgressOverlay
```

---

### Phase 5: Gemini Nanobanana Integration

**Purpose**: Submit character data to Gemini Nanobanana service to generate additional character images.

#### 5.1 Integration Architecture

```python
# src/character_creator/nanobanana_client.py

class GeminiNanobananaClient:
    """
    Client for Gemini Nanobanana image generation service.
    """

    def __init__(
        self,
        api_endpoint: str,
        api_key: str = None
    ):
        self.endpoint = api_endpoint
        self.api_key = api_key

    async def generate_character_images(
        self,
        character_prompt: dict,  # The JSON prompt
        reference_images: list[str],  # Paths to reference images
        generation_options: dict = {
            "count": 4,
            "variations": ["portrait", "full_body", "action", "casual"],
            "style": "photorealistic",
            "resolution": "1024x1024"
        }
    ) -> GenerationResult:
        """
        Submit character data for image generation.

        Returns:
        {
            "job_id": "string",
            "status": "queued|processing|completed|failed",
            "images": [
                {
                    "id": "string",
                    "url": "string",
                    "variation": "string",
                    "prompt_used": "string"
                }
            ],
            "metadata": { ... }
        }
        """
        pass

    async def check_job_status(self, job_id: str) -> dict:
        """Check the status of a generation job."""
        pass

    async def download_generated_images(
        self,
        job_id: str,
        save_dir: str
    ) -> list[str]:
        """Download completed images to local storage."""
        pass
```

#### 5.2 Submission Payload

```json
{
  "request_type": "character_generation",
  "character_prompt": { /* Full JSON prompt */ },
  "reference_images": [
    {
      "type": "movie_screenshot",
      "category": "face_closeup",
      "base64": "..."
    },
    {
      "type": "actor_photo",
      "category": "headshot",
      "url": "..."
    }
  ],
  "generation_config": {
    "count": 4,
    "variations": [
      {
        "name": "portrait",
        "prompt_modifier": "professional headshot, studio lighting"
      },
      {
        "name": "full_body",
        "prompt_modifier": "full body shot, neutral background"
      },
      {
        "name": "action",
        "prompt_modifier": "dynamic action pose, cinematic"
      },
      {
        "name": "casual",
        "prompt_modifier": "casual setting, relaxed pose"
      }
    ],
    "style": "photorealistic",
    "resolution": "1024x1024",
    "maintain_likeness": true,
    "likeness_strength": 0.85
  }
}
```

#### 5.3 API Endpoints to Add

```
POST   /api/characters/{id}/generate-images
       - Submit generation request
       - Returns: job_id

GET    /api/characters/{id}/generation-status/{job_id}
       - Check generation progress
       - Returns: status, progress, preview URLs

GET    /api/characters/{id}/generated-images
       - List all generated images for character
       - Returns: image list with metadata

DELETE /api/characters/{id}/generated-images/{image_id}
       - Delete a generated image
```

---

## Database Schema Updates

### New Tables

```python
# backend/app/models/character.py

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"))

    # Basic Info
    name = Column(String(255), nullable=False)
    role = Column(String(50))  # protagonist, antagonist, supporting
    description = Column(Text)

    # Actor Info (from web search)
    actor_name = Column(String(255))
    actor_metadata = Column(JSON)  # Full ActorMetadata as JSON

    # Generated Prompt
    prompt_json = Column(JSON)  # Full character prompt
    base_prompt_text = Column(Text)  # Generated text prompt

    # Status
    creation_status = Column(String(50), default="pending")
    # pending, capturing, searching, generating_prompt, ready, generating_images

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    video = relationship("Video", back_populates="characters")
    screenshots = relationship("CharacterScreenshot", back_populates="character")
    generated_images = relationship("CharacterGeneratedImage", back_populates="character")


class CharacterScreenshot(Base):
    __tablename__ = "character_screenshots"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))

    category = Column(String(50))  # face_closeup, full_body, expression, pose, outfit
    image_path = Column(String(500))
    timestamp = Column(Float)  # Video timestamp

    # LLAVA analysis results
    quality_score = Column(Float)
    analysis_data = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    character = relationship("Character", back_populates="screenshots")


class CharacterGeneratedImage(Base):
    __tablename__ = "character_generated_images"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))

    job_id = Column(String(100))  # Nanobanana job ID
    variation = Column(String(50))  # portrait, full_body, action, casual
    image_path = Column(String(500))
    image_url = Column(String(500))  # Original URL if applicable

    prompt_used = Column(Text)
    generation_metadata = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    character = relationship("Character", back_populates="generated_images")
```

---

## Implementation Order

### Step 1: Database & Models
1. Create Character, CharacterScreenshot, CharacterGeneratedImage models
2. Create Alembic migration
3. Add API schemas (Pydantic)

### Step 2: LLAVA Screenshot Capture
1. Implement LLAVACharacterCapture class
2. Add frame analysis methods
3. Add screenshot selection algorithm
4. Create API endpoint for capture trigger

### Step 3: Web Search Integration
1. Implement ActorMetadataSearch class
2. Add IMDB/Wikipedia parsing
3. Add photo download functionality
4. Create API endpoint for actor search

### Step 4: Prompt Generation
1. Implement CharacterPromptGenerator class
2. Create JSON schema validation
3. Add text prompt generation
4. Create API endpoint for prompt generation

### Step 5: Dialog UI
1. Create CharacterCreationDialog component
2. Implement sub-components (galleries, editors)
3. Add Zustand store for character creation state
4. Connect to backend APIs

### Step 6: Nanobanana Integration
1. Implement GeminiNanobananaClient class
2. Add job status polling
3. Add image download functionality
4. Create API endpoints for generation
5. Add generation progress UI

---

## File Structure

```
src/
├── character_creator/
│   ├── __init__.py
│   ├── llava_capture.py      # LLAVA screenshot capture
│   ├── actor_search.py       # Web search for actor info
│   ├── prompt_generator.py   # JSON prompt generation
│   └── nanobanana_client.py  # Gemini Nanobanana client

backend/app/
├── models/
│   └── character.py          # Character database models
├── schemas/
│   └── character.py          # Pydantic schemas
├── routers/
│   └── characters.py         # Character API endpoints
└── services/
    └── character_service.py  # Business logic

frontend/src/
├── components/
│   └── character/
│       ├── CharacterCreationDialog.tsx
│       ├── ScreenshotGallery.tsx
│       ├── ActorReferencePanel.tsx
│       ├── CharacterProfileEditor.tsx
│       ├── JsonPromptPreview.tsx
│       └── GenerationProgressOverlay.tsx
└── stores/
    └── characterStore.ts     # Character creation state
```

---

## Configuration

```python
# backend/app/config.py additions

class Settings(BaseSettings):
    # LLAVA settings
    LLAVA_MODEL: str = "llava:13b"
    LLAVA_HOST: str = "localhost:11434"

    # Web search settings
    WEB_SEARCH_ENABLED: bool = True
    IMDB_API_KEY: str = None  # Optional

    # Nanobanana settings
    NANOBANANA_ENDPOINT: str = "http://localhost:5000"
    NANOBANANA_API_KEY: str = None

    # Character creation settings
    MAX_SCREENSHOTS_PER_CATEGORY: int = 5
    CHARACTER_IMAGES_DIR: str = "characters"
```

---

## Success Criteria

1. **LLAVA Capture**: Successfully captures categorized screenshots with quality scoring
2. **Actor Search**: Retrieves accurate metadata from web sources
3. **Prompt Generation**: Creates comprehensive, valid JSON prompts
4. **Dialog UI**: User-friendly interface for review and editing
5. **Image Generation**: Successfully submits to Nanobanana and retrieves generated images
6. **Integration**: Seamlessly integrates with existing analysis pipeline

---

## Dependencies to Add

```python
# requirements.txt additions
beautifulsoup4>=4.12.0    # Web scraping for actor info
aiohttp>=3.9.0            # Async HTTP client for web search
imdbpy>=2022.7.9          # IMDB data access (optional)
```

```json
// package.json additions
{
  "dependencies": {
    "react-json-view": "^1.21.3",  // JSON viewer component
    "react-image-gallery": "^1.3.0"  // Image gallery component
  }
}
```

---

## Notes

- This feature depends on completed AI analysis - ensure analysis status checks are in place
- LLAVA model should be pre-downloaded in Ollama
- Web search may require rate limiting to avoid blocks
- Nanobanana API details need to be confirmed
- Consider caching actor metadata to reduce repeated searches
