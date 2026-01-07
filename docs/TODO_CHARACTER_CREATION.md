# Character Creation - Implementation TODO

## Overview
Post-AI-analysis feature to create detailed character profiles with screenshots, actor metadata, and AI image generation.

---

## Prerequisites Checklist
- [ ] All AI analysis complete (plot, character, intimacy)
- [ ] LLAVA model available in Ollama
- [ ] Gemini Nanobanana endpoint configured

---

## Phase 1: Database & Backend Foundation

### 1.1 Database Models
- [ ] Create `Character` model
  - [ ] Fields: name, role, actor_name, actor_metadata (JSON), prompt_json, base_prompt_text, creation_status
  - [ ] Relationships to Video
- [ ] Create `CharacterScreenshot` model
  - [ ] Fields: character_id, category, image_path, timestamp, quality_score, analysis_data
- [ ] Create `CharacterGeneratedImage` model
  - [ ] Fields: character_id, job_id, variation, image_path, prompt_used, generation_metadata
- [ ] Create Alembic migration
- [ ] Test database operations

### 1.2 Pydantic Schemas
- [ ] CharacterCreate schema
- [ ] CharacterResponse schema
- [ ] CharacterScreenshotResponse schema
- [ ] CharacterGeneratedImageResponse schema
- [ ] CharacterPromptData schema

### 1.3 API Endpoints (FastAPI Router)
- [ ] `POST /api/characters` - Create character
- [ ] `GET /api/characters` - List characters
- [ ] `GET /api/videos/{id}/characters` - Characters in video
- [ ] `GET /api/characters/{id}` - Get character details
- [ ] `PUT /api/characters/{id}` - Update character
- [ ] `DELETE /api/characters/{id}` - Delete character

---

## Phase 2: LLAVA Screenshot Capture System

### 2.1 Core Implementation
- [ ] Create `src/character_creator/__init__.py`
- [ ] Create `src/character_creator/llava_capture.py`
  - [ ] `LLAVACharacterCapture` class
  - [ ] `analyze_frame_for_character()` method
  - [ ] `capture_best_screenshots()` method
  - [ ] Frame quality scoring algorithm

### 2.2 Screenshot Categories
- [ ] Face close-up detection
- [ ] Full body detection
- [ ] Expression classification
- [ ] Pose detection
- [ ] Outfit identification

### 2.3 API Integration
- [ ] `POST /api/characters/{id}/capture-screenshots` endpoint
- [ ] Background task for screenshot capture
- [ ] Progress tracking

---

## Phase 3: Actor Web Search Integration

### 3.1 Core Implementation
- [ ] Create `src/character_creator/actor_search.py`
  - [ ] `ActorMetadataSearch` class
  - [ ] `search_actor()` method
  - [ ] `download_reference_photos()` method

### 3.2 Data Sources
- [ ] IMDB integration
- [ ] Wikipedia parsing
- [ ] TMDb API (optional)
- [ ] Photo download & caching

### 3.3 Metadata Fields
- [ ] Real name, stage name
- [ ] Birth date, age, nationality
- [ ] Height, weight, physical attributes
- [ ] Filmography highlights
- [ ] Profile picture URLs

### 3.4 API Integration
- [ ] `POST /api/characters/{id}/search-actor` endpoint
- [ ] `GET /api/characters/{id}/actor-metadata` endpoint

---

## Phase 4: JSON Prompt Generation

### 4.1 Core Implementation
- [ ] Create `src/character_creator/prompt_generator.py`
  - [ ] `CharacterPromptGenerator` class
  - [ ] `generate_prompt()` method
  - [ ] `generate_base_prompt()` text method

### 4.2 JSON Schema Structure
- [ ] Character basic info section
- [ ] Physical appearance section
  - [ ] Face details (shape, eyes, nose, mouth, facial hair)
  - [ ] Hair details
  - [ ] Body details
- [ ] Expression library
- [ ] Pose library
- [ ] Outfit library
- [ ] Character traits
- [ ] Reference images section
- [ ] Generation prompts section

### 4.3 API Integration
- [ ] `POST /api/characters/{id}/generate-prompt` endpoint
- [ ] `PUT /api/characters/{id}/prompt` endpoint (manual edits)

---

## Phase 5: Frontend Fullscreen Workspace UI

> **See detailed UI spec**: `docs/UI_CHARACTER_CREATION.md`

### 5.1 Main Layout Components
- [ ] Create `frontend/src/components/character/` directory
- [ ] `CharacterWorkspace.tsx` - Fullscreen container (`h-screen flex`)
- [ ] `CharacterSidebar.tsx` - Left sidebar (240px fixed width)
- [ ] `CharacterListItem.tsx` - Avatar + name + role badge
- [ ] `NodeGrid.tsx` - Responsive grid for character nodes

### 5.2 Character Node Components
- [ ] `nodes/BaseNode.tsx` - Shared node wrapper with expand/collapse
- [ ] `nodes/FaceNode.tsx` - Face screenshots gallery
- [ ] `nodes/BodyNode.tsx` - Full body screenshots
- [ ] `nodes/ExpressionNode.tsx` - Expression variations
- [ ] `nodes/PoseNode.tsx` - Pose screenshots
- [ ] `nodes/OutfitNode.tsx` - Outfit gallery
- [ ] `nodes/ActorNode.tsx` - Actor metadata + reference photos
- [ ] `nodes/PromptNode.tsx` - JSON prompt preview/editor

