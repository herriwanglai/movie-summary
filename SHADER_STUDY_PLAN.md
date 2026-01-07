# WebGL Shader Study Plan

**Goal:** Learn WebGL shaders to recreate Unicorn Studio-style effects and export them to JSON format.

**Reference Effect:** https://www.unicorn.studio/embed/jYxrWzSRtsXNqZADHnVH

---

## Phase 1: WebGL & GLSL Fundamentals

### 1.1 WebGL Basics
- [ ] Understand WebGL rendering pipeline
- [ ] Learn to set up a WebGL context in JavaScript
- [ ] Create basic vertex and fragment shaders
- [ ] Understand uniforms, attributes, and varyings
- [ ] Learn to pass data between JavaScript and shaders

### 1.2 GLSL Language Essentials
- [ ] Data types: `float`, `vec2`, `vec3`, `vec4`, `mat4`, `sampler2D`
- [ ] Built-in functions: `mix()`, `step()`, `smoothstep()`, `clamp()`
- [ ] Math functions: `sin()`, `cos()`, `pow()`, `abs()`, `fract()`, `mod()`
- [ ] Vector operations: `dot()`, `cross()`, `normalize()`, `length()`, `distance()`
- [ ] Texture sampling: `texture2D()`

### 1.3 Coordinate Systems
- [ ] Normalized device coordinates (NDC)
- [ ] UV coordinates (0.0 to 1.0)
- [ ] Screen-space coordinates
- [ ] Transforming between coordinate systems

---

## Phase 2: Core Shader Techniques

### 2.1 Color & Gradients
- [ ] Linear gradients
- [ ] Radial gradients
- [ ] Angular/conic gradients
- [ ] Multi-stop gradients with `mix()`
- [ ] Color blending modes (multiply, screen, overlay, etc.)

### 2.2 Noise Functions
- [ ] Random/hash functions
- [ ] Value noise
- [ ] Perlin noise
- [ ] Simplex noise
- [ ] Fractal Brownian Motion (fBm)
- [ ] Worley/cellular noise

### 2.3 Shapes & SDFs (Signed Distance Functions)
- [ ] Circle SDF
- [ ] Rectangle/rounded rectangle SDF
- [ ] Line segment SDF
- [ ] Combining shapes (union, intersection, subtraction)
- [ ] Smooth blending between shapes

### 2.4 Distortion Effects
- [ ] Wave distortion (sine waves)
- [ ] Ripple effects
- [ ] Twist/swirl distortion
- [ ] Lens distortion
- [ ] Displacement mapping

---

## Phase 3: Advanced Visual Effects

### 3.1 Lighting & Shading
- [ ] Ambient lighting
- [ ] Diffuse lighting (Lambert)
- [ ] Specular highlights (Phong/Blinn-Phong)
- [ ] Normal mapping
- [ ] Fresnel effect

### 3.2 Post-Processing Effects
- [ ] Blur (box blur, Gaussian blur)
- [ ] Bloom/glow effect
- [ ] Chromatic aberration
- [ ] Vignette
- [ ] Film grain
- [ ] Color grading / LUT

### 3.3 Particle & Motion Effects
- [ ] Particle systems in shaders
- [ ] Motion blur
- [ ] Trail effects
- [ ] Fluid simulation basics

### 3.4 Texture Effects
- [ ] Texture tiling and offset
- [ ] Texture masking
- [ ] Multi-texture blending
- [ ] Procedural textures

---

## Phase 4: Animation & Interactivity

### 4.1 Time-Based Animation
- [ ] Using `uniform float u_time`
- [ ] Easing functions in GLSL
- [ ] Looping animations
- [ ] Keyframe-style animations

### 4.2 Interactive Effects
- [ ] Mouse position tracking (`u_mouse`)
- [ ] Hover effects
- [ ] Click/touch interactions
- [ ] Scroll-based animations
- [ ] Gyroscope/device orientation

### 4.3 Audio Reactivity (Optional)
- [ ] Frequency analysis with Web Audio API
- [ ] Passing audio data to shaders
- [ ] Beat detection visualization

---

## Phase 5: Layer Composition System

### 5.1 Multi-Layer Rendering
- [ ] Framebuffer Objects (FBOs)
- [ ] Render-to-texture
- [ ] Layer blending modes
- [ ] Alpha compositing
- [ ] Layer ordering and z-index

### 5.2 Effect Chaining
- [ ] Ping-pong buffer technique
- [ ] Effect stack architecture
- [ ] Parameter interpolation between effects

---

## Phase 6: JSON Export Format Design

