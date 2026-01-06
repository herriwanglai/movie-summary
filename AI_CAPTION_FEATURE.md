# 🤖 AI-Powered Caption & Dialog Generation

## Overview

Add AI agents that can analyze screenshots and clips to generate and embed:
- **Captions** - Descriptive text about what's happening
- **Dialogs** - Actual dialogue from the scene
- **Quotes** - Memorable/impactful lines
- **Custom Prompts** - User-defined text generation

All text is embedded directly into the image/video with customizable styling.

---

## 🎨 UI/UX Design

### Collection Manager with AI Caption Button

```
┌────────────────────────────────────────┐
│ Screenshot                             │
│ ┌────────────────────────────────────┐ │
│ │                                    │ │
│ │        [Screenshot Image]          │ │
│ │                                    │ │
│ └────────────────────────────────────┘ │
│                                        │
│ Scene 12 • 00:12:34                    │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ 🤖 AI Caption                    ▼ │ │ ← New Button
│ └────────────────────────────────────┘ │
│                                        │
│ [🎬 Jump] [▶️ Play] [✏️ Edit]          │
└────────────────────────────────────────┘
```

### AI Caption Dialog

```
┌─────────────────────────────────────────────────┐
│ 🤖 Generate AI Caption                          │
├─────────────────────────────────────────────────┤
│                                                 │
│ Caption Type:                                   │
│ ○ Caption (Describe what's happening)          │
│ ○ Dialog (What characters are saying)          │
│ ○ Quote (Memorable line from scene)            │
│ ● Custom Prompt                                 │
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ Prompt:                                     │ │
│ │ ┌─────────────────────────────────────────┐ │ │
│ │ │ Describe the emotion and mood in this   │ │ │
│ │ │ scene with dramatic language            │ │ │
│ │ └─────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ Style Settings:                                 │
│ ┌───────────┬────────────┬──────────────┐      │
│ │ Font      │ Size       │ Position     │      │
│ │ [Arial ▼] │ [24px  ▼]  │ [Bottom  ▼]  │      │
│ └───────────┴────────────┴──────────────┘      │
│                                                 │
│ ┌───────────┬────────────┐                     │
│ │ Color     │ Background │                     │
│ │ [White ▼] │ [Black 80%]│                     │
│ └───────────┴────────────┘                     │
│                                                 │
│ Preview:                                        │
│ ┌─────────────────────────────────────────────┐ │
│ │ [Screenshot with overlay preview]           │ │
│ │                                             │ │
│ │ ╔═════════════════════════════════════════╗ │ │
│ │ ║ John confronts his nemesis in the       ║ │ │
│ │ ║ rain-soaked streets                     ║ │ │
│ │ ╚═════════════════════════════════════════╝ │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│        [Generate] [Apply & Save] [Cancel]      │
└─────────────────────────────────────────────────┘
```

---

## 🧠 AI Caption Generation Logic

### 1. Caption Types & Prompts