### 5.3 Chatbox Components
- [ ] `CharacterChatbox.tsx` - Main chat container (resizable)
- [ ] `ChatMessage.tsx` - Message bubble with action buttons
- [ ] `QuickActionBar.tsx` - Quick action buttons (Describe face, Find actor, etc.)
- [ ] AI integration with Ollama for character refinement

### 5.4 Action Components
- [ ] `GenerateButton.tsx` - Prominent CTA with validation
- [ ] `GenerationProgress.tsx` - Modal with progress tracking
- [ ] `ImageCaptureModal.tsx` - Video scrubber for manual capture

### 5.5 State Management
- [ ] Create `frontend/src/stores/characterStore.ts`
  - [ ] `characters[]` - All characters list
  - [ ] `selectedCharacterId` - Currently selected
  - [ ] `currentCharacter` - Full character data
  - [ ] `screenshots` - Categorized screenshots object
  - [ ] `actorMetadata` - Actor info from web search
  - [ ] `promptJson` - Generated JSON prompt
  - [ ] `chatMessages[]` - Chat history
  - [ ] `generationStatus` - idle/validating/generating/complete/error
  - [ ] `expandedNodes[]` - Which nodes are expanded
  - [ ] Actions: selectCharacter, addScreenshot, sendChatMessage, generateImages, etc.

### 5.6 TypeScript Types
- [ ] Create `frontend/src/types/character.ts`
  - [ ] `Character` interface
  - [ ] `Screenshot` interface
  - [ ] `ActorMetadata` interface
  - [ ] `CharacterPrompt` interface
  - [ ] `ChatMessage` interface
  - [ ] `GeneratedImage` interface

### 5.7 UI Features
- [ ] Left sidebar with face avatar thumbnails
- [ ] 7 node types in responsive grid (2-4 columns)
- [ ] Expandable/collapsible nodes
- [ ] AI chatbox with quick actions
- [ ] Chat message action buttons (Apply to Prompt, Edit, Regenerate)
- [ ] Generate button with pre-validation checklist
- [ ] Loading and progress states
- [ ] Toast notifications for actions

### 5.8 Interaction Flows
- [ ] Character selection → loads nodes + resets chat
- [ ] Capture more screenshots → modal with video scrubber
- [ ] Chat interaction → AI response with apply actions
- [ ] Generate images → validation → progress → results

---

## Phase 6: Gemini Nanobanana Integration

### 6.1 Core Implementation
- [ ] Create `src/character_creator/nanobanana_client.py`
  - [ ] `GeminiNanobananaClient` class
  - [ ] `generate_character_images()` method
  - [ ] `check_job_status()` method
  - [ ] `download_generated_images()` method

### 6.2 Generation Options
- [ ] Portrait variation
- [ ] Full body variation
- [ ] Action pose variation
- [ ] Casual setting variation
- [ ] Custom variation support

### 6.3 API Integration
- [ ] `POST /api/characters/{id}/generate-images` endpoint
- [ ] `GET /api/characters/{id}/generation-status/{job_id}` endpoint
- [ ] `GET /api/characters/{id}/generated-images` endpoint
- [ ] `DELETE /api/characters/{id}/generated-images/{image_id}` endpoint

### 6.4 Job Management
- [ ] Queue generation job
- [ ] Poll for status
- [ ] Handle completion callback
- [ ] Download and store images
- [ ] Error handling & retry logic

---

## Phase 7: Integration & Testing

### 7.1 Pipeline Integration
- [ ] Hook into post-analysis workflow
- [ ] Auto-trigger character creation after analysis
- [ ] Status tracking in Video model

### 7.2 Testing
- [ ] Unit tests for LLAVA capture
- [ ] Unit tests for actor search
- [ ] Unit tests for prompt generation
- [ ] Integration tests for full workflow
- [ ] E2E tests for UI dialog

### 7.3 Documentation
- [ ] API documentation
- [ ] User guide
- [ ] Configuration guide

---

## Configuration Updates

### Backend Config
```python
LLAVA_MODEL = "llava:13b"
LLAVA_HOST = "localhost:11434"
WEB_SEARCH_ENABLED = True
NANOBANANA_ENDPOINT = "http://localhost:5000"
NANOBANANA_API_KEY = ""
MAX_SCREENSHOTS_PER_CATEGORY = 5
CHARACTER_IMAGES_DIR = "characters"
```

### Dependencies
```
# Python
beautifulsoup4>=4.12.0
aiohttp>=3.9.0

# JavaScript
react-json-view
react-image-gallery
```

---

## Estimated Complexity

| Phase | Complexity | Files | Description |
|-------|------------|-------|-------------|
| 1 | Medium | 6-8 | Database models, schemas, basic API |
| 2 | High | 3-4 | LLAVA integration, frame analysis |
| 3 | Medium | 2-3 | Web scraping, API parsing |
| 4 | Medium | 2-3 | JSON schema, prompt generation |
| 5 | **Very High** | **15-20** | Fullscreen workspace, 7 nodes, chatbox, state |
| 6 | Medium | 3-4 | External API integration |
| 7 | Medium | 5-6 | Testing, documentation |

---

## Notes

1. **Dependency**: Requires completed AI analysis before activation
2. **LLAVA**: Must be pulled in Ollama (`ollama pull llava:13b`)
3. **Web Search**: Implement rate limiting to avoid blocks
4. **Nanobanana**: Confirm API specification and authentication
5. **Storage**: Consider S3/cloud storage for generated images in production
