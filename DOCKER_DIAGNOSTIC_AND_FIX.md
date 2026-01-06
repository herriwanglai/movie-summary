# Docker Diagnostic and Fix Guide

Since you're running Docker and I don't have Docker access, let's diagnose and fix this together.

## Step 1: Run Diagnostics

First, let's see what's happening in your container:

```bash
chmod +x diagnose-docker.sh
./diagnose-docker.sh
```

This will show:
- If `/app/src/lib/utils.ts` exists in the container
- What `vite.config.ts` looks like inside the container
- Path resolution test results
- Recent logs

**Please share the output** so I can see what's wrong.

---

## Step 2: Try Alternative Vite Config

I've created an alternative config that uses absolute paths (which work better in Docker):

```bash
# Backup current config
cp frontend/vite.config.ts frontend/vite.config.ts.backup

# Try the Docker-optimized config
cp frontend/vite.config.ts.docker-fix frontend/vite.config.ts

# Restart frontend
docker-compose restart frontend

# Watch logs
docker-compose logs -f frontend
```

### What's Different in the Alternative Config?

```typescript
// OLD (might not work in Docker):
alias: {
  '@': path.resolve(__dirname, './src'),
}

// NEW (Docker-friendly):
alias: {
  '@': '/app/src',  // Absolute path in container
}
```

Plus:
- More explicit file watching with `interval: 1000`
- Import meta URL handling
- Dependency optimization

---

## Step 3: If That Doesn't Work - Full Rebuild

```bash
# Stop everything
docker-compose down

# Clear any cache
docker-compose rm -f frontend
docker volume prune -f

# Rebuild frontend
docker-compose build --no-cache frontend

# Start everything
docker-compose up -d

# Watch logs
docker-compose logs -f frontend
```

---

## Step 4: Nuclear Option - Rebuild Everything

```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker rmi movie-summary-frontend movie-summary-backend 2>/dev/null

# Clean build
docker-compose build --no-cache

# Start
docker-compose up -d
```

---

## Step 5: Verify the Fix

Once running, check these:

```bash
# Should show VITE ready with no errors
docker-compose logs frontend | tail -30

# Test the frontend
curl http://localhost:3000

# Should return HTML, not errors
```

---

## Common Docker-Specific Issues

### Issue 1: Stale Container Cache
**Symptom:** Config changes don't take effect
**Fix:** `docker-compose restart frontend` or rebuild

### Issue 2: Wrong WORKDIR
**Symptom:** Paths don't resolve
**Fix:** Check `Dockerfile.dev` has `WORKDIR /app`

### Issue 3: Volume Mount Timing
**Symptom:** Files missing or outdated
**Fix:** Use absolute paths instead of relative

### Issue 4: Node Modules Mismatch
**Symptom:** Module resolution failures
**Fix:** Full rebuild with `--no-cache`

---

## Manual Testing Commands

Run these inside the container:

```bash
# Enter container shell
docker-compose exec frontend sh

# Check if file exists
ls -la /app/src/lib/utils.ts

# Check vite config
cat /app/vite.config.ts

# Test node resolution
node -e "console.log(require('path').resolve('/app', 'src'))"

# Try starting vite manually
npm run dev
```

---

## If Nothing Works: Run Locally

Exit Docker and run locally:

```bash
# Stop Docker
docker-compose down

# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
rm -rf node_modules/.vite
npm install
npm run dev
```

---

## What to Share With Me

If still having issues, share:

1. Output of `./diagnose-docker.sh`
2. Output of `docker-compose logs frontend | tail -50`
3. Output of `docker-compose exec frontend ls -la /app/src/lib/`
4. Your Docker and Docker Compose versions:
   ```bash
   docker --version
   docker-compose --version
   ```

This will help me understand exactly what's happening in your container!

---

## Quick Commands Reference

```bash
# Restart frontend
docker-compose restart frontend

# Rebuild frontend
docker-compose build --no-cache frontend && docker-compose up -d

# View logs
docker-compose logs -f frontend

# Enter container
docker-compose exec frontend sh

# Check services
docker-compose ps
```

---

Start with **Step 1 (diagnostics)** and **Step 2 (alternative config)** - that should fix it!
