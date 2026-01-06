# METEORA LX - Playwright Testing Strategy

## Overview

Integration of **Playwright** for comprehensive E2E and component testing throughout the development lifecycle.

---

## 🎭 Why Playwright for METEORA LX?

### **Perfect Fit for Our Stack**

✅ **TypeScript-First** - Native TypeScript support (already our language)
✅ **React Testing** - Excellent React integration
✅ **Dark Mode Testing** - Can test theme switching
✅ **Video Testing** - Can interact with video players (Vidstack)
✅ **File Upload Testing** - Can test Uppy drag-drop and TUS uploads
✅ **Multi-Browser** - Test on Chromium, Firefox, WebKit
✅ **Fast & Reliable** - Auto-wait, no flaky tests
✅ **CI/CD Ready** - Built-in GitHub Actions support
✅ **Visual Regression** - Screenshot comparison for UI

---

## 🏗️ Testing Architecture

### **Option A: Testing Sub-Agents** (Recommended)

Each implementation agent spawns a testing sub-agent that:
1. **Learns** Playwright best practices
2. **Writes tests** alongside feature implementation
3. **Validates** the feature before marking complete
4. **Reports** test results to main agent

**Benefits:**
- Tests written immediately (no backlog)
- Features validated before integration
- Faster feedback loop
- Test knowledge specific to feature

**Structure:**
```
Agent 1: Frontend UI
├── Implementation
└── Testing Sub-Agent
    ├── Learns Playwright + React Testing Library
    ├── Writes E2E tests for upload flow
    ├── Writes component tests for VideoPlayer
    └── Validates UI in dark mode

Agent 2: Backend API
├── Implementation
└── Testing Sub-Agent
    ├── Learns Playwright API testing
    ├── Writes API endpoint tests
    └── Validates TUS upload flow

Agent 3: Video Processing
├── Implementation
└── Testing Sub-Agent
    ├── Learns Playwright file system testing
    ├── Writes integration tests
    └── Validates scene detection accuracy
```

---

### **Option B: Dedicated Testing Agent** (Alternative)

A separate agent focused solely on testing after implementation.

**Agent 15: E2E Testing Specialist**
- Writes comprehensive test suites
- Sets up CI/CD integration
- Creates test reports
- **Estimate:** 6-8 hours

**Benefits:**
- Specialized testing expertise
- Consistent testing patterns
- Comprehensive coverage

**Drawbacks:**
- Tests written after implementation
- Slower feedback
- Potential test backlog

---

## 📋 Playwright Integration Plan

### **Phase 1: Setup** (30 minutes)

**Installation:**
```bash
npm install -D @playwright/test
npx playwright install
```

**Configuration:** `playwright.config.ts`
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

---

### **Phase 2: Core Tests** (Per Agent)

#### **Agent 1 Testing Sub-Agent: Frontend E2E Tests**

**File:** `e2e/video-upload.spec.ts`

```typescript
import { test, expect } from '@playwright/test'
import path from 'path'

test.describe('Video Upload Flow', () => {
  test('should upload video via drag-and-drop', async ({ page }) => {
    await page.goto('/')

    // Navigate to upload page
    await page.click('text=Upload Video')

    // Drag-drop file
    const filePath = path.join(__dirname, 'fixtures', 'sample-video.mp4')
    const fileInput = await page.locator('input[type="file"]')
    await fileInput.setInputFiles(filePath)

    // Wait for Uppy to process
    await expect(page.locator('.uppy-Dashboard-Item-name')).toContainText('sample-video.mp4')

    // Start upload
    await page.click('text=Upload')

    // Wait for progress
    await expect(page.locator('.uppy-ProgressBar')).toBeVisible()

    // Wait for completion
    await expect(page.locator('text=Upload complete')).toBeVisible({ timeout: 60000 })
  })

  test('should play uploaded video', async ({ page }) => {
    await page.goto('/videos/1')

    // Vidstack player should be visible
    const player = page.locator('media-player')
    await expect(player).toBeVisible()

    // Click play
    await page.click('[aria-label="Play"]')

    // Video should start playing
    await page.waitForTimeout(2000)
    const isPaused = await player.getAttribute('data-paused')
    expect(isPaused).toBe('false')
  })

  test('should take screenshot from video', async ({ page }) => {
    await page.goto('/videos/1')

    // Pause at specific time
    const player = page.locator('media-player')
    await page.click('[aria-label="Play"]')
    await page.waitForTimeout(3000)
    await page.click('[aria-label="Pause"]')

    // Take screenshot
    await page.click('button:has-text("Take Screenshot")')

    // Screenshot should appear in collection
    await expect(page.locator('.screenshot-item')).toHaveCount(1)
  })
})

test.describe('Dark Mode', () => {
  test('should render in dark mode by default', async ({ page }) => {
    await page.goto('/')

    // Check background color (dark theme)
    const body = page.locator('body')
    const bgColor = await body.evaluate(el =>
      window.getComputedStyle(el).backgroundColor
    )
    expect(bgColor).toContain('10, 10, 15') // #0a0a0f
  })
})
```

