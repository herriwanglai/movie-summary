# Docker Module Resolution Fix

## Issue
When running METEORA LX with Docker Compose, you may encounter this error:

```
Failed to resolve import "@/lib/utils" from "src/App.tsx". Does the file exist?
```

## Root Cause
The path alias `@` configured in `vite.config.ts` is not being resolved correctly inside the Docker container. This can happen due to:

1. **Stale node_modules**: The `/app/node_modules` volume in Docker may contain cached modules that don't match the current `package.json`
2. **Volume mount timing**: The bind mount `./frontend:/app` may override files before Vite initializes
3. **File watching issues**: Docker volume mounts require polling for file changes on some systems

## Solution 1: Rebuild Frontend Container (Recommended)

Stop and rebuild the frontend container to ensure fresh dependencies:

```bash
# Stop all services
docker-compose down

# Remove the frontend container and its volumes
docker-compose rm -f frontend
docker volume rm movie-summary_frontend_node_modules 2>/dev/null

# Rebuild frontend container with no cache
docker-compose build --no-cache frontend

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f frontend
```

## Solution 2: Quick Restart

If you just need to restart the frontend:

```bash
# Restart frontend service
docker-compose restart frontend

# Watch logs for errors
docker-compose logs -f frontend
```

## Solution 3: Nuclear Option (If Above Don't Work)

Complete clean rebuild of all services:

```bash
# Stop everything
docker-compose down -v

# Remove all containers and images
docker-compose rm -f
docker rmi $(docker images 'movie-summary*' -q) 2>/dev/null

# Rebuild from scratch
docker-compose build --no-cache

# Start services
docker-compose up -d
```

## Solution 4: Run Locally (Without Docker)

If Docker issues persist, run services locally:

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm install  # Ensure dependencies are fresh
rm -rf node_modules/.vite  # Clear Vite cache
npm run dev

# Access at http://localhost:3000
```

## Verify the Fix

After applying any solution, verify it works:

```bash
# Check frontend logs for errors
docker-compose logs frontend | grep -i error

# Check if frontend is accessible
curl http://localhost:3000

# Check API connectivity from frontend
docker-compose exec frontend wget -q -O- http://backend:8000/api/health
```

## What Was Fixed

### vite.config.ts Updates

Added Docker-specific configuration:

```typescript
server: {
  host: '0.0.0.0',        // Allow external connections (required for Docker)
  port: 3000,
  watch: {
    usePolling: true,     // Required for Docker volume mounts
  },
  // ... rest of config
}
```

### Why This Helps

- **host: '0.0.0.0'**: Allows Vite to accept connections from outside the container
- **usePolling: true**: Forces Vite to poll for file changes instead of using filesystem events (which don't work reliably with Docker volumes)

## Prevention

To avoid this issue in the future:

1. **Always rebuild after package.json changes**:
   ```bash
   docker-compose build frontend
   docker-compose up -d frontend
   ```

2. **Clear Vite cache if you see weird errors**:
   ```bash
   docker-compose exec frontend rm -rf node_modules/.vite
   docker-compose restart frontend
   ```

3. **Check logs regularly**:
   ```bash
   docker-compose logs -f frontend
   ```

## Alternative: Development Without Hot Reload

If hot reload continues to cause issues, you can run a production build:

```bash
# Build production image
docker-compose --profile production up -d

# Frontend will run on port 8080 with Nginx
# Access at http://localhost:8080
```

Note: This doesn't have hot reload, so you'll need to rebuild after code changes:

```bash
docker-compose --profile production build frontend-prod
docker-compose --profile production up -d frontend-prod
```

## Still Having Issues?

If none of these solutions work, check:

1. **Docker version**: Ensure you're running Docker 20.10+ and Docker Compose 2.0+
   ```bash
   docker --version
   docker-compose --version
   ```

2. **File permissions**: Ensure your user owns the project files
   ```bash
   ls -la frontend/src/lib/utils.ts
   # Should show your username, not root
   ```

3. **Disk space**: Ensure you have enough disk space
   ```bash
   df -h
   docker system df
   ```

4. **Try a different Docker driver**: If using Docker Desktop on Mac/Windows, try adjusting resources in Docker Desktop settings

## Technical Details

### File Structure
```
frontend/
├── src/
│   ├── lib/
│   │   └── utils.ts          ← This file exists
│   ├── App.tsx                ← Imports from @/lib/utils
│   └── ...
├── vite.config.ts             ← Defines @ alias
├── tsconfig.app.json          ← TypeScript @ alias
└── package.json
```

### Path Alias Configuration

**vite.config.ts**:
```typescript
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

**tsconfig.app.json**:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Both configurations are correct. The issue is with how Docker resolves these paths at runtime.

---

**Last Updated:** January 6, 2026
**Status:** ✅ Fixed in latest commit
