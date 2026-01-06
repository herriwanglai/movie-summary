# METEORA LX - Docker Setup Guide

Complete guide for running METEORA LX with Docker and Docker Compose.

---

## 🐳 Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

### Install Docker

**macOS:**
```bash
brew install --cask docker
```

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

**Windows:**
Download from [docker.com](https://www.docker.com/products/docker-desktop/)

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url> movie-summary
cd movie-summary
```

### 2. Create Environment File
```bash
cp .env.example .env
# Edit .env and change passwords
```

### 3. Start All Services (Development)
```bash
docker-compose up -d
```

This starts:
- **PostgreSQL** on port 5432
- **Backend API** on port 8000
- **Frontend** on port 3000

### 4. Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📦 Docker Services

### Development Mode (Default)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Production Mode
```bash
# Build and start production services
docker-compose --profile production up -d

# Production frontend runs on port 8080 with Nginx
```

---

## 🛠️ Common Commands

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Stop Services
```bash
# Stop (keeps data)
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes (⚠️ deletes data)
docker-compose down -v
```

### Rebuild After Code Changes
```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

---

## 🗄️ Database Management

### Access PostgreSQL
```bash
docker-compose exec db psql -U meteora -d meteora_lx
```

### Run Migrations
```bash
# Backend should auto-create tables on startup
# Or run manually:
docker-compose exec backend alembic upgrade head
```

### Backup Database
```bash
docker-compose exec db pg_dump -U meteora meteora_lx > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U meteora meteora_lx < backup.sql
```

---

## 🔧 Development Workflow

### Backend Development

**Hot Reload:** Enabled by default. Changes to Python files auto-reload.

```bash
# View backend logs
docker-compose logs -f backend

# Execute commands in backend container
docker-compose exec backend python -c "print('Hello')"

# Install new Python package
docker-compose exec backend pip install package-name
# Then add to requirements.txt and rebuild
```

### Frontend Development

**Hot Reload:** Enabled with Vite. Changes auto-refresh browser.

```bash
# View frontend logs
docker-compose logs -f frontend

# Install new npm package
docker-compose exec frontend npm install package-name
# Then rebuild
docker-compose restart frontend
```

### Run Commands Inside Containers
```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# Database shell
docker-compose exec db psql -U meteora meteora_lx
```

---

## 📊 Monitoring

### Health Checks
```bash
# Check all services health
docker-compose ps

# Backend health endpoint
curl http://localhost:8000/api/health

# Frontend health
curl http://localhost:3000
```

### Resource Usage
```bash
# View container resource usage
docker stats

# View disk usage
docker system df
```

---

## 🔐 Security Notes

### For Development:
- Default passwords in `.env.example`
- CORS allows localhost origins
- SQLite works but PostgreSQL recommended

### For Production:
1. **Change all passwords** in `.env`
2. **Use strong passwords** (20+ characters)
3. **Set proper CORS_ORIGINS** (your domain only)
4. **Enable HTTPS** with reverse proxy (nginx/traefik)
5. **Use secrets management** (Docker secrets, Vault)
6. **Regular backups** of database and videos
7. **Update images** regularly for security patches

---

## 🌐 Production Deployment

### Option 1: Docker Compose (Simple)
```bash
# Use production profile
docker-compose --profile production up -d

# Frontend runs on port 8080 with Nginx
# Add reverse proxy (Nginx/Traefik) for HTTPS
```

### Option 2: Kubernetes (Scalable)
```bash
# Convert to Kubernetes manifests
kompose convert

# Or use Helm charts (create custom)
```

### Option 3: Cloud Services
- **AWS**: ECS + RDS + S3
- **Google Cloud**: Cloud Run + Cloud SQL + GCS
- **Azure**: Container Instances + PostgreSQL + Blob Storage
- **DigitalOcean**: App Platform

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows

# Or change port in docker-compose.yml
```

### Container Won't Start
```bash
# View full logs
docker-compose logs backend

# Check container status
docker-compose ps

# Remove and recreate
docker-compose down
docker-compose up -d
```

### Database Connection Issues
```bash
# Check database is healthy
docker-compose ps db

# Test connection
docker-compose exec backend python -c "
from app.database import engine
print(engine.url)
"

# Reset database
docker-compose down -v
docker-compose up -d
```

### Permission Issues (Linux)
```bash
# Fix video directory permissions
sudo chown -R $USER:$USER ./backend/videos

# Or run with user namespace
docker-compose --user $(id -u):$(id -g) up
```

### Out of Disk Space
```bash
# Clean up unused images
docker system prune -a

# Remove unused volumes
docker volume prune

# Remove everything (⚠️ careful)
docker system prune -a --volumes
```

---

## 📁 File Structure

```
movie-summary/
├── docker-compose.yml          # Main orchestration
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Example environment file
│
├── backend/
│   ├── Dockerfile             # Backend container definition
│   ├── .dockerignore          # Exclude files from image
│   ├── requirements.txt       # Python dependencies
│   └── app/                   # Application code
│
├── frontend/
│   ├── Dockerfile             # Production build
│   ├── Dockerfile.dev         # Development build
│   ├── nginx.conf             # Nginx configuration
│   ├── .dockerignore          # Exclude files from image
│   ├── package.json           # Node dependencies
│   └── src/                   # Application code
│
└── volumes/                   # Docker volumes (auto-created)
    ├── postgres_data/         # Database data
    └── videos_data/           # Uploaded videos
```

---

## 🔄 Updates and Maintenance

### Update Application Code
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Update Dependencies

**Backend:**
```bash
# Update requirements.txt
docker-compose build backend
docker-compose up -d backend
```

**Frontend:**
```bash
# Update package.json
docker-compose build frontend
docker-compose up -d frontend
```

### Update Base Images
```bash
# Pull latest base images
docker-compose pull

# Rebuild with new bases
docker-compose build --pull
```

---

## 🚀 Performance Tips

### 1. Use BuildKit (Faster builds)
```bash
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
docker-compose build
```

### 2. Layer Caching
- Dependencies installed before code copy
- Changes to code don't reinstall dependencies

### 3. Multi-stage Builds
- Production frontend uses optimized Nginx image
- Smaller final image size

### 4. Volume Mounts
- Development uses bind mounts for hot reload
- Production uses named volumes for persistence

---

## 📝 Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@db:5432/meteora_lx
VIDEO_DIR=/app/videos
MAX_UPLOAD_SIZE=10737418240  # 10GB
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
```

---

## 🎯 Next Steps

1. **Start Development:**
   ```bash
   docker-compose up -d
   ```

2. **Upload a Video:**
   - Visit http://localhost:3000
   - Click "Show Uploader"
   - Upload a video file

3. **View Timeline:**
   - Click "Phase 2: Timeline Demo"
   - See video processing results

4. **Explore API:**
   - Visit http://localhost:8000/docs
   - Test API endpoints

---

## 🆘 Getting Help

### Check Logs First
```bash
docker-compose logs -f
```

### Common Issues
1. Port conflicts → Change ports in docker-compose.yml
2. Permission errors → Check file ownership
3. Memory issues → Increase Docker memory limit
4. Network errors → Check firewall/antivirus

### Useful Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)

---

**Last Updated:** January 6, 2026
**Docker Version:** 20.10+
**Compose Version:** 2.0+

**Status:** ✅ Production Ready
