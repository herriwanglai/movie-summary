# 📖 Ink Visual Novel Export Feature

## Overview

Export movie analysis as an interactive visual novel in Ink format (inkle/inkjs), including:
- Character dialogues with poses and expressions
- Scene settings and backgrounds
- Scene headings and transitions
- Character actions and movements
- Intercuts and subheaders
- Important visual shots

---

## 🎭 Ink Format Structure

### What is Ink?

Ink is a scripting language for interactive narratives used in games like *80 Days* and *Heaven's Vault*. It supports:
- Branching narratives
- Character dialogue
- Scene descriptions
- Variables and logic
- Tags for visual elements

### Basic Ink Syntax

```ink
=== scene_name ===
# SCENE: Location Name
# BACKGROUND: background_image.jpg
# MUSIC: ambient_track.mp3

Character expressions and dialogue...

-> next_scene

=== next_scene ===
...
```

---

## 🎬 Movie to Ink Conversion Pipeline

```
Movie Analysis Data
        │
        ├─→ Character Dialogue Extraction
        │   ├─→ Speaker identification
        │   ├─→ Pose detection (stand, sit, walk)
        │   └─→ Expression analysis (neutral, happy, sad, angry)
        │
        ├─→ Scene Setting Extraction
        │   ├─→ Location identification
        │   ├─→ Background description
        │   ├─→ Time of day
        │   └─→ Setting atmosphere
        │
        ├─→ Scene Structure
        │   ├─→ Scene headings (INT./EXT.)
        │   ├─→ Scene transitions (CUT TO, FADE TO)
        │   ├─→ Intercuts
        │   └─→ Subheaders
        │
        └─→ Ink Format Export
            ├─→ Generate .ink file
            ├─→ Create knot structure
            ├─→ Add character tags
            └─→ Include visual descriptions
```

---

## 🎨 Character Pose & Expression Detection

### Pose Detection (Basic)

Using visual analysis and context:

```typescript
interface CharacterPose {
  type: 'stand' | 'sit' | 'walk' | 'run' | 'lean' | 'crouch' | 'lie';
  facing: 'left' | 'right' | 'center' | 'away';
  position: 'foreground' | 'midground' | 'background';
}

async function detectCharacterPose(
  screenshot: Screenshot,
  character: string,
  context: SceneContext
): Promise<CharacterPose> {

  // Use Ollama vision model
  const prompt = `Analyze this image and determine the character's pose.
                  Character: ${character}

                  Respond with:
                  - pose: stand, sit, walk, run, lean, crouch, or lie
                  - facing: left, right, center, or away
                  - position: foreground, midground, or background`;

  const analysis = await ollamaClient.analyzeImage(screenshot.imageUrl, prompt);

  return parsePoseFromAnalysis(analysis);
}
```

### Expression Detection (Basic)

```typescript
interface CharacterExpression {
  type: 'neutral' | 'happy' | 'sad' | 'angry' | 'surprised' | 'fearful' | 'disgusted';
  intensity: 'subtle' | 'moderate' | 'intense';
}

async function detectCharacterExpression(
  screenshot: Screenshot,
  character: string,
  dialogue: string
): Promise<CharacterExpression> {

  // Analyze from dialogue tone
  const dialogueEmotion = analyzeDialogueEmotion(dialogue);

  // Analyze from image (if available)
  const visualEmotion = await analyzeVisualEmotion(screenshot, character);

  // Combine both
  return combineEmotions(dialogueEmotion, visualEmotion);
}

function analyzeDialogueEmotion(dialogue: string): CharacterExpression {
  const text = dialogue.toLowerCase();

  // Keywords for emotions
  if (text.includes('!') || text.includes('damn') || text.includes('hell')) {
    return { type: 'angry', intensity: 'intense' };
  }
  if (text.includes('?') && text.includes('what')) {
    return { type: 'surprised', intensity: 'moderate' };
  }
  if (text.includes('ha') || text.includes('laugh')) {
    return { type: 'happy', intensity: 'moderate' };
  }

  // Default
  return { type: 'neutral', intensity: 'subtle' };
}
```