```typescript
interface CaptionType {
  type: 'caption' | 'dialog' | 'quote' | 'custom';
  systemPrompt: string;
  userPrompt?: string;
}

const CAPTION_PROMPTS = {
  caption: {
    system: `You are a film critic describing a scene.
             Analyze the image and provide a concise, vivid description
             of what's happening in 1-2 sentences.`,
    userPrompt: `Describe what's happening in this scene`
  },

  dialog: {
    system: `You are transcribing dialogue from a movie scene.
             Based on the image and the transcript timestamp,
             provide the exact dialogue being spoken.`,
    userPrompt: `What dialogue is being spoken at this moment?`
  },

  quote: {
    system: `You are identifying memorable movie quotes.
             Find the most impactful or memorable line from this scene.`,
    userPrompt: `What is the most memorable quote from this scene?`
  },

  emotion: {
    system: `You are analyzing emotional content in film.
             Describe the dominant emotion and mood in this scene.`,
    userPrompt: `Describe the emotion and mood`
  },

  dramatic: {
    system: `You are writing dramatic movie descriptions.
             Create a dramatic, cinematic description of this scene.`,
    userPrompt: `Write a dramatic description of this scene`
  }
};
```

### 2. AI Analysis Workflow

```typescript
async function generateCaption(
  screenshot: Screenshot,
  captionType: CaptionType,
  customPrompt?: string
): Promise<GeneratedCaption> {

  // Step 1: Get context from analysis
  const context = await getSceneContext(screenshot);

  // Step 2: Prepare prompt for Ollama
  const prompt = buildPrompt(captionType, context, customPrompt);

  // Step 3: Generate caption with Ollama
  const caption = await ollamaClient.generateWithVision({
    image: screenshot.imageUrl,
    prompt: prompt,
    context: {
      sceneNumber: screenshot.sceneNumber,
      timestamp: screenshot.timestamp,
      transcript: context.transcript,
      characters: context.characters,
      importance: screenshot.importanceScore
    }
  });

  // Step 4: Format and validate
  const formatted = formatCaption(caption, captionType);

  return {
    id: generateId(),
    screenshotId: screenshot.id,
    type: captionType.type,
    text: formatted,
    generatedAt: Date.now(),
    prompt: customPrompt || captionType.userPrompt
  };
}
```

### 3. Context Retrieval

```typescript
async function getSceneContext(screenshot: Screenshot) {
  // Get scene information
  const scene = await getScene(screenshot.sceneNumber);

  // Get transcript around this timestamp
  const transcript = await getTranscript(
    screenshot.timestamp - 5,  // 5 seconds before
    screenshot.timestamp + 5   // 5 seconds after
  );

  // Get character analysis
  const characters = await getCharactersInScene(scene.sceneNumber);

  // Get importance analysis
  const importance = await getImportanceAnalysis(scene.sceneNumber);

  return {
    scene,
    transcript,
    characters,
    importance,
    // Additional context
    previousScenes: await getPreviousScenes(scene.sceneNumber, 2),
    themes: await getSceneThemes(scene.sceneNumber)
  };
}
```

---

## 🎨 Text Embedding System

### 1. Caption Overlay Component

```typescript
interface CaptionStyle {
  font: string;
  fontSize: number;
  color: string;
  backgroundColor: string;
  backgroundOpacity: number;
  position: 'top' | 'center' | 'bottom' | 'custom';
  customPosition?: { x: number; y: number };
  alignment: 'left' | 'center' | 'right';
  padding: number;
  borderRadius: number;
  shadow: boolean;
}

interface EmbeddedCaption {
  text: string;
  style: CaptionStyle;
  position: {
    x: number;  // percentage
    y: number;  // percentage
  };
}

// Generate image with embedded caption
async function embedCaptionInImage(
  screenshot: Screenshot,
  caption: GeneratedCaption,
  style: CaptionStyle
): Promise<string> {

  // Load image
  const image = await loadImage(screenshot.imageUrl);

  // Create canvas
  const canvas = createCanvas(image.width, image.height);
  const ctx = canvas.getContext('2d');

  // Draw original image
  ctx.drawImage(image, 0, 0);

  // Calculate text position
  const position = calculatePosition(style.position, image.width, image.height);

  // Draw background box
  if (style.backgroundColor) {
    ctx.fillStyle = `rgba(${hexToRgb(style.backgroundColor)}, ${style.backgroundOpacity})`;
    const textMetrics = measureText(caption.text, style);
    ctx.fillRect(
      position.x - style.padding,
      position.y - style.padding,
      textMetrics.width + style.padding * 2,
      textMetrics.height + style.padding * 2
    );
  }

  // Draw shadow
  if (style.shadow) {
    ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
    ctx.shadowBlur = 4;
    ctx.shadowOffsetX = 2;
    ctx.shadowOffsetY = 2;
  }

  // Draw text
  ctx.font = `${style.fontSize}px ${style.font}`;
  ctx.fillStyle = style.color;
  ctx.textAlign = style.alignment;

  // Word wrap if needed
  const lines = wrapText(caption.text, image.width * 0.9, ctx);
  lines.forEach((line, i) => {
    ctx.fillText(
      line,
      position.x,
      position.y + i * (style.fontSize * 1.2)
    );
  });

  // Save as new image
  const buffer = canvas.toBuffer('image/jpeg', { quality: 0.95 });
  const newUrl = await saveImage(buffer, `${screenshot.id}_captioned.jpg`);

  return newUrl;
}
```

### 2. Caption Presets

```typescript
const CAPTION_PRESETS = {
  subtitle: {
    font: 'Arial',
    fontSize: 24,
    color: '#FFFFFF',
    backgroundColor: '#000000',
    backgroundOpacity: 0.8,
    position: 'bottom',
    alignment: 'center',
    padding: 10,
    borderRadius: 4,
    shadow: true
  },

  filmQuote: {
    font: 'Georgia',
    fontSize: 32,
    color: '#FFFFFF',
    backgroundColor: '#000000',
    backgroundOpacity: 0.6,
    position: 'center',
    alignment: 'center',
    padding: 20,
    borderRadius: 8,
    shadow: true
  },

  minimal: {
    font: 'Helvetica',
    fontSize: 18,
    color: '#FFFFFF',
    backgroundColor: 'transparent',
    backgroundOpacity: 0,
    position: 'bottom',
    alignment: 'left',
    padding: 15,
    borderRadius: 0,
    shadow: true
  },

  dramatic: {
    font: 'Cinzel',
    fontSize: 36,
    color: '#FFD700',
    backgroundColor: '#1a1a1a',
    backgroundOpacity: 0.9,
    position: 'center',
    alignment: 'center',
    padding: 25,
    borderRadius: 12,
    shadow: true
  }
};
```

---

## 🔧 Implementation Components

### 1. Caption Generator Service

```typescript
// services/captionService.ts
class CaptionGeneratorService {
  private ollamaClient: OllamaClient;
  private analysisCache: Map<string, SceneContext>;

