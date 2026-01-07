# Character Creation UI - Detailed Design Plan

## Overview

A fullscreen workspace for creating and managing character profiles with an interactive node-based interface, AI chatbox, and image generation capabilities.

---

## Layout Structure

```
+--------------------------------------------------------------------------------+
|  FULLSCREEN CHARACTER CREATION WORKSPACE                                        |
+--------------------------------------------------------------------------------+
|  +------------+  +------------------------------------------------------------+ |
|  |            |  |                                                            | |
|  |  SIDEBAR   |  |                    MAIN AREA                               | |
|  |            |  |                                                            | |
|  | "Character"|  |  +--------+  +--------+  +--------+  +--------+           | |
|  |            |  |  | NODE 1 |  | NODE 2 |  | NODE 3 |  | NODE 4 |           | |
|  | [Avatar 1] |  |  | Face   |  | Body   |  | Outfit |  | Actor  |           | |
|  | Character1 |  |  +--------+  +--------+  +--------+  +--------+           | |
|  |            |  |                                                            | |
|  | [Avatar 2] |  |  +--------+  +--------+  +--------+                       | |
|  | Character2 |  |  | NODE 5 |  | NODE 6 |  | NODE 7 |                       | |
|  |            |  |  |Express |  | Pose   |  | Prompt |                       | |
|  | [Avatar 3] |  |  +--------+  +--------+  +--------+                       | |
|  | Character3 |  |                                                            | |
|  |            |  |  +--------------------------------------------------------+| |
|  |            |  |  |                    CHATBOX                             || |
|  | [+ Add]    |  |  | [AI conversation for refining character details]       || |
|  |            |  |  | [____________________________________] [Send]          || |
|  |            |  |  +--------------------------------------------------------+| |
|  |            |  |                                                            | |
|  |            |  |                              [Generate Character Images]   | |
|  +------------+  +------------------------------------------------------------+ |
+--------------------------------------------------------------------------------+
```

---

## Component Breakdown

### 1. Left Sidebar - Character List

```
+------------------+
|    Character     |  <- Title with icon
+------------------+
|                  |
|  +------------+  |
|  |  [AVATAR]  |  |  <- Face thumbnail (circular)
|  |  John Doe  |  |  <- Character name
|  |  ★ Main    |  |  <- Role badge (optional)
|  +------------+  |
|                  |
|  +------------+  |
|  |  [AVATAR]  |  |
|  |  Jane Smith|  |
|  |  Supporting|  |
|  +------------+  |
|                  |
|  +------------+  |
|  |  [AVATAR]  |  |
|  |  Villain X |  |
|  |  Antagonist|  |
|  +------------+  |
|                  |
|  ...             |
|                  |
|  +------------+  |
|  |    [+]     |  |  <- Add new character
|  |  Add New   |  |
|  +------------+  |
|                  |
+------------------+
```

#### Sidebar Specifications

| Property | Value |
|----------|-------|
| Width | 240px (fixed) |
| Background | `bg-gray-900/50` |
| Border | `border-r border-gray-800` |
| Title | "Character" with Users icon |
| Scroll | Vertical overflow auto |

#### Character List Item

```typescript
interface CharacterListItem {
  id: number;
  name: string;
  role: 'protagonist' | 'antagonist' | 'supporting' | 'background';
  avatarUrl: string;  // Face thumbnail
  isSelected: boolean;
  creationStatus: 'pending' | 'capturing' | 'ready' | 'generating';
}
```

#### List Item Styling

| State | Style |
|-------|-------|
| Default | `bg-transparent hover:bg-gray-800/50` |
| Selected | `bg-blue-500/20 border-l-2 border-blue-500` |
| Generating | `animate-pulse` with spinner overlay |

---

### 2. Main Area - Node Grid

The main area displays character data as interactive **nodes** (cards) arranged in a responsive grid.

#### Node Types

| Node | Content | Icon | Color Accent |
|------|---------|------|--------------|
| **Face** | Face screenshots gallery | `User` | Blue |
| **Body** | Full body screenshots | `Accessibility` | Purple |
| **Expression** | Expression variations | `SmilePlus` | Yellow |
| **Pose** | Pose screenshots | `PersonStanding` | Green |
| **Outfit** | Outfit gallery | `Shirt` | Pink |
| **Actor** | Actor metadata & photos | `Star` | Gold |
| **Prompt** | JSON prompt preview | `FileJson` | Cyan |

#### Node Layout

```
+------------------------------------------+
|  [Icon] Node Title              [Expand] |
+------------------------------------------+
|                                          |
|  +------+  +------+  +------+           |
|  | img1 |  | img2 |  | img3 |           |
|  +------+  +------+  +------+           |
|                                          |
|  [+ Add More]                            |
+------------------------------------------+
```