---

## 🏞️ Scene Setting Extraction

### Location Detection

```typescript
interface SceneSetting {
  heading: string;          // "INT. COFFEE SHOP - DAY"
  location: string;         // "Coffee Shop"
  setting: 'INT' | 'EXT';   // Interior or Exterior
  timeOfDay: 'DAY' | 'NIGHT' | 'MORNING' | 'EVENING';
  background: string;       // Description for visual novel
  atmosphere: string;       // Mood description
  lighting: string;         // Lighting description
}

async function extractSceneSetting(
  scene: Scene,
  keyframe: Keyframe,
  transcript: string
): Promise<SceneSetting> {

  const prompt = `Analyze this scene and describe the setting.

                  Provide:
                  1. Location name (e.g., "Coffee Shop", "City Street")
                  2. Interior or Exterior (INT/EXT)
                  3. Time of day (DAY/NIGHT/MORNING/EVENING)
                  4. Background description (for visual novel)
                  5. Atmosphere/mood
                  6. Lighting description

                  Dialogue context: ${transcript.substring(0, 200)}`;

  const analysis = await ollamaClient.analyzeWithVision({
    image: keyframe.frame.imageUrl,
    prompt: prompt
  });

  return parseSettingFromAnalysis(analysis);
}
```

---

## 📝 Ink Format Generator

### Main Exporter Class

```typescript
// services/inkExporter.ts
class InkExporter {
  private scenes: Scene[];
  private transcript: Transcript;
  private characters: Character[];
  private keyframes: Keyframe[];
  private analysis: MovieAnalysis;

  constructor(movieData: MovieData) {
    this.scenes = movieData.scenes;
    this.transcript = movieData.transcript;
    this.characters = movieData.characters;
    this.keyframes = movieData.keyframes;
    this.analysis = movieData.analysis;
  }

  async generateInkScript(): Promise<string> {
    let inkScript = '';

    // Header
    inkScript += this.generateHeader();
    inkScript += '\n\n';

    // Global variables
    inkScript += this.generateGlobalVariables();
    inkScript += '\n\n';

    // Character definitions
    inkScript += this.generateCharacterDefinitions();
    inkScript += '\n\n';

    // Main story flow
    inkScript += '=== start ===\n';
    inkScript += await this.generateMainStory();

    // End
    inkScript += '\n\n-> END\n';

    return inkScript;
  }

  private generateHeader(): string {
    return `// Generated from movie analysis
// Title: ${this.analysis.title || 'Untitled'}
// Duration: ${formatDuration(this.analysis.duration)}
// Scenes: ${this.scenes.length}
// Generated: ${new Date().toISOString()}

// This is an Ink script for visual novel presentation
// Compatible with inkle/inkjs
`;
  }

  private generateGlobalVariables(): string {
    return `// Global Variables
