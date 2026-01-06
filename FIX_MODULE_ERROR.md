# Fix: "@/lib/utils" Module Resolution Error

You're seeing: `Failed to resolve import "@/lib/utils" from "src/App.tsx"`

## Solution Levels (Try in Order)

### Level 1: Quick Restart (Try This First!) ⚡

Since your code is bind-mounted, a restart should pick up the config changes:

```bash
chmod +x QUICK_RESTART.sh
./QUICK_RESTART.sh
```

**OR manually:**
```bash
docker-compose restart frontend
docker-compose logs -f frontend
```

If you see "VITE ready" with no errors → **DONE!** ✅

If still seeing errors → Try Level 2

---

### Level 2: Rebuild Frontend Container 🔨

The container's cached configuration needs updating:

```bash
chmod +x fix-docker.sh
./fix-docker.sh
```

**OR manually:**
```bash
docker-compose down
docker-compose build --no-cache frontend
docker-compose up -d
docker-compose logs -f frontend
```

If you see "VITE ready" with no errors → **DONE!** ✅

If still seeing errors → Try Level 3

---

### Level 3: Nuclear Option 💣

Complete rebuild of everything:

```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker rmi $(docker images 'movie-summary*' -q) 2>/dev/null

# Rebuild everything
docker-compose build --no-cache

# Start services
docker-compose up -d

# Monitor
docker-compose logs -f
```

If still seeing errors → Try Level 4

---

### Level 4: Run Locally (Without Docker) 💻

If Docker continues to have issues, run locally:

**Terminal 1 - Backend:**
```bash
cd /home/user/movie-summary/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd /home/user/movie-summary/frontend
npm install
rm -rf node_modules/.vite  # Clear cache
npm run dev
```

Access at: http://localhost:3000

---

## What Fixed the Issue

The `vite.config.ts` has been updated with Docker-specific settings:

```typescript
server: {
  host: '0.0.0.0',        // Allow external Docker access
  port: 3000,
  watch: {
    usePolling: true,     // Required for Docker volumes
  },
  // ...
}
```

**The fix is already in your code** - your container just needs to pick it up!

---

## Verify Success

After any fix, you should see:

```
VITE v7.3.0  ready in XXX ms
➜  Local:   http://localhost:3000/
➜  Network: http://172.x.x.x:3000/
```

And **NO** "@/lib/utils" errors!

---

## Need Help?

**Check what's running:**
```bash
docker-compose ps
```

**View all logs:**
```bash
docker-compose logs
```

**Check if file exists in container:**
```bash
docker-compose exec frontend ls -la /app/src/lib/utils.ts
```

**Check vite.config.ts in container:**
```bash
docker-compose exec frontend cat /app/vite.config.ts
```

---

**Start with Level 1** - it's the quickest! 🚀