**File:** `e2e/component-tests/video-player.spec.tsx`

```typescript
import { test, expect } from '@playwright/experimental-ct-react'
import VideoPlayer from '@/components/player/VideoPlayer'

test('VideoPlayer renders and plays', async ({ mount, page }) => {
  const component = await mount(
    <VideoPlayer src="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4" />
  )

  await expect(component).toBeVisible()

  // Play button should exist
  const playButton = page.locator('[aria-label="Play"]')
  await expect(playButton).toBeVisible()

  // Click play
  await playButton.click()

  // Should start playing
  await page.waitForTimeout(1000)
  const player = page.locator('media-player')
  const isPaused = await player.getAttribute('data-paused')
  expect(isPaused).toBe('false')
})
```

---

#### **Agent 2 Testing Sub-Agent: Backend API Tests**

**File:** `e2e/api/upload.spec.ts`

```typescript
import { test, expect } from '@playwright/test'

test.describe('TUS Upload API', () => {
  test('should create upload session', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/upload', {
      headers: {
        'Upload-Length': '1000000',
        'Upload-Metadata': 'filename dGVzdC12aWRlby5tcDQ=', // base64: test-video.mp4
      },
    })

    expect(response.status()).toBe(201)
    expect(response.headers()['location']).toBeTruthy()
  })

  test('should upload chunks via PATCH', async ({ request }) => {
    // Create upload
    const createResponse = await request.post('http://localhost:8000/api/upload', {
      headers: {
        'Upload-Length': '100',
        'Upload-Metadata': 'filename dGVzdC5tcDQ=',
      },
    })

    const uploadUrl = createResponse.headers()['location']

    // Upload chunk
    const chunk = Buffer.from('test data chunk')
    const patchResponse = await request.patch(uploadUrl, {
      headers: {
        'Upload-Offset': '0',
        'Content-Type': 'application/offset+octet-stream',
      },
      data: chunk,
    })

    expect(patchResponse.status()).toBe(204)
    expect(patchResponse.headers()['upload-offset']).toBe(chunk.length.toString())
  })
})

test.describe('Video API', () => {
  test('should list uploaded videos', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/videos')

    expect(response.status()).toBe(200)
    const videos = await response.json()
    expect(Array.isArray(videos)).toBe(true)
  })
})
```

---

#### **Agent 3 Testing Sub-Agent: Video Processing Tests**

**File:** `e2e/processing/scene-detection.spec.ts`

```typescript
import { test, expect } from '@playwright/test'
import { VideoProcessingPipeline } from '@/src/video_processor/pipeline'
import path from 'path'

test.describe('Video Processing', () => {
  test('should detect scenes in video', async () => {
    const videoPath = path.join(__dirname, '../fixtures/test-video.mp4')
    const pipeline = new VideoProcessingPipeline(videoPath)

    const result = await pipeline.process()

    expect(result.scenes.length).toBeGreaterThan(0)
    expect(result.scenes[0]).toHaveProperty('start_time')
    expect(result.scenes[0]).toHaveProperty('end_time')
    expect(result.scenes[0]).toHaveProperty('importance_score')
  })

  test('should extract keyframes', async () => {
    const videoPath = path.join(__dirname, '../fixtures/test-video.mp4')
    const pipeline = new VideoProcessingPipeline(videoPath)

    const result = await pipeline.process()

    expect(result.total_keyframes).toBeGreaterThan(0)
    result.scenes.forEach(scene => {
      expect(scene.keyframes.length).toBeGreaterThan(0)
    })
  })
})
```