#### Node Grid Specifications

```css
/* Grid layout */
.node-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  padding: 24px;
}
```

#### Individual Node Card

```typescript
interface CharacterNode {
  type: 'face' | 'body' | 'expression' | 'pose' | 'outfit' | 'actor' | 'prompt';
  title: string;
  icon: LucideIcon;
  accentColor: string;
  images: string[];
  isExpanded: boolean;
  isEditable: boolean;
}
```

#### Node Card Styling

| Property | Value |
|----------|-------|
| Background | `bg-gray-900/30` |
| Border | `border border-gray-800` |
| Border Radius | `rounded-xl` |
| Hover | `hover:border-gray-700 hover:shadow-lg` |
| Header | Gradient based on accent color |
| Min Height | 200px |
| Max Height | 400px (expandable) |

---

### 3. Node Detailed Designs

#### 3.1 Face Node

```
+------------------------------------------+
|  [User] Face Close-ups          [⤢ Expand]|
|  ─────────────────────────────────────── |
|  +--------+  +--------+  +--------+      |
|  |        |  |        |  |        |      |
|  | [Face] |  | [Face] |  | [Face] |      |
|  |  img1  |  |  img2  |  |  img3  |      |
|  +--------+  +--------+  +--------+      |
|                                          |
|  Quality: ★★★★☆  |  3 of 5 captured     |
|                                          |
|  [+ Capture More]  [Auto-Select Best]    |
+------------------------------------------+
```

#### 3.2 Actor Node

```
+------------------------------------------+
|  [Star] Actor Reference         [⤢ Expand]|
|  ─────────────────────────────────────── |
|  +----------+  Name: Tom Holland         |
|  |          |  Age: 28                   |
|  | [Photo]  |  Height: 5'8" (173cm)      |
|  |          |  Weight: 150 lbs           |
|  +----------+                            |
|                                          |
|  +--------+  +--------+  +--------+      |
|  |  Ref1  |  |  Ref2  |  |  Ref3  |      |
|  +--------+  +--------+  +--------+      |
|                                          |
|  [🔍 Search Actor]  [Edit Metadata]      |
+------------------------------------------+
```

#### 3.3 Prompt Node

```
+------------------------------------------+
|  [FileJson] Character Prompt    [⤢ Expand]|
|  ─────────────────────────────────────── |
|  {                                       |
|    "character": {                        |
|      "name": "Peter Parker",             |
|      "role": "protagonist"               |
|    },                                    |
|    "physical_appearance": {              |
|      "face": { ... },                    |
|      ...                                 |
|    }                                     |
|  }                                       |
|                                          |
|  [📋 Copy]  [✏️ Edit]  [🔄 Regenerate]    |
+------------------------------------------+
```

---

### 4. Chatbox Component

An AI-powered chat interface for refining character details through conversation.

```
+------------------------------------------------------------------------+
|  💬 Character Assistant                                         [−] [×] |
+------------------------------------------------------------------------+
|                                                                         |
|  ┌─────────────────────────────────────────────────────────────────┐   |
|  │ 🤖 AI: I've analyzed the character "John Doe". He appears to    │   |
|  │ be a 35-year-old male with short brown hair and blue eyes.      │   |
|  │ Would you like me to add more detail to any specific aspect?    │   |
|  └─────────────────────────────────────────────────────────────────┘   |
|                                                                         |
|  ┌─────────────────────────────────────────────────────────────────┐   |
|  │ 👤 You: Can you describe his facial features in more detail?    │   |
|  └─────────────────────────────────────────────────────────────────┘   |
|                                                                         |
|  ┌─────────────────────────────────────────────────────────────────┐   |
|  │ 🤖 AI: Based on the screenshots, John has a square jawline,     │   |
|  │ prominent cheekbones, a slightly crooked nose (possibly from    │   |
|  │ an old injury), thin lips, and light stubble. His eyebrows      │   |
|  │ are thick and dark, giving him an intense look.                 │   |
|  │                                                                  │   |
|  │ [Apply to Prompt] [Edit] [Regenerate]                           │   |
|  └─────────────────────────────────────────────────────────────────┘   |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  | Ask about this character...                              [Send ➤] | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  Quick actions: [Describe face] [Describe outfit] [Find actor]         |
+------------------------------------------------------------------------+
```

#### Chatbox Specifications

| Property | Value |
|----------|-------|
| Position | Bottom of main area |
| Height | 300px default, resizable |
| Background | `bg-gray-900/60 backdrop-blur-sm` |
| Border | `border border-gray-800 rounded-xl` |
| Messages | Scrollable with auto-scroll |