  async generateCaption(
    screenshot: Screenshot,
    options: CaptionOptions
  ): Promise<GeneratedCaption> {

    // Get context
    const context = await this.getContext(screenshot);

    // Prepare prompt based on type
    const prompt = this.buildPrompt(options.type, options.customPrompt, context);

    // Generate with vision model
    const response = await this.ollamaClient.generateWithVision({
      model: 'llava',  // or 'bakllava' for vision
      image: screenshot.imageUrl,
      prompt: prompt,
      context: {
        transcript: context.transcript,
        sceneDescription: context.scene.description,
        importance: screenshot.importanceScore
      }
    });

    return {
      id: generateId(),
      screenshotId: screenshot.id,
      type: options.type,
      text: response.text.trim(),
      prompt: options.customPrompt || prompt,
      generatedAt: Date.now(),
      metadata: {
        model: 'llava',
        confidence: response.confidence,
        context: context
      }
    };
  }

  private buildPrompt(
    type: CaptionType,
    customPrompt?: string,
    context?: SceneContext
  ): string {
    if (customPrompt) {
      return customPrompt;
    }

    const basePrompt = CAPTION_PROMPTS[type];

    let prompt = basePrompt.userPrompt;

    // Add context
    if (context?.transcript) {
      prompt += `\n\nDialogue from scene: "${context.transcript}"`;
    }

    if (context?.characters) {
      prompt += `\n\nCharacters present: ${context.characters.join(', ')}`;
    }

    if (context?.importance > 0.7) {
      prompt += `\n\nNote: This is a high-importance scene.`;
    }

    return prompt;
  }

  async embedCaption(
    screenshot: Screenshot,
    caption: GeneratedCaption,
    style: CaptionStyle
  ): Promise<string> {
    // Call image processing service
    return await embedCaptionInImage(screenshot, caption, style);
  }
}
```

### 2. Caption UI Component

```tsx
// components/CaptionGenerator/CaptionGenerator.tsx
interface CaptionGeneratorProps {
  screenshot: Screenshot;
  onCaptionGenerated: (caption: GeneratedCaption) => void;
  onClose: () => void;
}

