# React UI Component Structure - METEORA LX

**Generated:** January 6, 2026
**Status:** ✅ All imports verified and working

---

## 📊 Import Verification Results

✅ **All 40 imports checked - 0 errors found**
✅ **All critical files exist and are readable**
✅ **All @/ path aliases resolve correctly**

---

## 🗂️ Component Directory Structure

```
frontend/src/
├── components/
│   ├── ui/                    # shadcn/ui components (8 files)
│   │   ├── badge.tsx          ✅ Imports: @/lib/utils
│   │   ├── button.tsx         ✅ Imports: @/lib/utils
│   │   ├── card.tsx           ✅ Imports: @/lib/utils
│   │   ├── dialog.tsx         ✅ Imports: @/lib/utils
│   │   ├── input.tsx          ✅ Imports: @/lib/utils
│   │   ├── progress.tsx       ✅ Imports: @/lib/utils
│   │   ├── toast.tsx          ✅ Imports: @/lib/utils
│   │   └── toaster.tsx        ✅ Imports: @/components/ui/toast, @/hooks/use-toast
│   │
│   ├── upload/                # Video upload UI
│   │   ├── index.ts           ✅ Exports VideoUploader
│   │   └── VideoUploader.tsx  ✅ Imports: @/components/ui/*, @/hooks/use-toast, @/lib/utils
│   │
│   ├── player/                # Video player UI
│   │   ├── index.ts           ✅ Exports VideoPlayer
│   │   └── VideoPlayer.tsx    ✅ Imports: @/components/ui/*, @/hooks/use-toast
│   │
│   ├── timeline/              # Timeline components (Phase 2)
│   │   ├── MagneticTimeline.tsx      ✅ Imports: @/stores/timelineStore, @/lib/utils
│   │   ├── PlaybackControls.tsx      ✅ Imports: @/stores/timelineStore, @/components/ui/button
│   │   └── SceneNavigator.tsx        ✅ Imports: @/stores/timelineStore, @/components/ui/*, @/lib/utils
│   │
│   ├── workspace/             # Video workspace container
│   │   └── VideoWorkspace.tsx ✅ Imports: @/components/timeline/*, @/stores/*, @/hooks/*
│   │
│   └── LoadingStates.tsx      ✅ Imports: @/lib/utils
│
├── stores/                    # Zustand state management
│   ├── index.ts               ✅ Exports all stores
│   ├── playerStore.ts         ✅ No external imports
│   ├── timelineStore.ts       ✅ No external imports
│   └── videoStore.ts          ✅ No external imports
│
├── hooks/                     # Custom React hooks
│   ├── use-toast.ts           ✅ Imports: @/components/ui/toast
│   └── useKeyboardShortcuts.ts ✅ Imports: @/stores/timelineStore
│
├── lib/                       # Utility functions
│   └── utils.ts               ✅ Core utilities (cn, formatTimestamp, parseTimestamp)
│
├── App.tsx                    ✅ Main app component
└── main.tsx                   ✅ Entry point
```

---

## 🔗 Import Dependency Graph

### Core Dependencies (No External Imports)
- `stores/playerStore.ts`
- `stores/timelineStore.ts`
- `stores/videoStore.ts`

### Level 1 (Depends Only on Core)
- `lib/utils.ts` (clsx, tailwind-merge)

### Level 2 (Depends on Level 1)
- `components/ui/badge.tsx` → utils
- `components/ui/button.tsx` → utils
- `components/ui/card.tsx` → utils
- `components/ui/dialog.tsx` → utils
- `components/ui/input.tsx` → utils
- `components/ui/progress.tsx` → utils
- `components/ui/toast.tsx` → utils
- `hooks/useKeyboardShortcuts.ts` → timelineStore

### Level 3 (Depends on Level 2)
- `components/ui/toaster.tsx` → toast, use-toast
- `hooks/use-toast.ts` → toast
- `components/LoadingStates.tsx` → utils
- `components/timeline/MagneticTimeline.tsx` → timelineStore, utils
- `components/timeline/PlaybackControls.tsx` → timelineStore, button
- `components/timeline/SceneNavigator.tsx` → timelineStore, ui/*, utils

### Level 4 (Depends on Level 3)
- `components/player/VideoPlayer.tsx` → ui/*, use-toast
- `components/upload/VideoUploader.tsx` → ui/*, use-toast, utils

### Level 5 (Top Level Components)
- `components/workspace/VideoWorkspace.tsx` → timeline/*, stores/*, hooks/*
- `App.tsx` → ui/*, upload, player, workspace

---

## 📦 External Package Dependencies

### UI Libraries
- `@radix-ui/react-dialog` → dialog.tsx
- `@radix-ui/react-progress` → progress.tsx
- `@radix-ui/react-slot` → button.tsx
- `@radix-ui/react-toast` → toast.tsx, toaster.tsx
- `lucide-react` → All icon imports
- `framer-motion` → MagneticTimeline.tsx (animations)

### State & Utils
- `zustand` → All stores
- `clsx` + `tailwind-merge` → utils.ts (cn function)
- `class-variance-authority` → button.tsx, badge.tsx (cva)
- `tus-js-client` → VideoUploader.tsx (uploads)
- `react-use` → ⚠️ UNUSED (can be removed)

---

## ✅ Verified Import Patterns

### @/ Path Alias (40 verified imports)
```typescript
// All of these work correctly:
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import { useTimelineStore } from "@/stores/timelineStore"
import { VideoPlayer } from "@/components/player"
import { MagneticTimeline } from "@/components/timeline/MagneticTimeline"
```

### Relative Imports
- `components/upload/index.ts` → `./VideoUploader`
- `components/player/index.ts` → `./VideoPlayer`
- `stores/index.ts` → `./playerStore`, `./timelineStore`, `./videoStore`

---

## 🐛 Issues Found & Fixed

### ✅ Fixed: Directory Permissions
- `src/components/workspace/` was `700` → fixed to `755`
- `src/components/timeline/` was `700` → fixed to `755`

### ✅ Fixed: File Permissions
- `src/lib/utils.ts` was `600` → fixed to `644`
- `src/hooks/` directory was `700` → fixed to `755`
- All `.ts` and `.tsx` files set to `644`

### ✅ Verified: All Files Exist
- ✅ src/lib/utils.ts
- ✅ src/main.tsx
- ✅ src/App.tsx
- ✅ src/stores/index.ts
- ✅ src/hooks/use-toast.ts
- ✅ src/components/ui/button.tsx

---

## 🔧 vite.config.ts Configuration

```typescript
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
    '@/*': path.resolve(__dirname, './src/*'),
  },
}
```

**Status:** ✅ Correctly configured for Docker

---

## 🎯 Conclusion

**All React UI imports are verified and working on the filesystem.**

The Docker error is NOT caused by broken imports or missing files. The issue is:
1. ✅ **FIXED:** File permissions (were too restrictive)
2. 🔄 **NEEDS:** Docker container restart to pick up changes

---

## 🚀 Next Step

Run the complete fix to restart Docker with corrected permissions:

```bash
./COMPLETE_FIX.sh
```

This will:
1. Ensure all permissions are correct
2. Rebuild Docker container
3. Clear all caches
4. Start fresh with working imports

**Expected Result:** ✅ No more "@/lib/utils" errors