VAR current_scene = 0
VAR total_scenes = ${this.scenes.length}
`;
  }

  private generateCharacterDefinitions(): string {
    let def = '// Character Definitions\n';

    this.characters.forEach(char => {
      def += `// ${char.name}\n`;
      def += `//   Role: ${char.role || 'Unknown'}\n`;
      def += `//   Appearances: ${char.sceneCount || 0} scenes\n`;
      def += '\n';
    });

    return def;
  }

  private async generateMainStory(): string {
    let story = '';

    for (let i = 0; i < this.scenes.length; i++) {
      const scene = this.scenes[i];
      story += await this.generateSceneKnot(scene, i);
      story += '\n\n';
    }

    return story;
  }

  private async generateSceneKnot(scene: Scene, index: number): Promise<string> {
    const knotName = `scene_${index + 1}`;
    let knot = `=== ${knotName} ===\n`;

    // Scene setting
    const setting = await this.extractSceneSetting(scene);
    knot += this.formatSceneHeading(setting);
    knot += '\n';

    // Get keyframe for this scene
    const keyframe = this.getSceneKeyframe(scene);
    if (keyframe) {
      knot += `# IMAGE: ${keyframe.frame.imageUrl}\n`;
    }

    // Scene description
    const description = await this.generateSceneDescription(scene);
    knot += `${description}\n\n`;

    // Dialogue
    const dialogues = this.getSceneDialogues(scene);
    for (const dialogue of dialogues) {
      knot += await this.formatDialogue(dialogue, scene);
      knot += '\n';
    }

    // Transition to next scene
    if (index < this.scenes.length - 1) {
      const transition = this.determineTransition(scene, this.scenes[index + 1]);
      knot += `\n${transition}\n`;
      knot += `-> scene_${index + 2}\n`;
    } else {
      knot += '\n-> finale\n';
    }

    return knot;
  }

  private formatSceneHeading(setting: SceneSetting): string {
    return `# SCENE: ${setting.heading}
# LOCATION: ${setting.location}
# TIME: ${setting.timeOfDay}
# BACKGROUND: ${setting.background}
# ATMOSPHERE: ${setting.atmosphere}`;
  }

  private async formatDialogue(
    dialogue: TranscriptSegment,
    scene: Scene
  ): Promise<string> {
    // Detect speaker
    const speaker = this.detectSpeaker(dialogue);

    // Get screenshot near this timestamp
    const screenshot = this.getScreenshotNearTime(dialogue.start);

    // Detect pose and expression
    let pose: CharacterPose | null = null;
    let expression: CharacterExpression | null = null;

    if (screenshot && speaker) {
      pose = await this.detectCharacterPose(screenshot, speaker, scene);
      expression = await this.detectCharacterExpression(screenshot, speaker, dialogue.text);
    }

    // Format in Ink with tags
    let inkDialogue = '';

    // Character action/pose tag
    if (pose) {
      inkDialogue += `# CHARACTER: ${speaker}\n`;
      inkDialogue += `# POSE: ${pose.type}\n`;
      inkDialogue += `# FACING: ${pose.facing}\n`;
      inkDialogue += `# POSITION: ${pose.position}\n`;
    }

    // Expression tag
    if (expression) {
      inkDialogue += `# EXPRESSION: ${expression.type}\n`;
      inkDialogue += `# INTENSITY: ${expression.intensity}\n`;
    }

    // Dialogue text
    if (speaker) {
      inkDialogue += `${speaker}: ${dialogue.text}\n`;
    } else {
      inkDialogue += `NARRATOR: ${dialogue.text}\n`;
    }

    return inkDialogue;
  }

  private determineTransition(currentScene: Scene, nextScene: Scene): string {
    const timeDiff = nextScene.start_time - currentScene.end_time;

    if (timeDiff < 1) {
      return '// CUT TO:';
    } else if (timeDiff < 3) {
      return '// FADE TO:';
    } else {
      return '// DISSOLVE TO:';
    }
  }
}
```

---

## 📋 Ink Format Examples

### Example 1: Simple Scene with Dialogue

```ink
=== scene_1 ===
# SCENE: INT. COFFEE SHOP - DAY
# LOCATION: Coffee Shop
# TIME: DAY
# BACKGROUND: A cozy coffee shop with warm lighting
# ATMOSPHERE: Casual, friendly

The morning sun streams through the large windows of the coffee shop.

# CHARACTER: John
# POSE: sit
# FACING: right
# POSITION: foreground
# EXPRESSION: neutral
# INTENSITY: subtle
John: I've been waiting for you.

# CHARACTER: Sarah
# POSE: stand
# FACING: left
# POSITION: foreground
# EXPRESSION: surprised
# INTENSITY: moderate
Sarah: What? How did you find me here?

# CHARACTER: John
# POSE: sit
# FACING: right
# POSITION: foreground
# EXPRESSION: serious
# INTENSITY: moderate
John: We need to talk about what happened.

// CUT TO:
-> scene_2
```

### Example 2: Action Scene

```ink
=== scene_15 ===
# SCENE: EXT. CITY STREET - NIGHT
# LOCATION: Downtown Street
# TIME: NIGHT
# BACKGROUND: Rain-soaked city street with neon lights
# ATMOSPHERE: Tense, dangerous
# IMAGE: keyframe_015_action.jpg