export const CaptionGenerator: React.FC<CaptionGeneratorProps> = ({
  screenshot,
  onCaptionGenerated,
  onClose
}) => {
  const [captionType, setCaptionType] = useState<CaptionType>('caption');
  const [customPrompt, setCustomPrompt] = useState('');
  const [style, setStyle] = useState<CaptionStyle>(CAPTION_PRESETS.subtitle);
  const [preview, setPreview] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);

    try {
      // Generate caption text
      const caption = await captionService.generateCaption(screenshot, {
        type: captionType,
        customPrompt: customPrompt || undefined
      });

      // Generate preview with caption embedded
      const previewUrl = await captionService.embedCaption(
        screenshot,
        caption,
        style
      );

      setPreview(previewUrl);

    } catch (error) {
      toast.error('Failed to generate caption');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleApply = async () => {
    if (!preview) return;

    // Save captioned version
    await screenshotService.updateScreenshot(screenshot.id, {
      captionedUrl: preview,
      caption: caption,
      captionStyle: style
    });

    onCaptionGenerated(caption);
    toast.success('Caption added to screenshot!');
  };

  return (
    <Dialog open onClose={onClose}>
      <DialogTitle>🤖 Generate AI Caption</DialogTitle>

      <DialogContent>
        {/* Caption Type Selection */}
        <FormControl>
          <FormLabel>Caption Type</FormLabel>
          <RadioGroup value={captionType} onChange={setCaptionType}>
            <Radio value="caption">
              Caption - Describe what's happening
            </Radio>
            <Radio value="dialog">
              Dialog - What characters are saying
            </Radio>
            <Radio value="quote">
              Quote - Memorable line from scene
            </Radio>
            <Radio value="custom">
              Custom Prompt
            </Radio>
          </RadioGroup>
        </FormControl>

        {/* Custom Prompt */}
        {captionType === 'custom' && (
          <TextField
            label="Custom Prompt"
            multiline
            rows={3}
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder="e.g., Describe the tension and atmosphere in this scene"
            fullWidth
          />
        )}

        {/* Style Settings */}
        <Box className="style-settings">
          <Typography variant="h6">Style Settings</Typography>

          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Select
                label="Preset"
                value={selectedPreset}
                onChange={(preset) => setStyle(CAPTION_PRESETS[preset])}
              >
                <MenuItem value="subtitle">Subtitle</MenuItem>
                <MenuItem value="filmQuote">Film Quote</MenuItem>
                <MenuItem value="minimal">Minimal</MenuItem>
                <MenuItem value="dramatic">Dramatic</MenuItem>
              </Select>
            </Grid>

            <Grid item xs={4}>
              <Select label="Font" value={style.font} onChange={...}>
                <MenuItem value="Arial">Arial</MenuItem>
                <MenuItem value="Georgia">Georgia</MenuItem>
                <MenuItem value="Helvetica">Helvetica</MenuItem>
                <MenuItem value="Cinzel">Cinzel</MenuItem>
              </Select>
            </Grid>

            <Grid item xs={4}>
              <TextField
                label="Size"
                type="number"
                value={style.fontSize}
                onChange={(e) => updateStyle('fontSize', e.target.value)}
              />
            </Grid>

            <Grid item xs={6}>
              <ColorPicker
                label="Text Color"
                value={style.color}
                onChange={(color) => updateStyle('color', color)}
              />
            </Grid>

            <Grid item xs={6}>
              <Select
                label="Position"
                value={style.position}
                onChange={(pos) => updateStyle('position', pos)}
              >
                <MenuItem value="top">Top</MenuItem>
                <MenuItem value="center">Center</MenuItem>
                <MenuItem value="bottom">Bottom</MenuItem>
              </Select>
            </Grid>
          </Grid>
        </Box>

        {/* Preview */}
        <Box className="preview-section">
          <Typography variant="h6">Preview</Typography>
          {preview ? (
            <img src={preview} alt="Preview" className="preview-image" />
          ) : (
            <Box className="preview-placeholder">
              <Typography color="textSecondary">
                Click "Generate" to see preview
              </Typography>
            </Box>
          )}
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleGenerate}
          disabled={isGenerating}
          variant="outlined"
        >
          {isGenerating ? '🤖 Generating...' : '🤖 Generate'}
        </Button>
        <Button
          onClick={handleApply}
          disabled={!preview}
          variant="contained"
          color="primary"
        >
          Apply & Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};
```

### 3. Collection Manager Integration

```tsx
// components/CollectionManager/ScreenshotCard.tsx
<ScreenshotCard screenshot={screenshot}>
  <img src={screenshot.captionedUrl || screenshot.imageUrl} />

  {/* Show if caption exists */}
  {screenshot.caption && (
    <div className="caption-badge">
      <span>🤖 AI Caption</span>
    </div>
  )}

  <div className="action-buttons">
    <JumpButton timestamp={screenshot.timestamp} />

    {/* AI Caption Button */}
    <button
      className="ai-caption-btn"
      onClick={() => openCaptionGenerator(screenshot)}
    >
      <span className="icon">🤖</span>
      <span className="label">
        {screenshot.caption ? 'Edit Caption' : 'Add Caption'}
      </span>
    </button>

    <button onClick={() => openPreview(screenshot)}>
      👁️ Preview
    </button>
  </div>
</ScreenshotCard>
```

---

## 🎬 Video Clip Caption Support

### Embedded Subtitle Track

```typescript
// For clips, generate SRT subtitle file
async function generateClipSubtitles(
  clip: Clip,
  captionType: CaptionType
): Promise<string> {

  // Analyze clip in segments
  const segments = await analyzeClipSegments(clip);

  // Generate caption for each segment
  const subtitles = await Promise.all(
    segments.map(segment =>
      captionService.generateCaption(segment, {
        type: captionType
      })
    )
  );

  // Create SRT file
  const srtContent = generateSRT(subtitles, segments);

  // Save SRT file
  const srtPath = await saveSRT(clip.id, srtContent);

  // Optionally burn subtitles into video
  if (options.burnIn) {
    const captionedVideoPath = await burnSubtitles(
      clip.videoUrl,
      srtPath,
      style
    );
    return captionedVideoPath;
  }

  return srtPath;
}
```

---

## 📊 Database Schema Updates

```sql
-- Add caption fields to screenshots table
ALTER TABLE screenshots ADD COLUMN caption_text TEXT;
ALTER TABLE screenshots ADD COLUMN caption_type VARCHAR(50);
ALTER TABLE screenshots ADD COLUMN caption_style JSON;
ALTER TABLE screenshots ADD COLUMN captioned_image_url VARCHAR(512);
ALTER TABLE screenshots ADD COLUMN caption_prompt TEXT;
ALTER TABLE screenshots ADD COLUMN caption_generated_at TIMESTAMP;