#### Message Types

```typescript
type MessageRole = 'user' | 'assistant' | 'system';

interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  actions?: ChatAction[];  // Apply to Prompt, Edit, etc.
}

interface ChatAction {
  label: string;
  type: 'apply_prompt' | 'edit' | 'regenerate' | 'search';
  targetNode?: string;
}
```

#### Quick Action Buttons

| Action | Function |
|--------|----------|
| Describe face | AI describes facial features from screenshots |
| Describe outfit | AI describes current outfit in detail |
| Find actor | Search for actor playing this character |
| Suggest poses | AI suggests poses for image generation |
| Refine prompt | AI improves the JSON prompt |

---

### 5. Generate Button

A prominent call-to-action button to submit character data for image generation.

```
+------------------------------------------------------------------+
|                                                                    |
|        +------------------------------------------------+         |
|        |  ✨  Generate Character Images                 |         |
|        |                                                |         |
|        |  Create 4 variations: Portrait, Full Body,     |         |
|        |  Action Pose, Casual Setting                   |         |
|        +------------------------------------------------+         |
|                                                                    |
+------------------------------------------------------------------+
```

#### Button States

| State | Style |
|-------|-------|
| Default | `bg-gradient-to-r from-blue-600 to-purple-600` |
| Hover | `from-blue-500 to-purple-500 scale-105` |
| Disabled | `opacity-50 cursor-not-allowed` |
| Loading | Spinner + "Generating..." text |

#### Pre-generation Checklist

Before enabling the generate button, validate:
- [ ] At least 1 face screenshot
- [ ] At least 1 full body screenshot
- [ ] Character prompt JSON is complete
- [ ] Actor metadata (optional but recommended)

---

## Interaction Flows

### Flow 1: Select Character

```
1. User clicks character in sidebar
2. Main area loads with character's nodes
3. Chatbox resets with character context
4. Generate button enabled/disabled based on data completeness
```

### Flow 2: Capture More Screenshots

```
1. User clicks [+ Capture More] on a node
2. Modal opens with video scrubber
3. User navigates to desired frame
4. Clicks "Capture" → LLAVA analyzes frame
5. If quality passes, screenshot added to node
6. Node updates with new thumbnail
```

### Flow 3: Chat Interaction

```
1. User types question in chatbox
2. AI analyzes current character data + screenshots
3. AI responds with detailed description
4. Response includes [Apply to Prompt] action
5. User clicks action → JSON prompt updated
6. Prompt node shows updated content
```

### Flow 4: Generate Images

```
1. User clicks "Generate Character Images"
2. Validation runs (checks required data)
3. If valid:
   a. Button shows loading state
   b. Progress modal appears
   c. Request sent to Nanobanana
   d. Poll for status
   e. Display generated images when complete
4. If invalid:
   a. Toast notification shows missing requirements
   b. Highlight incomplete nodes
```

---

## Component Hierarchy

```
CharacterWorkspace (fullscreen)
├── CharacterSidebar
│   ├── SidebarHeader ("Character" title)
│   ├── CharacterList
│   │   └── CharacterListItem[] (avatar, name, role)
│   └── AddCharacterButton
│
├── CharacterMainArea
│   ├── NodeGrid
│   │   ├── FaceNode
│   │   │   └── ImageThumbnailGrid
│   │   ├── BodyNode
│   │   │   └── ImageThumbnailGrid
│   │   ├── ExpressionNode
│   │   │   └── ImageThumbnailGrid
│   │   ├── PoseNode
│   │   │   └── ImageThumbnailGrid
│   │   ├── OutfitNode
│   │   │   └── ImageThumbnailGrid
│   │   ├── ActorNode
│   │   │   ├── ActorMetadataDisplay
│   │   │   └── ReferencePhotoGrid
│   │   └── PromptNode
│   │       └── JsonCodePreview
│   │
│   ├── CharacterChatbox
│   │   ├── ChatMessageList
│   │   │   └── ChatMessage[] (with actions)
│   │   ├── ChatInput
│   │   └── QuickActionBar
│   │
│   └── GenerateButton
│       └── GenerationProgress (modal)
│
└── ImageCaptureModal (overlay)
    ├── VideoScrubber
    ├── FramePreview
    └── CaptureControls
```

---

## State Management (Zustand Store)