The rain pours down as lightning illuminates the dark street.

# CHARACTER: John
# POSE: run
# FACING: right
# POSITION: midground
# EXPRESSION: fearful
# INTENSITY: intense
John: Get down!

// INTERCUT - GUNFIRE

# CHARACTER: Sarah
# POSE: crouch
# FACING: left
# POSITION: foreground
# EXPRESSION: fearful
# INTENSITY: intense
Sarah: We have to get out of here!

// IMPORTANT SHOT: Explosion in background

The building behind them erupts in flames.

// FADE TO BLACK:
-> scene_16
```

### Example 3: Emotional Scene

```ink
=== scene_23 ===
# SCENE: INT. HOSPITAL ROOM - NIGHT
# LOCATION: Hospital Room
# TIME: NIGHT
# BACKGROUND: Sterile hospital room with dim lighting
# ATMOSPHERE: Somber, emotional
# IMAGE: keyframe_023_hospital.jpg

The heart monitor beeps steadily in the quiet room.

# CHARACTER: John
# POSE: sit
# FACING: center
# POSITION: foreground
# EXPRESSION: sad
# INTENSITY: intense
John: I should have been there...

# CHARACTER: Sarah
# POSE: lie
# FACING: center
# POSITION: midground
# EXPRESSION: sad
# INTENSITY: subtle
Sarah: It's not your fault.

// SUBHEADER: A moment of silence

John takes Sarah's hand.

# CHARACTER: John
# POSE: sit
# FACING: center
# POSITION: foreground
# EXPRESSION: sad
# INTENSITY: intense
John: I'm not leaving you.

// DISSOLVE TO:
-> scene_24
```

---

## 🎯 Complete Export Workflow

### User Flow

```
User completes movie analysis
        │
        ▼
Clicks "Export to Ink"
        │
        ▼
┌─────────────────────────────────┐
│ Export to Visual Novel (Ink)    │
├─────────────────────────────────┤
│                                 │
│ Options:                        │
│ ☑️ Include character poses      │
│ ☑️ Include expressions          │
│ ☑️ Include scene descriptions   │
│ ☑️ Include visual shots         │
│ ☐ Generate character sprites    │
│                                 │
│ Detail Level:                   │
│ ○ Basic (dialogue only)         │
│ ● Standard (+ poses/expressions)│
│ ○ Detailed (+ all metadata)    │
│                                 │
│ Format:                         │
│ ● Ink Script (.ink)             │
│ ○ Ren'Py Script (.rpy)         │
│                                 │
│ [Cancel] [Export]               │
└─────────────────────────────────┘
        │
        ▼
Processing...
├─→ Analyzing character poses
├─→ Detecting expressions
├─→ Extracting scene settings
├─→ Formatting dialogue
└─→ Generating Ink script
        │
        ▼
Download: movie_script.ink
```

---

## 🔧 Implementation Components

### 1. Pose Detection Service

```typescript
// services/poseDetectionService.ts
class PoseDetectionService {
  private ollamaClient: OllamaClient;

  async detectPose(
    screenshot: Screenshot,
    character: string
  ): Promise<CharacterPose> {

    const prompt = `Look at this image and determine the pose of ${character}.

                    Choose the pose type:
                    - stand: standing upright
                    - sit: sitting down
                    - walk: walking motion
                    - run: running motion
                    - lean: leaning against something
                    - crouch: crouching or kneeling
                    - lie: lying down

                    Choose facing direction:
                    - left: facing left
                    - right: facing right
                    - center: facing camera
                    - away: facing away

                    Choose position:
                    - foreground: close to camera
                    - midground: middle distance
                    - background: far from camera

                    Respond in format: "pose: X, facing: Y, position: Z"`;

    const response = await this.ollamaClient.analyzeImage(
      screenshot.imageUrl,
      prompt
    );

    return this.parsePoseResponse(response);
  }