-- Add caption fields to clips table
ALTER TABLE clips ADD COLUMN subtitle_url VARCHAR(512);  -- SRT file
ALTER TABLE clips ADD COLUMN captioned_video_url VARCHAR(512);  -- Burned-in
ALTER TABLE clips ADD COLUMN caption_segments JSON;
```

---

## 🚀 API Endpoints

```python
# Generate caption for screenshot
POST /api/captions/screenshot/{screenshot_id}
Body: {
  "type": "caption" | "dialog" | "quote" | "custom",
  "customPrompt": "optional custom prompt",
  "style": CaptionStyle
}
Response: {
  "caption": GeneratedCaption,
  "previewUrl": string
}

# Apply caption to screenshot
POST /api/screenshots/{screenshot_id}/apply-caption
Body: {
  "caption": GeneratedCaption,
  "style": CaptionStyle
}
Response: {
  "captionedUrl": string
}

# Generate subtitles for clip
POST /api/captions/clip/{clip_id}
Body: {
  "type": "caption" | "dialog",
  "burnIn": boolean,
  "style": CaptionStyle
}
Response: {
  "subtitleUrl": string,
  "captionedVideoUrl": string (if burnIn=true)
}
```

---

## ✨ Example Use Cases

### Use Case 1: Create Shareable Movie Quotes

```
1. User finds dramatic moment
2. Captures screenshot
3. Clicks "🤖 Add Caption"
4. Selects "Quote" type
5. AI generates: "I am inevitable."
6. User selects "Film Quote" preset (dramatic styling)
7. Caption embedded with gold text on dark background
8. Share on social media
```

### Use Case 2: Educational Analysis

```
1. Film student analyzing cinematography
2. Captures screenshot of interesting shot
3. Clicks "🤖 Add Caption"
4. Custom prompt: "Explain the framing and composition"
5. AI generates technical analysis
6. Embedded as educational annotation
7. Export for presentation
```

### Use Case 3: Dialogue Documentation

```
1. User studying foreign film
2. Captures key dialogue moments
3. Clicks "🤖 Add Caption"
4. Selects "Dialog" type
5. AI extracts exact dialogue with translation
6. Embedded as subtitle
7. Build collection of key dialogues
```

---

## 🎨 UI Flow Diagram

```
Screenshot in Collection
         │
         ├─→ Click "🤖 Add Caption"
         │
         ▼
   Caption Generator Dialog
         │
         ├─→ Select Type (Caption/Dialog/Quote/Custom)
         ├─→ Enter Custom Prompt (optional)
         ├─→ Choose Style Preset
         ├─→ Adjust Style Settings
         │
         ▼
   Click "Generate"
         │
         ├─→ Backend: Fetch scene context
         ├─→ Backend: Call Ollama with vision
         ├─→ Backend: Generate caption text
         ├─→ Backend: Embed in image
         │
         ▼
   Preview Shown
         │
         ├─→ User reviews
         ├─→ User adjusts style if needed
         ├─→ Click "Apply & Save"
         │
         ▼
   Captioned Screenshot Saved
         │
         ├─→ Collection Manager: Shows captioned version
         ├─→ Node Editor: Available with caption
         ├─→ Export: Can export with captions
```

---

## ✅ Summary

### New Features Added:

1. **🤖 AI Caption Button** in Collection Manager
2. **Caption Types**: Description, Dialog, Quote, Custom
3. **Text Embedding**: Overlay captions on images/videos
4. **Style Presets**: Subtitle, Film Quote, Minimal, Dramatic
5. **Custom Prompts**: User can specify exactly what they want
6. **Live Preview**: See caption before applying
7. **Context-Aware**: Uses transcript, characters, importance
8. **Video Support**: Generate SRT subtitles for clips

### Technical Stack:

- **AI**: Ollama + LLaVA (vision model) for caption generation
- **Image Processing**: Canvas API for text embedding
- **Video**: FFmpeg for subtitle burning
- **UI**: React dialog with style customization

**Ready to add this feature to the implementation plan!** 🚀