```typescript
// frontend/src/stores/characterStore.ts

interface CharacterState {
  // Character list
  characters: Character[];
  selectedCharacterId: number | null;

  // Current character data
  currentCharacter: Character | null;
  screenshots: {
    face: Screenshot[];
    body: Screenshot[];
    expression: Screenshot[];
    pose: Screenshot[];
    outfit: Screenshot[];
  };
  actorMetadata: ActorMetadata | null;
  promptJson: CharacterPrompt | null;

  // Chat state
  chatMessages: ChatMessage[];
  chatLoading: boolean;

  // Generation state
  generationStatus: 'idle' | 'validating' | 'generating' | 'complete' | 'error';
  generationProgress: number;
  generatedImages: GeneratedImage[];

  // UI state
  expandedNodes: string[];
  captureModalOpen: boolean;
  captureNodeType: string | null;

  // Actions
  selectCharacter: (id: number) => void;
  fetchCharacterData: (id: number) => Promise<void>;
  addScreenshot: (type: string, screenshot: Screenshot) => void;
  removeScreenshot: (type: string, id: number) => void;
  updatePromptJson: (prompt: CharacterPrompt) => void;
  sendChatMessage: (message: string) => Promise<void>;
  applyAiSuggestion: (suggestion: string, targetNode: string) => void;
  generateImages: () => Promise<void>;
  toggleNodeExpanded: (nodeType: string) => void;
  openCaptureModal: (nodeType: string) => void;
  closeCaptureModal: () => void;
}
```

---

## File Structure

```
frontend/src/
├── components/
│   └── character/
│       ├── CharacterWorkspace.tsx      # Main fullscreen container
│       ├── CharacterSidebar.tsx        # Left sidebar
│       ├── CharacterListItem.tsx       # Individual list item
│       ├── NodeGrid.tsx                # Grid container for nodes
│       ├── nodes/
│       │   ├── BaseNode.tsx            # Shared node wrapper
│       │   ├── FaceNode.tsx
│       │   ├── BodyNode.tsx
│       │   ├── ExpressionNode.tsx
│       │   ├── PoseNode.tsx
│       │   ├── OutfitNode.tsx
│       │   ├── ActorNode.tsx
│       │   └── PromptNode.tsx
│       ├── CharacterChatbox.tsx        # AI chat interface
│       ├── ChatMessage.tsx             # Individual message
│       ├── QuickActionBar.tsx          # Quick action buttons
│       ├── GenerateButton.tsx          # Generate CTA
│       ├── GenerationProgress.tsx      # Progress modal
│       └── ImageCaptureModal.tsx       # Screenshot capture
│
├── stores/
│   └── characterStore.ts               # Zustand store
│
└── types/
    └── character.ts                    # TypeScript interfaces
```

---

## Styling Guidelines

### Color Scheme (matching existing theme)

```css
/* Node accent colors */
--node-face: #3b82f6;       /* Blue */
--node-body: #8b5cf6;       /* Purple */
--node-expression: #f59e0b; /* Amber */
--node-pose: #10b981;       /* Green */
--node-outfit: #ec4899;     /* Pink */
--node-actor: #f59e0b;      /* Gold */
--node-prompt: #06b6d4;     /* Cyan */

/* Chatbox */
--chat-user: #3b82f6;
--chat-assistant: #8b5cf6;
--chat-system: #6b7280;
```

### Animation Guidelines

- Node hover: `transition-all duration-200`
- Node expand: `framer-motion` with spring animation
- Chat messages: Slide in from bottom
- Generate button: Pulse animation when ready
- Loading states: `animate-pulse` or spinner

---

## Responsive Behavior

| Breakpoint | Layout Change |
|------------|---------------|
| < 768px | Sidebar becomes bottom sheet, nodes stack vertically |
| 768px - 1024px | 2-column node grid |
| 1024px - 1440px | 3-column node grid |
| > 1440px | 4-column node grid, wider chatbox |

---

## Accessibility

- All nodes keyboard navigable
- Screen reader labels for images
- Focus indicators on interactive elements
- Chatbox supports keyboard shortcuts (Enter to send)
- High contrast mode support

---

## Integration Points

1. **After AI Analysis**: Character list populated from analysis results
2. **LLAVA Integration**: Screenshot capture modal uses LLAVA for quality assessment
3. **Web Search**: Actor node triggers web search service
4. **Chatbox AI**: Uses Ollama/deepseek for conversation
5. **Nanobanana**: Generate button submits to image generation service

---

## Success Metrics

- [ ] Fullscreen workspace renders correctly
- [ ] Character list displays with face avatars
- [ ] All 7 node types display and expand properly
- [ ] Chatbox sends/receives messages
- [ ] Quick actions update relevant nodes
- [ ] Generate button validates and submits
- [ ] Generated images display in results