  private parsePoseResponse(response: string): CharacterPose {
    // Parse format: "pose: stand, facing: right, position: foreground"
    const poseMatch = response.match(/pose:\s*(\w+)/i);
    const facingMatch = response.match(/facing:\s*(\w+)/i);
    const positionMatch = response.match(/position:\s*(\w+)/i);

    return {
      type: (poseMatch?.[1] || 'stand') as any,
      facing: (facingMatch?.[1] || 'center') as any,
      position: (positionMatch?.[1] || 'foreground') as any
    };
  }
}
```

### 2. Scene Setting Extractor

```typescript
// services/sceneSettingExtractor.ts
class SceneSettingExtractor {
  async extractSetting(
    scene: Scene,
    keyframe: Keyframe,
    transcript: string
  ): Promise<SceneSetting> {

    const prompt = `Analyze this scene image and dialogue to determine the setting.

                    Dialogue: "${transcript.substring(0, 300)}"

                    Provide:
                    1. Location name (e.g., "Coffee Shop")
                    2. Is it Interior (INT) or Exterior (EXT)?
                    3. Time of day: DAY, NIGHT, MORNING, or EVENING?
                    4. Brief background description for visual novel (1 sentence)
                    5. Atmosphere/mood (1-2 words like "tense, romantic")
                    6. Lighting description (1-2 words like "dim, bright")

                    Format response as:
                    Location: X
                    Setting: INT/EXT
                    Time: X
                    Background: X
                    Atmosphere: X
                    Lighting: X`;

    const response = await this.ollamaClient.analyzeWithVision({
      image: keyframe.frame.imageUrl,
      prompt: prompt
    });

    return this.parseSettingResponse(response, scene);
  }

  private parseSettingResponse(response: string, scene: Scene): SceneSetting {
    // Parse the response
    const location = this.extractField(response, 'Location');
    const setting = this.extractField(response, 'Setting') as 'INT' | 'EXT';
    const timeOfDay = this.extractField(response, 'Time') as any;
    const background = this.extractField(response, 'Background');
    const atmosphere = this.extractField(response, 'Atmosphere');
    const lighting = this.extractField(response, 'Lighting');

    const heading = `${setting}. ${location.toUpperCase()} - ${timeOfDay}`;

    return {
      heading,
      location,
      setting,
      timeOfDay,
      background,
      atmosphere,
      lighting
    };
  }

  private extractField(text: string, field: string): string {
    const regex = new RegExp(`${field}:\\s*(.+?)(?:\\n|$)`, 'i');
    const match = text.match(regex);
    return match?.[1]?.trim() || 'Unknown';
  }
}
```

### 3. Ink Format Builder

```typescript
// services/inkFormatBuilder.ts
class InkFormatBuilder {
  private content: string[] = [];

  addHeader(title: string, metadata: any) {
    this.content.push(`// ${title}`);
    this.content.push(`// Generated: ${new Date().toISOString()}`);
    this.content.push('');
    return this;
  }

  addSceneHeading(heading: string, tags: Record<string, string>) {
    this.content.push(`=== ${this.sanitizeKnotName(heading)} ===`);

    Object.entries(tags).forEach(([key, value]) => {
      this.content.push(`# ${key.toUpperCase()}: ${value}`);
    });

    this.content.push('');
    return this;
  }

  addNarration(text: string) {
    this.content.push(text);
    this.content.push('');
    return this;
  }

  addDialogue(
    speaker: string,
    text: string,
    tags?: {
      pose?: string;
      expression?: string;
      facing?: string;
      position?: string;
    }
  ) {
    if (tags) {
      if (tags.pose) this.content.push(`# CHARACTER: ${speaker}`);
      if (tags.pose) this.content.push(`# POSE: ${tags.pose}`);
      if (tags.facing) this.content.push(`# FACING: ${tags.facing}`);
      if (tags.position) this.content.push(`# POSITION: ${tags.position}`);
      if (tags.expression) this.content.push(`# EXPRESSION: ${tags.expression}`);
    }

    this.content.push(`${speaker}: ${text}`);
    this.content.push('');
    return this;
  }