### 6.1 Schema Design
- [ ] Define base effect schema
- [ ] Layer configuration format
- [ ] Animation keyframe format
- [ ] Interaction event format
- [ ] Asset references (textures, images)

### 6.2 Example JSON Structure
```json
{
  "name": "CustomEffect",
  "version": "1.0",
  "canvas": {
    "width": 1920,
    "height": 1080,
    "pixelRatio": 2
  },
  "layers": [
    {
      "id": "layer-1",
      "type": "shader",
      "shader": "gradient",
      "uniforms": {
        "u_color1": [1.0, 0.0, 0.5, 1.0],
        "u_color2": [0.0, 0.5, 1.0, 1.0],
        "u_angle": 45
      },
      "blendMode": "normal",
      "opacity": 1.0
    },
    {
      "id": "layer-2",
      "type": "shader",
      "shader": "noise",
      "uniforms": {
        "u_scale": 3.0,
        "u_speed": 0.5,
        "u_octaves": 4
      },
      "blendMode": "overlay",
      "opacity": 0.5
    }
  ],
  "animations": [
    {
      "target": "layer-2.uniforms.u_scale",
      "keyframes": [
        { "time": 0, "value": 3.0 },
        { "time": 2000, "value": 5.0, "easing": "easeInOut" }
      ],
      "loop": true
    }
  ],
  "interactions": [
    {
      "type": "mousemove",
      "target": "layer-1.uniforms.u_mouse",
      "mapping": "normalized"
    }
  ],
  "shaderLibrary": {
    "gradient": {
      "vertex": "...",
      "fragment": "..."
    },
    "noise": {
      "vertex": "...",
      "fragment": "..."
    }
  }
}
```

### 6.3 Export Features
- [ ] Serialize shader code
- [ ] Export uniform values
- [ ] Bundle textures (base64 or URLs)
- [ ] Minify shader code
- [ ] Validate schema

---

## Phase 7: Implementation Project

### 7.1 Build the Runtime Engine
- [ ] Create WebGL renderer class
- [ ] Implement shader compiler/linker
- [ ] Build uniform management system
- [ ] Create layer compositor
- [ ] Implement animation system
- [ ] Add interaction handlers

### 7.2 Build the Effect Library
- [ ] Implement 10+ reusable effects:
  - [ ] Gradient
  - [ ] Noise
  - [ ] Wave distortion
  - [ ] Blur
  - [ ] Glow/bloom
  - [ ] Chromatic aberration
  - [ ] Vignette
  - [ ] Color shift
  - [ ] Ripple
  - [ ] Morph/displacement

### 7.3 JSON Import/Export
- [ ] Build JSON parser for effect configs
- [ ] Create export function
- [ ] Add import validation
- [ ] Test round-trip (export → import → render)

### 7.4 Testing & Optimization
- [ ] Test on multiple browsers
- [ ] Profile GPU performance
- [ ] Optimize shader code
- [ ] Add fallbacks for unsupported features

---

## Learning Resources

### Books & Courses
- [The Book of Shaders](https://thebookofshaders.com/) - Essential GLSL tutorial
- [WebGL Fundamentals](https://webglfundamentals.org/) - Comprehensive WebGL guide
- [Learn OpenGL](https://learnopengl.com/) - Concepts apply to WebGL
- [Shadertoy](https://www.shadertoy.com/) - Shader examples and inspiration

### Tools
- [Shadertoy](https://www.shadertoy.com/) - Online shader editor
- [GLSL Sandbox](http://glslsandbox.com/) - Shader playground
- [Shader Editor VS Code Extension](https://marketplace.visualstudio.com/items?itemName=circledev.glsl-canvas)
- [Unicorn Studio](https://www.unicorn.studio/) - Reference for effect types

### Reference Code
- [Three.js ShaderMaterial](https://threejs.org/docs/#api/en/materials/ShaderMaterial)
- [GLSL Noise Functions](https://gist.github.com/patriciogonzalezvivo/670c22f3966e662d2f83)
- [Lygia Shader Library](https://lygia.xyz/)

---

## Progress Tracking

| Phase | Status | Completion Date |
|-------|--------|-----------------|
| Phase 1: Fundamentals | Not Started | |
| Phase 2: Core Techniques | Not Started | |
| Phase 3: Advanced Effects | Not Started | |
| Phase 4: Animation | Not Started | |
| Phase 5: Layer System | Not Started | |
| Phase 6: JSON Format | Not Started | |
| Phase 7: Implementation | Not Started | |

---

## Notes

_Use this section to document learnings, challenges, and solutions as you progress._

---

**Created:** 2026-01-07
**Last Updated:** 2026-01-07