---

## 🎯 Test Coverage Goals

### **MVP (Phase 1)**
- ✅ Video upload flow (E2E)
- ✅ Upload progress tracking
- ✅ Video playback
- ✅ Screenshot capture
- ✅ API endpoint tests
- ✅ Scene detection
- ✅ Dark mode rendering

**Target Coverage:** 70-80%

---

### **Full Project**
- All MVP tests
- Timeline navigation
- Collection manager CRUD
- Node editor interactions
- AI caption generation
- Ink export validation
- Keyboard shortcuts
- Accessibility (ARIA)
- Visual regression tests

**Target Coverage:** 85-90%

---

## 🚀 CI/CD Integration

### **GitHub Actions Workflow**

**File:** `.github/workflows/playwright.yml`

```yaml
name: Playwright Tests

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test

      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

---

## 📊 Estimated Time for Testing

### **Per Agent Testing Sub-Agent**

| Agent | Testing Sub-Agent Time | What They Test |
|-------|----------------------|----------------|
| Agent 1 | 1.5-2 hours | Upload UI, Video Player, Dark Mode |
| Agent 2 | 1-1.5 hours | API Endpoints, TUS Protocol |
| Agent 3 | 1.5-2 hours | Scene Detection, Keyframe Extraction |

**Total Testing Time (MVP):** 4-5.5 hours (parallel with implementation)

### **Dedicated Testing Agent (Alternative)**

**Agent 15: E2E Testing**
- Setup Playwright: 30 min
- Write MVP test suite: 4-5 hours
- CI/CD integration: 1 hour
- Visual regression tests: 1-2 hours

**Total:** 6.5-8.5 hours (after implementation complete)

---

## 🎭 Recommendation: Testing Sub-Agents

**Use testing sub-agents** for:
1. ✅ Faster feedback (tests written with features)
2. ✅ Better test quality (fresh context)
3. ✅ No test backlog
4. ✅ Parallel execution
5. ✅ Feature-specific expertise

**Implementation:**
```
For each implementation agent:
├── Main Agent (implements feature)
└── Testing Sub-Agent
    ├── Learn Playwright for this feature
    ├── Write tests alongside implementation
    ├── Run tests before marking complete
    └── Report coverage metrics
```

---

## 📝 Testing Best Practices

### **From Playwright Documentation:**

1. **Auto-Wait:** Playwright waits for elements before acting
2. **Isolation:** Each test runs in isolation (fresh context)
3. **Selectors:** Use user-facing selectors (text, aria-label)
4. **TypeScript:** Full type safety in tests
5. **Debugging:** Built-in trace viewer for failures
6. **Visual Testing:** Screenshot comparison for UI changes

---

## ✅ Success Criteria

**Testing is successful when:**
1. ✅ All critical user flows covered
2. ✅ Tests run in CI/CD on every commit
3. ✅ <5% flaky tests
4. ✅ Fast execution (<5 min for full suite)
5. ✅ Clear failure reports with traces
6. ✅ 80%+ code coverage for MVP
7. ✅ Visual regression tests prevent UI breaks

---

**Sources:**
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [E2E Testing React with Playwright Guide](https://medium.com/@oshadhadushan/end-to-end-testing-in-react-with-playwright-a-step-by-step-integration-guide-00e32effbd15)
- [Playwright End to End Testing Complete Guide](https://luxequality.com/blog/playwright-end-to-end-testing/)
- [Modern React Testing with Playwright](https://sapegin.me/blog/react-testing-5-playwright/)
- [E2E Testing React Playwright](https://articles.mergify.com/e-2-e-testing-react-playwright/)
- [Playwright Component Testing Guide](https://devsquad.com/blog/playwright-component-testing)
- [E2E Test Architecture with Playwright TypeScript](https://medium.com/@denisskvrtsv/a-simple-and-effective-e2e-test-architecture-with-playwright-and-typescript-913c62ce0e89)

---

**Last Updated:** January 6, 2026
**Strategy:** Testing Sub-Agents (Recommended)
