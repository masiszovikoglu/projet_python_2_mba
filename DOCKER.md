# 🐳 Docker Guide - Banking Transactions API

Complete guide for running the Banking Transactions API in Docker containers.

---

## 📋 Prerequisites

- **Docker** installed ([Download Docker](https://www.docker.com/products/docker-desktop))
- **Docker Compose** installed (included with Docker Desktop)
- **Data file**: `bs140513_032310.csv` from Kaggle

---

## 🚀 Quick Start with Docker

### Method 1: Using Docker Compose (Recommended)

```bash
# 1. Place your data file in the data/ folder
# Make sure the file is: data/bs140513_032310.csv

# 2. Build and start the container
docker-compose up --build

# 3. Access the API
# Open: http://localhost:8000/docs
```

### Method 2: Using Docker CLI

```bash
# 1. Build the Docker image
docker build -t banking-api:1.0.0 .

# 2. Run the container
docker run -d \
  --name banking-api \
  -p 8000:8000 \
  -v ${PWD}/data:/app/data \
  -e DATA_PATH=/app/data/bs140513_032310.csv \
  banking-api:1.0.0

# 3. Check logs
docker logs -f banking-api

# 4. Access the API
# Open: http://localhost:8000/docs
```

---

## 📁 Project Structure for Docker

```
projet_python_2_mba/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── data/                   # Data directory (mounted as volume)
│   └── bs140513_032310.csv # Your Kaggle dataset
├── src/
│   └── banking_api/        # Application code
├── pyproject.toml          # Python package config
└── requirements.txt        # Python dependencies
```

---

## 🔧 Docker Compose Configuration

**Current `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  api:
    build: .                          # Build from Dockerfile
    container_name: banking-api       # Container name
    ports:
      - "8000:8000"                   # Map port 8000
    volumes:
      - ./data:/app/data              # Mount data directory
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DATA_PATH=/app/data/bs140513_032310.csv
    restart: unless-stopped           # Auto-restart policy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/system/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## 📝 Docker Commands Reference

### Building

```bash
# Build the image
docker-compose build

# Build with no cache (force rebuild)
docker-compose build --no-cache

# Build using Docker CLI
docker build -t banking-api:1.0.0 .
```

### Starting & Stopping

```bash
# Start in detached mode (background)
docker-compose up -d

# Start with build
docker-compose up --build

# Stop the containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Logs & Monitoring

```bash
# View logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f api

# View last 100 lines
docker-compose logs --tail=100
```

### Container Management

```bash
# List running containers
docker-compose ps

# Execute command in container
docker-compose exec api bash

# Check container health
docker-compose exec api curl http://localhost:8000/api/system/health

# Restart container
docker-compose restart

# Stop container
docker-compose stop

# Start stopped container
docker-compose start
```

---

## 🔍 Verification Steps

### 1. Check Container Status

```bash
# List running containers
docker ps

# Expected output:
# CONTAINER ID   IMAGE          PORTS                    STATUS
# abc123...      banking-api    0.0.0.0:8000->8000/tcp   Up 2 minutes (healthy)
```

### 2. Check Health Status

```bash
# View health status
docker inspect banking-api --format='{{.State.Health.Status}}'

# Expected: healthy
```

### 3. Test API Endpoints

```bash
# Test health endpoint
curl http://localhost:8000/api/system/health

# Test transactions endpoint
curl http://localhost:8000/api/transactions?limit=5

# Test in PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/system/health"
```

### 4. Access Interactive Documentation

Open your browser:
```
http://localhost:8000/docs
```

---

## 🎯 Advanced Usage

### Custom Port Mapping

```bash
# Run on port 9000 instead of 8000
docker run -d \
  --name banking-api \
  -p 9000:8000 \
  -v ${PWD}/data:/app/data \
  banking-api:1.0.0

# Access: http://localhost:9000/docs
```

### Production Mode with Multiple Workers

Modify `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    command: uvicorn banking_api.main:app --host 0.0.0.0 --port 8000 --workers 4
    # ... rest of config
```

### Development Mode with Hot Reload

```yaml
services:
  api:
    build: .
    command: uvicorn banking_api.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./data:/app/data
      - ./src:/app/src  # Mount source code for hot reload
```

### Environment Variables File

Create `.env` file:

```env
API_HOST=0.0.0.0
API_PORT=8000
DATA_PATH=/app/data/bs140513_032310.csv
MAX_PAGE_SIZE=1000
DEFAULT_PAGE_SIZE=100
```

Update `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    env_file:
      - .env
```

---

## 🐛 Troubleshooting

### Problem: Container exits immediately

```bash
# Check logs
docker-compose logs api

# Common causes:
# - Data file not found
# - Port already in use
# - Python dependencies missing
```

### Problem: "Port 8000 already in use"

```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Solution 1: Stop the process
# Solution 2: Use different port
docker-compose up -d -p 9000:8000
```

### Problem: Data file not found

```bash
# Verify file exists
ls data/bs140513_032310.csv

# Check volume mount
docker-compose exec api ls -la /app/data/

# Check environment variable
docker-compose exec api env | grep DATA_PATH
```

### Problem: Container unhealthy

```bash
# Check health status
docker inspect banking-api | grep -A 10 Health

# Manual health check
docker-compose exec api curl http://localhost:8000/api/system/health

# Restart container
docker-compose restart
```

### Problem: Out of memory

```bash
# Set memory limits in docker-compose.yml
services:
  api:
    mem_limit: 4g
    mem_reservation: 2g
```

---

## 📊 Performance Optimization

### Multi-stage Build (Already in Dockerfile)

The Dockerfile uses Python 3.12-slim for smaller image size:
- Base image: ~150MB
- Final image: ~500MB (with dependencies)

### Resource Limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

---

## 🔐 Security Best Practices

### 1. Non-root User (Already implemented in Dockerfile)

The Dockerfile creates and uses `appuser` instead of root.

### 2. Read-only Root Filesystem

```yaml
services:
  api:
    read_only: true
    tmpfs:
      - /tmp
```

### 3. Security Options

```yaml
services:
  api:
    security_opt:
      - no-new-privileges:true
```

---

## 📦 Image Distribution

### Build and Save Image

```bash
# Build image
docker build -t banking-api:1.0.0 .

# Save to tar file
docker save banking-api:1.0.0 -o banking-api-1.0.0.tar

# Load on another machine
docker load -i banking-api-1.0.0.tar
```

### Push to Docker Hub

```bash
# Tag image
docker tag banking-api:1.0.0 yourusername/banking-api:1.0.0

# Login to Docker Hub
docker login

# Push image
docker push yourusername/banking-api:1.0.0
```

---

## 🧪 Testing in Docker

```bash
# Run tests in container
docker-compose exec api pytest tests/ -v

# Run with coverage
docker-compose exec api pytest tests/ --cov=banking_api

# Run specific test file
docker-compose exec api pytest tests/test_transactions_routes.py -v
```

---

## 🔄 Complete Workflow Example

```bash
# 1. Clone repository
git clone https://github.com/masiszovikoglu/projet_python_2_mba.git
cd projet_python_2_mba

# 2. Download and place data file
# Place bs140513_032310.csv in data/ folder

# 3. Build and start
docker-compose up --build -d

# 4. Check logs
docker-compose logs -f

# 5. Verify API is running
curl http://localhost:8000/api/system/health

# 6. Open browser
# http://localhost:8000/docs

# 7. When done, stop and clean up
docker-compose down
```

---

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **FastAPI in Docker**: https://fastapi.tiangolo.com/deployment/docker/
- **Best Practices**: https://docs.docker.com/develop/dev-best-practices/

---

## ✅ Summary

Your Banking API is **Docker-ready** with:

- ✅ **Dockerfile** - Optimized Python 3.12 image
- ✅ **docker-compose.yml** - Easy orchestration
- ✅ **Health checks** - Container monitoring
- ✅ **Volume mounts** - Persistent data
- ✅ **Environment variables** - Flexible configuration
- ✅ **Auto-restart** - High availability
- ✅ **Port mapping** - External access

**Start your API in Docker with one command:**
```bash
docker-compose up -d
```

🎉 **Your API is containerized and production-ready!**