  addTransition(type: string) {
    this.content.push(`// ${type.toUpperCase()}:`);
    this.content.push('');
    return this;
  }

  addKnotLink(targetKnot: string) {
    this.content.push(`-> ${this.sanitizeKnotName(targetKnot)}`);
    this.content.push('');
    return this;
  }

  addIntercut(description: string) {
    this.content.push(`// INTERCUT - ${description.toUpperCase()}`);
    this.content.push('');
    return this;
  }

  addSubheader(text: string) {
    this.content.push(`// ${text.toUpperCase()}`);
    this.content.push('');
    return this;
  }

  addImportantShot(description: string) {
    this.content.push(`// IMPORTANT SHOT: ${description}`);
    this.content.push('');
    return this;
  }

  build(): string {
    return this.content.join('\n');
  }

  private sanitizeKnotName(name: string): string {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9_]/g, '_')
      .replace(/_{2,}/g, '_')
      .replace(/^_|_$/g, '');
  }
}
```

---

## 📊 Database Schema Updates

```sql
-- Add Ink export metadata
CREATE TABLE ink_exports (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos(id),
  ink_script TEXT,
  include_poses BOOLEAN DEFAULT TRUE,
  include_expressions BOOLEAN DEFAULT TRUE,
  include_settings BOOLEAN DEFAULT TRUE,
  detail_level VARCHAR(50),  -- 'basic', 'standard', 'detailed'
  generated_at TIMESTAMP,
  file_url VARCHAR(512)
);

-- Character pose cache
CREATE TABLE character_poses (
  id UUID PRIMARY KEY,
  screenshot_id UUID REFERENCES screenshots(id),
  character_name VARCHAR(255),
  pose_type VARCHAR(50),
  facing VARCHAR(50),
  position VARCHAR(50),
  confidence FLOAT,
  detected_at TIMESTAMP
);

-- Scene settings cache
CREATE TABLE scene_settings (
  id UUID PRIMARY KEY,
  scene_id UUID REFERENCES scenes(id),
  location VARCHAR(255),
  setting VARCHAR(10),  -- 'INT' or 'EXT'
  time_of_day VARCHAR(50),
  background_description TEXT,
  atmosphere VARCHAR(255),
  lighting VARCHAR(255),
  extracted_at TIMESTAMP
);
```

---

## 🚀 API Endpoints

```python
# Export to Ink format
POST /api/export/ink/{video_id}
Body: {
  "includePoses": true,
  "includeExpressions": true,
  "includeSettings": true,
  "detailLevel": "standard",
  "format": "ink"  # or "renpy"
}
Response: {
  "exportId": "uuid",
  "status": "processing"
}

# Get export status
GET /api/export/ink/{export_id}/status
Response: {
  "status": "complete",
  "progress": 100,
  "fileUrl": "/downloads/movie_script.ink"
}

# Download Ink script
GET /api/export/ink/{export_id}/download
Response: movie_script.ink file
```

---

## ✅ Summary

### Features Added:

1. **Character Analysis**
   - Pose detection (stand, sit, walk, run, lean, crouch, lie)
   - Expression detection (neutral, happy, sad, angry, surprised, fearful, disgusted)
   - Facing direction (left, right, center, away)
   - Position depth (foreground, midground, background)

2. **Scene Settings**
   - Location identification
   - INT/EXT classification
   - Time of day
   - Background descriptions
   - Atmosphere and mood
   - Lighting descriptions

3. **Ink Format Export**
   - Scene headings
   - Character dialogues with tags
   - Scene transitions (CUT TO, FADE TO, DISSOLVE TO)
   - Intercuts
   - Subheaders
   - Important visual shots
   - Narration

4. **Export Options**
   - Basic (dialogue only)
   - Standard (+ poses/expressions)
   - Detailed (+ all metadata)
   - Choice of formats (Ink, Ren'Py)

**Ready to implement visual novel export!** 📖✨
